import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env", override=True)


async def main():
    model = os.getenv("ANTHROPIC_MODEL", "haiku")

    options = ClaudeAgentOptions(
        model=model,
        allowed_tools=["WebSearch"],
        setting_sources=[],
        cwd=str(PROJECT_ROOT),
        max_turns=4,
    )

    prompt = """
Investiga brevemente el impacto de la IA en artes visuales.
Usa máximo una búsqueda web.
Devuelve máximo 2 hallazgos.
Responde en español.
"""

    async for message in query(prompt=prompt, options=options):
        print("Mensaje:", type(message).__name__)

        if isinstance(message, ResultMessage):
            print("RESULTADO:")
            print(message.result)


if __name__ == "__main__":
    asyncio.run(main())