# Hexagonal Architecture - Alias API

## Overview

This API implements the **Hexagonal Architecture** (Ports & Adapters) pattern to create a maintainable, testable, and flexible system for alias management between banks.

## Architecture Principles

### Core Concepts

- **Domain Layer**: Pure business logic, no external dependencies
- **Application Layer**: Orchestrates domain objects, implements use cases  
- **Infrastructure Layer**: Technical implementations, external adapters
- **Dependency Rule**: Dependencies point inward → Domain knows nothing about external world

### Project Structure

src/
├── domain/                          # Business Core - Most Important
│   ├── entities/                    # Business entities with behavior
│   │   ├── alias_registry_entity.py
│   │   ├── alias_event_entity.py
│   │   ├── global_alias_entity.py
│   │   ├── interop_audit_entity.py
│   │   ├── tenant_entity.py
│   │   └── error_log_entity.py
│   ├── repositories/                # Interfaces (Ports) - WHAT we can do
│   │   ├── __init__.py
│   │   ├── base.py                  # IBaseRepository
│   │   ├── alias.py                 # IAliasRepository, IAliasEventRepository
│   │   ├── global_alias.py          # IGlobalAliasRepository  
│   │   ├── interop_audit.py         # IInteropAuditRepository
│   │   ├── tenant.py                # ITenantRepository
│   │   └── error_log.py             # IErrorLogRepository
│   └── services/                    # Domain services - Complex business logic
│       ├── __init__.py
│       ├── bank_routing_service.py
│       ├── digital_signature_service.py
│       ├── hash_chain_service.py
│       ├── interop_service.py
│       └── jwt_validation_service.py
├── application/                     # Use Cases & Coordination
│   ├── dtos/                        # Data transfer objects
│   │   ├── __init__.py
│   │   ├── alias.py                 # AliasCreate, AliasResponse, etc.
│   │   ├── tenant.py                # TenantCreate, TenantResponse, etc.
│   │   ├── worm.py                  # WormEvidenceResponse, etc.
│   │   └── commands_queries.py      # Commands and Queries
│   └── use_cases/                   # Application services - HOW we do things
│       ├── __init__.py
│       ├── alias/                   # Alias-related use cases
│       │   ├── register_alias.py
│       │   ├── resolve_alias.py
│       │   ├── deactivate_alias.py
│       │   ├── get_alias_event_history.py
│       │   └── verify_hash_chain.py
│       ├── tenant/                  # Tenant-related use cases
│       │   ├── create_tenant.py
│       │   ├── get_tenant.py
│       │   ├── update_tenant.py
│       │   ├── activate_tenant.py
│       │   ├── authenticate_tenant.py
│       │   └── generate_api_key.py
│       ├── worm/                    # WORM evidence use case
│       │   └── generate_worm_evidence.py
│       └── error_log/               # Error logging use case
│           └── error_log_service.py
├── infrastructure/                  # Technical Implementation
│   ├── database/                    # PostgreSQL adapters
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # BaseModel
│   │   │   ├── alias_registry.py    # AliasRegistryModel
│   │   │   ├── alias_event.py       # AliasEventModel
│   │   │   ├── global_alias.py      # GlobalAliasModel
│   │   │   ├── interop_audit.py     # InteropAuditModel
│   │   │   ├── tenant.py            # TenantModel
│   │   │   └── error_log.py         # ErrorLogModel
│   │   └── repositories/            # Repository implementations (Adapters)
│   │       ├── __init__.py
│   │       ├── base.py              # BaseSQLRepository
│   │       ├── alias.py             # AliasRepository, AliasEventRepository
│   │       ├── global_alias.py      # GlobalAliasRepository
│   │       ├── interop_audit.py     # InteropAuditRepository
│   │       ├── tenant.py            # TenantRepository
│   │       └── error_log.py         # ErrorLogRepository
│   └── security/                    # JWT configuration
│       └── jwt.py                   # get_jwt_validation_service
├── api/                             # FastAPI Layer
│   ├── __init__.py
│   ├── routers.py                   # Router configuration
│   ├── alias_router.py
│   ├── tenant_router.py
│   └── health_router.py
├── core/                            # Cross-cutting concerns
│   ├── __init__.py
│   ├── config.py                    # Settings and configuration
│   ├── database.py                  # Database session and engine
│   ├── auth/                        # Authentication dependencies
│   │   ├── __init__.py
│   │   └── dependencies.py          # get_current_tenant, etc.
│   ├── middleware/                  # HTTP middleware
│   │   ├── __init__.py
│   │   ├── logging.py               # LoggingMiddleware
│   │   └── error_handler.py         # http_error_handler_middleware
│   └── utils/                       # Shared utilities
│       ├── __init__.py
│       ├── messages.py              # MESSAGES, enums
│       └── logging_utils.py         # log_execution_time, etc.
└── main.py                          # FastAPI app initialization


## Key Components

### Domain Layer

**Entities**: `AliasRegistryEntity`, `AliasEventEntity`
- Contain business rules and validation
- Pure Python objects, no framework dependencies

**Repositories (Ports)**: `IAliasRepository`, `IAliasEventRepository`  
- Define WHAT operations are possible
- Interfaces only, no implementation

**Services**: `HashChainService`, `JWTValidationService`
- Complex business logic that doesn't fit in entities
- Stateless operations

### Application Layer

**Use Cases**: `RegisterAliasUseCase`, `ResolveAliasUseCase`, `DeactivateAliasUseCase`
- Orchestrate domain objects to fulfill business use cases
- Transaction boundaries
- Input/output validation with DTOs

### Infrastructure Layer

**Adapters**: `AliasRepository`, `AliasEventRepository`, FastAPI endpoints
- Implement domain interfaces for specific technologies
- Know about PostgreSQL, FastAPI, etc.

## Data Flow
HTTP Request
→ FastAPI Endpoint (Infrastructure)
→ Use Case (Application)
→ Domain Entities & Services (Domain)
→ Repository Adapter (Infrastructure)
→ PostgreSQL Database


## Dependency Injection

We use dependency injection to:
- Decouple components
- Enable easy testing
- Switch implementations (e.g., MySQL for PostgreSQL)

## Testing Strategy

- **Domain Layer**: Unit tests with no mocks
- **Application Layer**: Unit tests with mocked repositories  
- **Infrastructure Layer**: Integration tests
- **End-to-End**: API tests with test database

## Benefits

- **Testability**: Each layer can be tested in isolation
- **Maintainability**: Business rules are centralized and clear
- **Flexibility**: Easy to change databases, frameworks, or APIs
- **Team Scaling**: Different teams can work on different layers

## Cross-Cutting Concerns

### Security Implementation
- **JWT Authentication**: Tenant-scoped tokens with role claims
- **API Key Rotation**: Secure key generation and one-time exposure
- **CORS Configuration**: Controlled cross-origin access
- **Input Validation**: Pydantic models for all DTOs

### Audit & Compliance
- **Hash Chain Service**: Cryptographic audit trail integrity
- **WORM Evidence**: Regulatory compliance with digital signatures
- **Error Logging**: Structured logging with correlation IDs
- **Interop Auditing**: Cross-tenant query tracking

### Database Design
- **Soft Delete**: Logical deletion with timestamps
- **Index Strategy**: Optimized for alias resolution queries
- **Foreign Keys**: Referential integrity across tenants
- **Enum Types**: PostgreSQL native enums for status fields

### Performance Considerations
- **Connection Pooling**: SQLAlchemy queue pool for database connections
- **Normalized Aliases**: Case-insensitive search optimization
- **Selective Indexing**: Balanced read/write performance
- **Caching Strategy**: Future Redis integration for hot data

## Deployment & Operations

### Environment Configuration
- **12-Factor App**: Environment-based configuration
- **Feature Flags**: Controlled rollout of new features
- **Health Checks**: Readiness and liveness endpoints
- **Metrics**: Structured logging for operational insights

### Scaling Strategy
- **Stateless Design**: Horizontal scaling capability
- **Database Partitioning**: Tenant-based data separation
- **Async Operations**: Background processing for audit tasks
- **Circuit Breakers**: Resilience for external dependencies