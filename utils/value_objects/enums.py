import enum


class AliasStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"


class TenantRole(str, enum.Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"


class TenantType(str, enum.Enum):
    BANK = "BANK"
    ADMIN = "ADMIN"
    PARTNER = "PARTNER"


class TenantStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING = "PENDING"


class EEventType(str, enum.Enum):
    REGISTER = "REGISTER"
    RESOLVE = "RESOLVE"
    DEACTIVATE = "DEACTIVATE"
    INTEROP_RESOLVE = "INTEROP_RESOLVE"


class EAccountType(str, enum.Enum):
    CTA_VISTA = "CTA_VISTA"
    CTA_CORRIENTE = "CTA_CORRIENTE"
    CTA_AHORRO = "CTA_AHORRO"
    CTA_PLATINUM = "CTA_PLATINUM"


class EQueryType(str, enum.Enum):
    """Tipos de consultas de interoperabilidad"""

    GLOBAL_VALIDATION = "GLOBAL_VALIDATION"  # Validación global de alias
    CROSS_TENANT_LOOKUP = "CROSS_TENANT_LOOKUP"  # Búsqueda específica cross-tenant
    ROUTING_RESOLUTION = "ROUTING_RESOLUTION"  # Resolución de ruteo bancario
    COMPLIANCE_CHECK = "COMPLIANCE_CHECK"  # Verificación de cumplimiento
    FRAUD_VALIDATION = "FRAUD_VALIDATION"  # Validación antifraude
