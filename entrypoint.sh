#!/bin/bash

set -e

echo "🚀 Iniciando entrypoint..."

# Configuración
DB_HOST=${DB_HOST:-postgres}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}
DB_NAME=${DB_NAME:-kura}
DB_PASSWORD=${DB_PASSWORD}

echo "🔧 Configuración de Base de Datos:"
echo "   Host: $DB_HOST | Puerto: $DB_PORT | Usuario: $DB_USER | Base: $DB_NAME"

# Verificar que tenemos las variables críticas
if [ -z "$DB_PASSWORD" ]; then
    echo "❌ ERROR: DB_PASSWORD no está definida"
    exit 1
fi

# Esperar PostgreSQL
echo "⏳ Esperando a PostgreSQL..."
max_attempts=30
attempt=1

until PGPASSWORD=$DB_PASSWORD pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" >/dev/null 2>&1; do
    if [ $attempt -eq $max_attempts ]; then
        echo "❌ PostgreSQL no está disponible después de $max_attempts intentos"
        exit 1
    fi
    echo "📦 PostgreSQL no está listo aún... intento $attempt/$max_attempts"
    sleep 5
    attempt=$((attempt + 1))
done
echo "✅ PostgreSQL listo"

# Verificar configuración de Alembic
if [ ! -f "alembic.ini" ]; then
    echo "❌ ERROR: alembic.ini no encontrado"
    ls -la
    exit 1
fi

if [ ! -f "alembic/env.py" ]; then
    echo "❌ ERROR: alembic/env.py no encontrado"
    ls -la alembic/ 2>/dev/null || echo "Directorio alembic no existe"
    exit 1
fi

# Configurar la URL de la base de datos en alembic.ini
echo "🔧 Configurando Alembic..."
sed -i "s|sqlalchemy.url =.*|sqlalchemy.url = postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME|" alembic.ini

# Asegurar que la carpeta versions existe
mkdir -p alembic/versions

# Función para verificar si existe una tabla
check_table_exists() {
    local table_name=$1
    PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = '$table_name'
    );" | grep -q "t"
}

# Determinar el estado de la base de datos
echo "📊 Verificando estado de la base de datos..."

if check_table_exists "alembic_version"; then
    echo "📋 Base de datos con migraciones existentes"
    echo "🔄 Aplicando migraciones pendientes..."
    alembic upgrade head
elif check_table_exists "alias_registries"; then
    echo "⚠️  Tablas existentes sin migraciones"
    echo "🔄 Generando migración baseline..."
    alembic revision --autogenerate -m "Baseline from existing schema"
    alembic upgrade head
else
    echo "🆕 Base de datos vacía"
    echo "📝 Ejecutando migración inicial..."
    alembic upgrade head
fi

echo "✅ Base de datos lista"
echo "🎉 Iniciando aplicación..."
exec uvicorn main:app --host 0.0.0.0 --port 8000