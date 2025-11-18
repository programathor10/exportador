# main.py
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from api_client import APIClientError, fetch_posts, fetch_users
from exporters import ensure_output_dir, export_to_excel, export_to_json
from processors import DataValidationError, validate_posts, validate_users, build_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Script de integración con API y exportación a Excel/JSON."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Cantidad máxima de posts a descargar (por defecto: 20). 0 = sin límite.",
    )
    parser.add_argument(
        "--format",
        choices=["excel", "json", "both"],
        default="both",
        help="Formato de salida (por defecto: both).",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directorio donde se guardarán los reportes (por defecto: output).",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Nivel de logs (por defecto: INFO).",
    )
    return parser.parse_args()


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def main() -> None:
    args = parse_args()
    configure_logging(args.log_level)

    if args.limit == 0:
        limit = None
    else:
        limit = args.limit

    logging.info("Iniciando generación de reporte...")

    try:
        posts = fetch_posts(limit=limit)
        users = fetch_users()

        validate_posts(posts)
        validate_users(users)

        df = build_report(posts, users)

        output_dir = ensure_output_dir(args.output_dir)

        if args.format in ("excel", "both"):
            excel_path = export_to_excel(df, output_dir)
            logging.info("Reporte Excel generado en: %s", excel_path)

        if args.format in ("json", "both"):
            json_path = export_to_json(df, output_dir)
            logging.info("Reporte JSON generado en: %s", json_path)

    except (APIClientError, DataValidationError) as exc:
        logging.error("Error procesando datos: %s", exc)
        raise SystemExit(1)
    except Exception as exc:  # catch-all
        logging.exception("Error inesperado")
        raise SystemExit(1)

    logging.info("Proceso terminado correctamente.")


if __name__ == "__main__":
    main()
