"""Second migration

Revision ID: afd40e3c3760
Revises: ba6061d88289
Create Date: 2023-11-25 23:06:36.505418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afd40e3c3760'
down_revision: Union[str, None] = 'ba6061d88289'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    regions_table = op.create_table(
        'regions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
    )

    op.bulk_insert(
        regions_table,
        [
            {'id': 1, 'name': 'Магаданская область'},
            {'id': 2, 'name': 'Республика Дагестан'}
        ]
    )


    op.add_column('users', sa.Column('region_id', sa.Integer, sa.ForeignKey('regions.id')))

    op.execute("""
        UPDATE users
        SET region_id = 1 WHERE id = 1
            
    """)

    op.execute("""
        UPDATE users
        SET region_id = 1 WHERE id = 2
            
    """)


def downgrade() -> None:
    op.drop_column('users', 'region_id')

    op.drop_table('regions')