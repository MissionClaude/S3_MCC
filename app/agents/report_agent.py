from claude_agent_sdk import AgentDefinition


def build_report_agent() -> AgentDefinition:
    return AgentDefinition(
        description=(
            "Agente generador de reportes. Úsalo solo al final para redactar "
            "un reporte completo con citas y limitaciones."
        ),
        prompt="""
Eres un agente especializado en redacción de reportes profesionales.

Tu trabajo:
1. Crear el reporte final en Markdown.
2. Usar solo los claims, fuentes y síntesis entregados.
3. Incluir citas o referencias por hallazgo.
4. Incluir limitaciones y resultados parciales.

Reglas críticas:
- No agregues información nueva.
- No inventes fuentes.
- No ocultes errores; colócalos en limitaciones.
- Responde en español.
""",
        tools=[],
        model="inherit",
        maxTurns=2,
    )
