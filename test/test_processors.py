# tests/test_processors.py
import sys
from pathlib import Path

# Agregamos la raíz del proyecto al sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
from processors import validate_posts, validate_users, build_report, DataValidationError


def test_validate_posts_ok():
    posts = [
        {"userId": 1, "id": 1, "title": "Titulo", "body": "Contenido"},
        {"userId": 2, "id": 2, "title": "Otro", "body": "Más contenido"},
    ]

    # No debería lanzar excepción
    validate_posts(posts)


def test_validate_posts_falla_si_faltan_claves():
    posts = [
        {"userId": 1, "title": "Sin ID ni body"},
    ]

    try:
        validate_posts(posts)
        assert False, "Debería lanzar DataValidationError si faltan claves"
    except DataValidationError:
        assert True


def test_validate_users_ok():
    users = [
        {
            "id": 1,
            "name": "Bruno",
            "email": "bruno@example.com",
            "company": {"name": "Empresa X"},
        }
    ]

    validate_users(users)  # no debe fallar


def test_build_report_devuelve_columnas_esperadas():
    posts = [
        {"userId": 1, "id": 1, "title": "Titulo", "body": "Contenido"},
    ]
    users = [
        {
            "id": 1,
            "name": "Bruno",
            "email": "bruno@example.com",
            "company": {"name": "Empresa X"},
        }
    ]

    df = build_report(posts, users)

    # El DataFrame debe tener al menos estas columnas
    for col in ["id", "userId", "user_name", "user_email", "company_name", "title", "body"]:
        assert col in df.columns

    # Y una sola fila
    assert len(df) == 1
    assert df.loc[0, "user_name"] == "Bruno"
