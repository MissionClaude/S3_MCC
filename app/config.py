import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR

DOCUMENTS_DIR = BASE_DIR / "documents"
OUTPUT_DIR = BASE_DIR / "output"

ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise RuntimeError(
        f"No se encontró ANTHROPIC_API_KEY. Verifica el archivo: {ENV_FILE}"
    )

os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY


# ============================================================
# MODELO Y VELOCIDAD
# ============================================================

CLAUDE_MODEL = os.getenv("ANTHROPIC_MODEL", "haiku").strip()
CLAUDE_MAX_TURNS = int(os.getenv("CLAUDE_MAX_TURNS", "3"))
SUBAGENT_MAX_TURNS = int(os.getenv("SUBAGENT_MAX_TURNS", "2"))
CLAUDE_TIMEOUT_SECONDS = int(os.getenv("CLAUDE_TIMEOUT_SECONDS", "60"))
MIN_CLAIMS_PER_DOMAIN = int(os.getenv("MIN_CLAIMS_PER_DOMAIN", "1"))
MAX_DOMAINS = int(os.getenv("MAX_DOMAINS", "0"))


ALL_DOMAINS = [
    "artes visuales y arte digital",
    "música y producción musical",
    "escritura, periodismo y literatura",
    "cine, video y producción audiovisual",
    "fotografía",
    "diseño gráfico y publicidad",
    "videojuegos y animación",
]

if MAX_DOMAINS > 0:
    DEFAULT_DOMAINS = ALL_DOMAINS[:MAX_DOMAINS]
else:
    DEFAULT_DOMAINS = ALL_DOMAINS