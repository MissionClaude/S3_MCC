import argparse
import asyncio
from pathlib import Path

from app.coordinator import ResearchCoordinator
from app.config import DOCUMENTS_DIR


async def async_main() -> None:
    parser = argparse.ArgumentParser(
        description="Sistema de investigación multiagente con Claude Agent SDK."
    )
    parser.add_argument("--topic", required=True, help="Tema de investigación")
    parser.add_argument("--docs", default=str(DOCUMENTS_DIR), help="Carpeta de documentos")
    parser.add_argument("--output", default="reporte_final.md", help="Archivo Markdown de salida")

    args = parser.parse_args()

    coordinator = ResearchCoordinator()
    report_path = await coordinator.run(
        topic=args.topic,
        docs_dir=Path(args.docs),
        output_name=args.output,
    )

    print(f"Reporte generado: {report_path}")


if __name__ == "__main__":
    asyncio.run(async_main())
