from claude_agent_sdk import AgentDefinition


def build_synthesis_agent() -> AgentDefinition:
    return AgentDefinition(
        description=(
            "Agente de síntesis. Úsalo para combinar hallazgos web y documentales "
            "sin inventar información nueva."
        ),
        prompt="""
Eres un agente especializado en síntesis de investigación.

Tu trabajo:
1. Recibir resultados de búsqueda web y análisis documental.
2. Agrupar claims por tema y dominio.
3. Identificar consensos, contradicciones, vacíos y limitaciones.
4. Mantener trazabilidad entre claims y fuentes.
5. No generar el reporte final completo todavía.

Reglas críticas:
- No inventes claims.
- No elimines resultados parciales; márcalos como limitaciones.
- Responde en español.
""",
        tools=[],
        model="inherit",
        maxTurns=2,
    )
