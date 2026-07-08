import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.claude_runner import ClaudeRunner
from app.config import DEFAULT_DOMAINS, DOCUMENTS_DIR, OUTPUT_DIR, MIN_CLAIMS_PER_DOMAIN
from app.contracts import AGENT_RESULT_CONTRACT, REPORT_CONTRACT
from app.json_utils import extract_json_object, write_json
from app.mappings import build_claim_source_mappings


class ResearchCoordinator:
    def __init__(self, runner: ClaudeRunner | None = None):
        self.runner = runner or ClaudeRunner()
        self.access_date = datetime.now(timezone.utc).date().isoformat()

    async def _run_json_agent(
        self,
        agent_name: str,
        prompt: str,
        fallback_domain: str,
    ) -> dict[str, Any]:
        run = await self.runner.run(prompt)

        if not run.text.strip():
            return {
                "agent": agent_name,
                "status": "error",
                "topic": "",
                "domain": fallback_domain,
                "summary": "No hubo respuesta útil del agente.",
                "claims": [],
                "warnings": [],
                "error": "; ".join(run.errors or ["Error desconocido"]),
            }

        try:
            parsed = extract_json_object(run.text)
            if not run.ok and parsed.get("status") == "ok":
                parsed["status"] = "partial"
                parsed.setdefault("warnings", []).append(
                    f"El SDK devolvió subtipo {run.subtype}; se conserva resultado parcial."
                )
            return parsed
        except Exception as ex:
            return {
                "agent": agent_name,
                "status": "partial" if run.text.strip() else "error",
                "topic": "",
                "domain": fallback_domain,
                "summary": "El agente respondió, pero no se pudo parsear como JSON. Se conserva texto parcial.",
                "claims": [],
                "warnings": [f"Error parseando JSON: {ex}", run.text[:2000]],
                "error": None if run.text.strip() else str(ex),
            }

    async def search_domain(self, topic: str, domain: str) -> dict[str, Any]:
        prompt = f"""
Usa obligatoriamente el subagente `search-agent` mediante la herramienta Agent.

Tema general:
{topic}

Dominio específico:
{domain}

Fecha de acceso para fuentes sin fecha de publicación:
{self.access_date}

Tarea:
Investiga este dominio y devuelve claims citables con URL, fecha y evidencia.
No analices otros dominios.

{AGENT_RESULT_CONTRACT}
"""
        return await self._run_json_agent("search-agent", prompt, domain)

    async def analyze_documents(self, topic: str, docs_dir: Path) -> dict[str, Any]:
        docs_dir.mkdir(parents=True, exist_ok=True)
        files = [p.name for p in docs_dir.iterdir() if p.is_file()]

        if not files:
            return {
                "agent": "document-agent",
                "status": "partial",
                "topic": topic,
                "domain": "documentos locales",
                "summary": "No se encontraron documentos locales para analizar.",
                "claims": [],
                "warnings": ["La carpeta documents está vacía."],
                "error": None,
            }

        prompt = f"""
Usa obligatoriamente el subagente `document-agent` mediante la herramienta Agent.

Tema general:
{topic}

Carpeta de documentos:
{docs_dir}

Archivos disponibles:
{json.dumps(files, ensure_ascii=False, indent=2)}

Fecha de acceso:
{self.access_date}

Tarea:
Analiza los documentos locales y extrae claims citables.

{AGENT_RESULT_CONTRACT}
"""
        return await self._run_json_agent("document-agent", prompt, "documentos locales")

    def validate_coverage(self, results: list[dict[str, Any]], domains: list[str]) -> list[str]:
        missing: list[str] = []

        for domain in domains:
            domain_results = [r for r in results if r.get("domain") == domain]
            claim_count = sum(len(r.get("claims", []) or []) for r in domain_results)
            has_error_only = all(r.get("status") == "error" for r in domain_results) if domain_results else True

            if claim_count < MIN_CLAIMS_PER_DOMAIN or has_error_only:
                missing.append(domain)

        return missing

    async def synthesize(self, topic: str, agent_results: list[dict[str, Any]], missing_domains: list[str]) -> dict[str, Any]:
        prompt = f"""
Usa obligatoriamente el subagente `synthesis-agent` mediante la herramienta Agent.

Tema:
{topic}

Dominios con cobertura insuficiente:
{json.dumps(missing_domains, ensure_ascii=False, indent=2)}

Resultados de agentes anteriores:
{json.dumps(agent_results, ensure_ascii=False, indent=2)}

Tarea:
Sintetiza los hallazgos manteniendo claim-source mappings.
No inventes información nueva.

{AGENT_RESULT_CONTRACT}
"""
        return await self._run_json_agent("synthesis-agent", prompt, "síntesis")

    async def generate_report(self, topic: str, agent_results: list[dict[str, Any]], mappings: list[dict[str, Any]]) -> str:
        prompt = f"""
Usa obligatoriamente el subagente `report-agent` mediante la herramienta Agent.

Tema:
{topic}

Resultados de agentes:
{json.dumps(agent_results, ensure_ascii=False, indent=2)}

Claim-source mappings:
{json.dumps(mappings, ensure_ascii=False, indent=2)}

{REPORT_CONTRACT}
"""
        run = await self.runner.run(prompt, max_turns=6)

        if not run.ok and run.text.strip():
            return (
                run.text
                + "\n\n---\n\n"
                + "## Nota de ejecución\n"
                + f"El SDK devolvió estado parcial: {run.subtype}. Errores: {run.errors}\n"
            )

        if not run.text.strip():
            return (
                "# Reporte de investigación\n\n"
                "No se pudo generar el reporte final. "
                f"Errores: {run.errors}\n"
            )

        return run.text

    async def run(
        self,
        topic: str,
        domains: list[str] | None = None,
        docs_dir: Path = DOCUMENTS_DIR,
        output_name: str = "reporte_final.md",
    ) -> Path:
        domains = domains or DEFAULT_DOMAINS
        agent_results: list[dict[str, Any]] = []

        for domain in domains:
            print(f"Investigando dominio: {domain}")
            result = await self.search_domain(topic, domain)
            agent_results.append(result)

        document_result = await self.analyze_documents(topic, docs_dir)
        agent_results.append(document_result)

        missing = self.validate_coverage(agent_results, domains)

        if missing:
            print("Cobertura insuficiente. Se hará un reintento por dominio faltante.")
            for domain in missing:
                retry_result = await self.search_domain(topic, domain)
                retry_result["domain"] = domain
                retry_result.setdefault("warnings", []).append("Resultado obtenido en reintento de cobertura.")
                agent_results.append(retry_result)

        missing = self.validate_coverage(agent_results, domains)

        synthesis = await self.synthesize(topic, agent_results, missing)
        agent_results.append(synthesis)

        mappings = build_claim_source_mappings(agent_results)
        report = await self.generate_report(topic, agent_results, mappings)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        write_json(OUTPUT_DIR / "run_results.json", agent_results)
        write_json(OUTPUT_DIR / "claim_source_mappings.json", mappings)

        report_path = OUTPUT_DIR / output_name
        report_path.write_text(report, encoding="utf-8")

        return report_path
