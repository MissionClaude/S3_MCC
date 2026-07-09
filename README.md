# Multi-Agent Research System con Claude Agent SDK

Sistema de investigación multiagente en Python:

- Coordinador en Python.
- Subagente de búsqueda web.
- Subagente de análisis documental.
- Subagente de síntesis.
- Subagente de generación de reporte.
- Claim-source mappings con URL, fecha de acceso y evidencia.
- Propagación de errores con resultados parciales.

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Prueba rápida para ver si esta funcional tanto el sdk 

```powershell
python -m app.smoke_test
```
## Prueba si el api esta bien 

```powershell
python -m app.test_api_key
```
## Prueba sensilla 

```powershell
python app/test_simple_research.py
```

## Ejecutar investigación

```powershell
python -m app.main --topic "Impacto de la IA en las industrias creativas"
```

## Ejecutar pruebas locales

```powershell
pytest
```

## Archivos generados

- `output/reporte_ia.md`
- `output/claim_source_mappings.json`
- `output/run_results.json`

## Archivo .env qie es de cofiguracion
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=
CLAUDE_MAX_TURNS=3
SUBAGENT_MAX_TURNS=2
CLAUDE_TIMEOUT_SECONDS=60
MAX_DOMAINS=1
MIN_CLAIMS_PER_DOMAIN=1
AGENT_TEMPERATURE=0.2