**LEVANTAR EL SANDBOX**

1. En VS Code: Terminal → New Terminal
estar en:

PS D:\Proyecto KURA\KURA_SANDBOX>


2. Bajamos cualquier contenedor viejo (por si quedó algo colgado):

docker compose down -v


3. Levantamos y construimos todo:

docker compose up --build


4. Esperar los logs hasta ver algo como:

    - Base de datos lista
    - Iniciando aplicación...
    - Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

# Esa terminal queda “ocupada” mostrando logs. No la cierres.

**VERIFICAR QUE ESTÁ TODO OK**

1. Abrí el navegador (Chrome) y entrá a:

http://localhost:8050/api/health/

# Deberías ver algo como:
```json
{
  "status": "healthy",
  "service": "Kura Sandbox",
  "environment": "production",
  "version": "1.0.0"
}


Para mostrar la API al cliente (banco, Tecnoglobal, etc.):

http://localhost:8050/docs


Ahí se ve:

    - Sección Health → GET /api/health/
    - Endpoints de aliases:
    - POST /api/v1/aliases/ (registrar alias)
    - GET /api/v1/aliases/{alias} (resolver alias)
    - DELETE /api/v1/aliases/{alias} (baja)
    - etc.

usar “Try it out” en Swagger para hacer una demo en vivo.