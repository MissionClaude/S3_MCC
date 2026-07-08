AGENT_RESULT_CONTRACT = """
Devuelve SOLO un JSON válido, sin markdown, con esta estructura exacta:
{
  "agent": "nombre-del-agente",
  "status": "ok | partial | error",
  "topic": "tema investigado",
  "domain": "dominio o alcance",
  "summary": "resumen breve",
  "claims": [
    {
      "claim": "afirmación concreta",
      "confidence": "high | medium | low",
      "sources": [
        {
          "url": "URL completa de la fuente, si existe",
          "title": "título de la fuente",
          "date": "fecha de publicación o fecha de acceso en ISO YYYY-MM-DD",
          "evidence": "evidencia breve que respalda el claim"
        }
      ]
    }
  ],
  "warnings": ["advertencias o limitaciones"],
  "error": null
}

Reglas:
- Cada claim debe tener al menos una fuente cuando venga de web.
- No inventes URLs.
- Si una parte falla, usa status = "partial" y explica en warnings.
- Si no puedes completar la tarea, usa status = "error" y llena error.
"""

REPORT_CONTRACT = """
Genera el reporte final en Markdown con esta estructura:

# Reporte de investigación

## 1. Resumen ejecutivo
## 2. Alcance y metodología
## 3. Matriz de cobertura
## 4. Hallazgos por dominio
## 5. Síntesis transversal
## 6. Riesgos, controversias y limitaciones
## 7. Conclusiones
## 8. Fuentes

Reglas:
- Usa únicamente claims y fuentes entregadas por los agentes anteriores.
- No inventes datos, citas ni URLs.
- Si hubo resultados parciales, inclúyelos en limitaciones.
- Cada hallazgo importante debe incluir la referencia de su fuente.
"""
