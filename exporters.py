# exporters.py
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd


def ensure_output_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def export_to_excel(df: pd.DataFrame, output_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"reporte_posts_{timestamp}.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


def export_to_json(df: pd.DataFrame, output_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"reporte_posts_{timestamp}.json"

    records = df.to_dict(orient="records")
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return file_path
