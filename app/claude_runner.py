import asyncio
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from app.agents import build_agents
from app import config


# ============================================================
# CONFIGURACIÓN BASE
# ============================================================

BASE_DIR = getattr(config, "BASE_DIR", Path(__file__).resolve().parents[1])
PROJECT_ROOT = getattr(config, "PROJECT_ROOT", BASE_DIR)
ENV_FILE = BASE_DIR / ".env"


# ============================================================
# CARGAR .env DEL PROYECTO
# ============================================================

load_dotenv(dotenv_path=ENV_FILE, override=True)


def _get_env_value(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return value.strip()


def _get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None or not value.strip():
        return default

    try:
        return int(value)
    except ValueError:
        return default


ANTHROPIC_API_KEY = getattr(
    config,
    "ANTHROPIC_API_KEY",
    os.getenv("ANTHROPIC_API_KEY"),
)

if not ANTHROPIC_API_KEY:
    raise RuntimeError(
        "\nNo se encontró ANTHROPIC_API_KEY.\n\n"
        f"Debes crear el archivo .env aquí:\n{ENV_FILE}\n\n"
        "Contenido esperado:\n"
        "ANTHROPIC_API_KEY=tu_api_key_de_claude\n"
        "ANTHROPIC_MODEL=haiku\n"
        "CLAUDE_MAX_TURNS=5\n"
        "CLAUDE_TIMEOUT_SECONDS=180\n"
    )

# Asegura que el SDK reciba la API key cargada desde el .env local
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY


CLAUDE_MODEL = getattr(
    config,
    "CLAUDE_MODEL",
    _get_env_value("ANTHROPIC_MODEL", "haiku"),
)

CLAUDE_MAX_TURNS = getattr(
    config,
    "CLAUDE_MAX_TURNS",
    _get_env_int("CLAUDE_MAX_TURNS", 5),
)

CLAUDE_TIMEOUT_SECONDS = getattr(
    config,
    "CLAUDE_TIMEOUT_SECONDS",
    _get_env_int("CLAUDE_TIMEOUT_SECONDS", 180),
)


# ============================================================
# RESULTADO ESTÁNDAR
# ============================================================

@dataclass
class RunOutput:
    ok: bool
    text: str
    subtype: Optional[str] = None
    errors: Optional[list[str]] = None


# ============================================================
# CLAUDE RUNNER
# ============================================================

class ClaudeRunner:
    def __init__(self, cwd: Optional[Path] = None):
        self.cwd = cwd or PROJECT_ROOT

    async def run(
        self,
        prompt: str,
        max_turns: Optional[int] = None,
    ) -> RunOutput:
        """
        Ejecuta Claude Agent SDK con timeout.

        Devuelve un objeto compatible con coordinator.py:

        - run.ok
        - run.text
        - run.subtype
        - run.errors
        """

        turns = max_turns or CLAUDE_MAX_TURNS

        try:
            return await asyncio.wait_for(
                self._execute_claude(
                    prompt=prompt,
                    max_turns=turns,
                ),
                timeout=CLAUDE_TIMEOUT_SECONDS,
            )

        except asyncio.TimeoutError:
            return RunOutput(
                ok=False,
                text="",
                subtype="timeout",
                errors=[
                    f"La ejecución superó {CLAUDE_TIMEOUT_SECONDS} segundos.",
                    "Para probar más rápido usa ANTHROPIC_MODEL=haiku, MAX_DOMAINS=1 y CLAUDE_MAX_TURNS=5.",
                ],
            )

        except Exception as ex:
            error_text = str(ex)

            if "Not logged in" in error_text or "/login" in error_text:
                return RunOutput(
                    ok=False,
                    text="",
                    subtype="not_logged_in",
                    errors=[
                        "Claude Agent SDK no está tomando la API key del proyecto.",
                        f"Verifica que exista el archivo .env aquí: {ENV_FILE}",
                        "Verifica que el .env tenga: ANTHROPIC_API_KEY=tu_api_key_de_claude",
                    ],
                )

            return RunOutput(
                ok=False,
                text="",
                subtype="unexpected_error",
                errors=[error_text],
            )

    async def _execute_claude(
        self,
        prompt: str,
        max_turns: int,
    ) -> RunOutput:
        """
        Ejecuta directamente query() del Claude Agent SDK.
        """

        options = ClaudeAgentOptions(
            model=CLAUDE_MODEL,
            agents=build_agents(),
            allowed_tools=[
                "Agent",
                "WebSearch",
                "WebFetch",
                "Read",
                "Glob",
                "Grep",
            ],
            setting_sources=[],
            cwd=str(self.cwd),
            max_turns=max_turns,
        )

        last_result: Optional[RunOutput] = None

        async for message in query(
            prompt=prompt,
            options=options,
        ):
            # Esto te ayuda a ver que no está congelado
            message_type = type(message).__name__

            if message_type == "TaskStartedMessage":
                print("[SDK] Subagente iniciado...")

            elif message_type == "TaskProgressMessage":
                print(".", end="", flush=True)

            elif isinstance(message, ResultMessage):
                print("\n[SDK] Resultado final recibido.")

            if isinstance(message, ResultMessage):
                subtype = getattr(message, "subtype", None)
                is_error = getattr(message, "is_error", False)
                result_text = getattr(message, "result", "") or ""
                errors = getattr(message, "errors", None) or []

                last_result = RunOutput(
                    ok=(not is_error and subtype == "success"),
                    text=str(result_text),
                    subtype=subtype,
                    errors=errors,
                )

        if last_result is None:
            return RunOutput(
                ok=False,
                text="",
                subtype="no_result",
                errors=[
                    "Claude terminó, pero no devolvió ResultMessage.",
                    "Puede ser problema de autenticación, modelo, permisos o timeout interno.",
                ],
            )

        return last_result

    async def execute(self, prompt: str) -> RunOutput:
        """
        Alias por compatibilidad.
        """
        return await self.run(prompt)

    async def ask(self, prompt: str) -> RunOutput:
        """
        Alias por compatibilidad.
        """
        return await self.run(prompt)


# ============================================================
# FUNCIÓN OPCIONAL PARA ARCHIVOS QUE USEN run_claude()
# ============================================================

async def run_claude(
    prompt: str,
    cwd: Optional[Path] = None,
    max_turns: Optional[int] = None,
) -> str:
    runner = ClaudeRunner(cwd=cwd)
    result = await runner.run(
        prompt=prompt,
        max_turns=max_turns,
    )

    if not result.ok and not result.text.strip():
        raise RuntimeError(
            "Claude no devolvió texto útil.\n"
            f"Subtipo: {result.subtype}\n"
            f"Errores: {result.errors}"
        )

    return result.text