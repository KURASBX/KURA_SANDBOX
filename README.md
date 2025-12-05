**KURA Sandbox – Backend de Validación de Alias**
---
**project: KURA – Sistema Interoperable de Alias**
---
version: 1.0
---
date: 2025-12-05
author: Alias Chile SpA · Área Técnica
status: Interno / Distribución Controlada
---

# KURA Sandbox – Backend de Validación de Alias

KURA Sandbox es el entorno local oficial para pruebas técnicas del sistema de alias interoperable desarrollado por Alias Chile SpA.
Permite validar los flujos de registro, resolución, baja y auditoría encadenada (WORM lógico), operando con una arquitectura modular basada en FastAPI y PostgreSQL.

Este entorno está diseñado para:
- Equipos técnicos internos
- Integradores (bancos / PSP)
- Evaluación preliminar de arquitectura y flujos por parte de terceros

---

## 🚀 Ejecución del Sandbox

### Requisitos

- Docker Desktop activo
- Archivo .env en la raíz con variables mínimas:

# .env
```bash
ENVIRONMENT=production
DB_PASSWORD=<definir>
SECRET_KEY=<definir>
JWT_SECRET=<definir>
```

### Comandos
```bash
docker compose down -v
docker compose up --build
```


### Accesos

👉🏻 Healthcheck: http://localhost:8050/api/health/
👉🏻 Swagger UI: http://localhost:8050/docs

---

## 📁 Estructura del Proyecto


api/ # Endpoints HTTP
application/ # Casos de uso y lógica de aplicación
core/ # Configuración y seguridad
domain/ # Entidades y modelos de dominio
infrastructure/ # Repositorios y capa de persistencia
alembic/ # Migraciones de base de datos
docs/
internal/ # Documentación técnica del proyecto
tenant/ # Guías de integración (bancos / PSP)
regulador/ # Documentación para sandbox regulatorio (CMF / SFA)

---

## 📚 Documentación

### Clientes (Bancos / PSP)

Carpeta: docs/tenant/  
Incluye:
- Manual de integración API
- Ejemplos de request/response
- Especificación funcional mínima

---

### Interna (Arquitectura / Dev)

Carpeta: docs/internal/  
Incluye:
- Arquitectura
- Runbooks
- Documentos heredados del piloto anterior

---

### Regulador (Sandbox CMF/SFA)

Carpeta: docs/regulador/  
Incluye:
- Alcance del sandbox
- Controles Bootstrap (equivalencias ISO/NIST)
- Evidencias WORM
- Diagramas de arquitectura C4

---

## 🛠 Tecnologías

- FastAPI
- PostgreSQL
- Docker Compose
- Alembic
- Python 3.10+

---

## 🏢 Autoría Corporativa

Alias Chile SpA · Proyecto KURA™  
Plataforma RegTech para validación y trazabilidad segura de alias interoperables.  
Contacto: kuraaliaschile@gmail.com
