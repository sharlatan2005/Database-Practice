"""Zero migration

Revision ID: 9f18cf25e2ae
Revises: 
Create Date: 2023-11-25 21:54:59.389550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table

# revision identifiers, used by Alembic.
revision: str = '9f18cf25e2ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users_table = op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('fio', sa.String, nullable=False),
        sa.Column('address', sa.String),
        sa.Column('sex', sa.String, nullable=False),
    )

    op.bulk_insert(
        users_table,
        [
            {'id': 1, 'fio': 'Байден Джо Владимирович', 'address': 'Пермь', 'sex': 'Ж'},
            {'id': 2, 'fio': 'Мамонтов Михаил Романович', 'address': '456 Elm St', 'sex': 'М'}
        ]
    )

def downgrade() -> None:
    op.drop_table('users')
