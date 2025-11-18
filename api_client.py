# api_client.py
from __future__ import annotations

import logging
from typing import Any, List, Dict

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


class APIClientError(Exception):
    """Errores genéricos del cliente de API."""


def _get(path: str, timeout: int = 10) -> Any:
    """Hace un GET a la API y devuelve el JSON ya parseado."""
    url = f"{BASE_URL}{path}"
    logging.info("Llamando a la API: %s", url)

    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logging.exception("Error al hacer la petición HTTP")
        raise APIClientError(f"Error de red o HTTP al llamar {url}") from exc

    try:
        data = resp.json()
    except ValueError as exc:
        logging.exception("La respuesta de la API no es JSON válido")
        raise APIClientError("La API devolvió una respuesta no válida (no JSON)") from exc

    return data


def fetch_posts(limit: int | None = None) -> List[Dict[str, Any]]:
    """Descarga posts. Opcional: limitar la cantidad."""
    data = _get("/posts")

    if not isinstance(data, list):
        raise APIClientError("Formato inesperado para /posts (no es lista)")

    if limit is not None:
        data = data[:limit]

    return data


def fetch_users() -> List[Dict[str, Any]]:
    """Descarga usuarios."""
    data = _get("/users")

    if not isinstance(data, list):
        raise APIClientError("Formato inesperado para /users (no es lista)")

    return data
