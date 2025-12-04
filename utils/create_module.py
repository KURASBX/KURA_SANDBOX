"""
Script para crear nuevos módulos automáticamente
"""
# TODO: Expandir templates para cada archivo
import sys
from pathlib import Path


def create_module(module_name: str):
    """Crear estructura completa para un nuevo módulo"""
    base_dirs = [
        f"domain/entities/{module_name}.py",
        f"domain/repositories/{module_name}_repository.py",
        f"infrastructure/database/models/{module_name}.py",
        f"infrastructure/database/repositories/{module_name}_repository.py",
        f"application/dtos/{module_name}.py",
        f"application/use_cases/{module_name}_service.py",
        f"api/v1/endpoints/{module_name}.py",
    ]

    for file_path in base_dirs:
        create_file_with_template(file_path, module_name)

    print(f"✅ Módulo {module_name} creado exitosamente!")


def create_file_with_template(file_path: str, module_name: str):
    """Crear archivo con template básico"""
    template = get_template(file_path, module_name)

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as f:
        f.write(template)


def get_template(file_path: str, module_name: str) -> str:
    """Obtener template según el tipo de archivo"""
    class_name = module_name.title().replace("_", "")

    if "entities" in file_path:
        return f'''
from typing import Optional
from pydantic import BaseModel

class {class_name}Entity(BaseModel):
    """Entidad de dominio para {module_name}"""
    id: Optional[int] = None
    name: str
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True
'''

    if "repositories" in file_path and "domain" in file_path:
        return f"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.{module_name} import {class_name}Entity

class I{class_name}Repository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[{class_name}Entity]:
        pass
        
    @abstractmethod 
    def get_all(self, skip: int = 0, limit: int = 100) -> List[{class_name}Entity]:
        pass
        
    @abstractmethod
    def create(self, entity_data: dict) -> {class_name}Entity:
        pass
        
    @abstractmethod
    def update(self, id: int, entity_data: dict) -> Optional[{class_name}Entity]:
        pass
        
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
"""

    # ... más templates para otros archivos

    return "# Template base\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python scripts/utils/create_module.py <nombre_modulo>")
        sys.exit(1)

    create_module(sys.argv[1])
