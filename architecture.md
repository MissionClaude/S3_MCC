# Arquitectura del sistema multiagente

El sistema utiliza una arquitectura jerárquica tipo Coordinator / Supervisor - Subagents.

Un agente coordinador recibe el tema de investigación, divide el trabajo en dominios y delega tareas a subagentes especializados. Cada subagente cumple una función específica: búsqueda web, análisis documental, síntesis de hallazgos y generación de reportes.

La arquitectura también funciona como un pipeline secuencial, donde los resultados de una etapa sirven como entrada para la siguiente:

1. Planificación de la investigación.
2. Búsqueda web por dominio.
3. Análisis de documentos locales.
4. Validación de cobertura.
5. Síntesis de hallazgos.
6. Generación del reporte final.
7. Registro de claim-source mappings.

El coordinador centraliza los resultados parciales, controla errores, valida la cobertura mínima y evita generar el reporte final si la evidencia es insuficiente.