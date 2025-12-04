from ...infrastructure.database.models import TenantModel

print("✅ Modelos importados correctamente")


def get_models():
    return [TenantModel]


if __name__ == "__main__":
    print("Todos los modelos cargan sin errores de importación circular")
