"""
Script para inicializar la base de datos
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from core.database import Base, engine
from infrastructure.database.models import *  # noqa: F403


def init_db():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Eliminar todas las tablas (solo para desarrollo)"""
    Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gestión de Base de Datos")
    parser.add_argument("--init", action="store_true", help="Inicializar base de datos")
    parser.add_argument("--drop", action="store_true", help="Eliminar todas las tablas")
    parser.add_argument("--reset", action="store_true", help="Reiniciar base de datos")

    args = parser.parse_args()

    if args.drop or args.reset:
        drop_db()

    if args.init or args.reset:
        init_db()
