import os

from claude_agent_sdk import AgentDefinition


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)

    if not value:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def build_search_agent() -> AgentDefinition:
    model = os.getenv("ANTHROPIC_MODEL", "haiku")
    max_turns = _env_int("SUBAGENT_MAX_TURNS", 2)

    return AgentDefinition(
        description=(
            "Agente de búsqueda web rápida. Úsalo para obtener pocos claims "
            "con fuentes y evidencia verificable."
        ),
        prompt="""
Eres un agente de investigación web rápida.

Reglas obligatorias:
1. Usa máximo una búsqueda web.
2. No hagas navegación extensa.
3. No generes reporte final.
4. Devuelve máximo 2 claims.
5. Responde únicamente con JSON válido.
6. No escribas texto antes ni después del JSON.
7. No inventes URLs, fechas ni evidencia.

Formato obligatorio:

{
  "agent": "search-agent",
  "status": "ok",
  "topic": "",
  "domain": "",
  "summary": "",
  "claims": [
    {
      "claim": "",
      "source_url": "",
      "source_title": "",
      "source_date": "",
      "access_date": "",
      "evidence": ""
    }
  ],
  "warnings": [],
  "error": null
}

Si hay poca información, usa:
"status": "partial"
""",
        tools=["WebSearch"],
        model=model,
        maxTurns=max_turns,
    )