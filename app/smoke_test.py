import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)


async def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise RuntimeError(
            f"No se encontró ANTHROPIC_API_KEY. "
            f"Verifica que exista este archivo: {ENV_FILE}"
        )

    options = ClaudeAgentOptions(
        allowed_tools=[],
        setting_sources=[],
        max_turns=3,
    )

    async for message in query(
        prompt="Responde exactamente: SDK OK",
        options=options,
    ):
        if isinstance(message, ResultMessage):
            print(message.result)


if __name__ == "__main__":
    asyncio.run(main())