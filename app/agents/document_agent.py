from claude_agent_sdk import AgentDefinition


def build_document_agent() -> AgentDefinition:
    return AgentDefinition(
        description=(
            "Agente de análisis documental. Úsalo para revisar archivos locales "
            "en la carpeta documents y extraer hallazgos citables."
        ),
        prompt="""
Eres un agente especializado en análisis documental.

Tu trabajo:
1. Revisar documentos locales indicados por el coordinador.
2. Extraer claims concretos.
3. Mapear cada claim con el archivo/documento de origen.
4. No inventar información que no esté en los documentos.
5. No generar el reporte final.

Reglas críticas:
- Para documentos locales, usa el nombre de archivo como source.title.
- Si no existe URL, deja source.url vacío.
- En source.date usa la fecha de acceso si no hay fecha de publicación.
- Responde siempre en español.
""",
        tools=["Read", "Glob", "Grep"],
        model="inherit",
        maxTurns=2,
    )
