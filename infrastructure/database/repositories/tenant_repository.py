from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.tenant_entity import TenantEntity, TenantStatus, TenantType
from domain.repositories.tenant_repository import ITenantRepository
from infrastructure.database.models import TenantModel
from infrastructure.database.repositories.base_sql_repository import BaseSQLRepository
from utils.value_objects.enums import TenantRole


class TenantRepository(BaseSQLRepository[TenantEntity, TenantModel], ITenantRepository):
    def __init__(self, db: Session):
        super().__init__(db, TenantModel)

    def find_by_code(self, code: str) -> Optional[TenantEntity]:
        db_tenant = self.db.query(self.model).filter(self.model.code == code).first()
        return self._to_entity(db_tenant) if db_tenant else None

    def find_by_email(self, email: str) -> Optional[TenantEntity]:
        db_tenant = (
            self.db.query(self.model).filter(self.model.contact_email == email).first()
        )
        return self._to_entity(db_tenant) if db_tenant else None

    def find_by_tax_id(self, tax_id: str) -> Optional[TenantEntity]:
        db_tenant = (
            self.db.query(self.model).filter(self.model.tax_id == tax_id).first()
        )
        return self._to_entity(db_tenant) if db_tenant else None

    def find_active_tenants(self) -> list[TenantEntity]:
        db_tenants = (
            self.db.query(self.model)
            .filter(self.model.status == TenantStatus.ACTIVE)
            .all()
        )
        return [self._to_entity(tenant) for tenant in db_tenants]

    def find_tenants_by_type(self, tenant_type: TenantType) -> list[TenantEntity]:
        db_tenants = (
            self.db.query(self.model).filter(self.model.type == tenant_type).all()
        )
        return [self._to_entity(tenant) for tenant in db_tenants]

    def update_status(self, tenant_id: UUID, status: TenantStatus) -> bool:
        db_tenant = self.db.query(self.model).filter(self.model.id == tenant_id).first()
        if not db_tenant:
            return False

        db_tenant.status = status
        self.db.commit()
        return True

    def _to_entity(self, db_tenant: TenantModel) -> Optional[TenantEntity]:
        if not db_tenant:
            return None

        roles_raw = db_tenant.roles

        roles_converted = []
        if roles_raw:
            if (
                isinstance(roles_raw, str)
                and roles_raw.startswith("{")
                and roles_raw.endswith("}")
            ):
                roles_cleaned = roles_raw[1:-1]
                if roles_cleaned:
                    role_strings = [
                        role.strip().upper() for role in roles_cleaned.split(",")
                    ]
                    for role_str in role_strings:
                        try:
                            roles_converted.append(TenantRole[role_str])
                        except KeyError:
                            continue
            elif isinstance(roles_raw, list):
                for role_item in roles_raw:
                    if isinstance(role_item, str):
                        try:
                            roles_converted.append(TenantRole[role_item.upper()])
                        except KeyError:
                            continue
                    else:
                        roles_converted.append(role_item)

        return TenantEntity(
            id=db_tenant.id,
            name=db_tenant.name,
            code=db_tenant.code,
            type=db_tenant.type,
            contact_email=db_tenant.contact_email,
            contact_phone=db_tenant.contact_phone,
            website=db_tenant.website,
            legal_name=db_tenant.legal_name,
            tax_id=db_tenant.tax_id,
            status=db_tenant.status,
            tenant_metadata=db_tenant.tenant_metadata or {},
            roles=roles_converted,
            created_at=db_tenant.created_at,
            updated_at=db_tenant.updated_at,
        )

    def create(self, entity: TenantEntity) -> TenantEntity:
        """Override para manejar el enum correctamente"""
        entity_dict = entity.model_dump()

        db_model = self.model(**entity_dict)
        self.db.add(db_model)
        self.db.commit()
        self.db.refresh(db_model)
        return self._to_entity(db_model)
