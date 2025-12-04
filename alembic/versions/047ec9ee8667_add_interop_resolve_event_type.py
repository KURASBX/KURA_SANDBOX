"""add_interop_resolve_event_type

Revision ID: 047ec9ee8667
Revises: 7c5214149b81
Create Date: 2025-11-27 16:10:36.757437

"""
from collections.abc import Sequence
from typing import Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "047ec9ee8667"
down_revision: Union[str, None] = "7c5214149b81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE eeventtype ADD VALUE 'INTEROP_RESOLVE'")


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE alias_events 
        ALTER COLUMN eeventtype TYPE VARCHAR;
        
        DROP TYPE eeventtype;
        
        CREATE TYPE eeventtype AS ENUM ('REGISTER', 'RESOLVE', 'DEACTIVATE');
        
        UPDATE alias_events 
        SET eeventtype = 'RESOLVE' 
        WHERE eeventtype = 'INTEROP_RESOLVE';
        
        ALTER TABLE alias_events 
        ALTER COLUMN eeventtype TYPE eeventtype USING eeventtype::eeventtype;
    """
    )
