# processors.py
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Set

import pandas as pd


class DataValidationError(Exception):
    """Se lanza cuando los datos de la API no tienen el formato esperado."""


def _validate_required_keys(
    records: Iterable[Dict[str, Any]],
    required_keys: Set[str],
    record_name: str,
) -> None:
    """
    Valida que cada dict en 'records' contenga las claves requeridas.
    Lanza DataValidationError si falta algo.
    """
    for idx, rec in enumerate(records):
        missing = required_keys - rec.keys()
        if missing:
            raise DataValidationError(
                f"El {record_name} #{idx} no tiene las claves requeridas: {missing}"
            )


def validate_posts(posts: List[Dict[str, Any]]) -> None:
    required = {"userId", "id", "title", "body"}
    _validate_required_keys(posts, required, "post")


def validate_users(users: List[Dict[str, Any]]) -> None:
    required = {"id", "name", "email", "company"}
    _validate_required_keys(users, required, "usuario")


def build_report(posts: List[Dict[str, Any]], users: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Combina posts con datos de usuario (nombre, email, empresa) en un DataFrame.
    """
    df_posts = pd.DataFrame(posts)
    df_users = pd.DataFrame(users)

    # Nos quedamos con algunas columnas útiles de usuarios
    if "company" in df_users.columns:
        # company es un objeto, lo convertimos a string legible
        df_users["company_name"] = df_users["company"].apply(
            lambda c: c.get("name") if isinstance(c, dict) else None
        )

    df_users = df_users.rename(
        columns={
            "id": "userId",
            "name": "user_name",
            "email": "user_email",
        }
    )

    columnas_users = ["userId", "user_name", "user_email", "company_name"]
    columnas_users = [c for c in columnas_users if c in df_users.columns]

    df_users = df_users[columnas_users]

    # Join por userId
    df = df_posts.merge(df_users, on="userId", how="left")

    # Ordenar columnas de forma linda
    columnas_ordenadas = [
        "id",
        "userId",
        "user_name",
        "user_email",
        "company_name",
        "title",
        "body",
    ]
    columnas_existentes = [c for c in columnas_ordenadas if c in df.columns]
    df = df[columnas_existentes]

    return df
