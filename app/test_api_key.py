import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")
model = os.getenv("ANTHROPIC_MODEL", "haiku")


async def main():
    if not api_key:
        print("ERROR: No se encontró ANTHROPIC_API_KEY en el archivo .env")
        print(f"Ruta esperada: {ENV_FILE}")
        return

    print("API KEY encontrada en .env")
    print(f"Modelo configurado: {model}")
    print("Enviando prueba a Claude...")

    options = ClaudeAgentOptions(
        model=model,
        allowed_tools=[],
        setting_sources=[],
        max_turns=3,
        cwd=str(PROJECT_ROOT),
    )

    async for message in query(
        prompt="Responde exactamente: API KEY OK",
        options=options,
    ):
        print("Mensaje recibido:", type(message).__name__)

        if isinstance(message, ResultMessage):
            print("RESULTADO FINAL:")
            print(message.result)

            if "API KEY OK" in str(message.result):
                print("PRUEBA CORRECTA: la API key sí devuelve resultado.")
            else:
                print("La API respondió, pero no devolvió el texto esperado.")


if __name__ == "__main__":
    asyncio.run(main())