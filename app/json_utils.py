import json
import re
from typing import Any


def extract_json_object(text: str) -> dict[str, Any]:
    """Extrae un objeto JSON desde texto plano o desde un bloque ```json."""
    if not text or not text.strip():
        raise ValueError("La respuesta está vacía; no se puede extraer JSON.")

    clean = text.strip()

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", clean, flags=re.DOTALL)
    if fenced:
        clean = fenced.group(1).strip()

    if not clean.startswith("{"):
        start = clean.find("{")
        end = clean.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No se encontró un objeto JSON válido en la respuesta.")
        clean = clean[start:end + 1]

    return json.loads(clean)


def write_json(path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
