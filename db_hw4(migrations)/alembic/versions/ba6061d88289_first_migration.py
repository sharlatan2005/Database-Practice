"""First migration

Revision ID: ba6061d88289
Revises: 9f18cf25e2ae
Create Date: 2023-11-25 22:53:35.714533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba6061d88289'
down_revision: Union[str, None] = '9f18cf25e2ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('surname', sa.String(), nullable=True))
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))

    # Обновление новых столбцов на основе существующего поля FIO
    op.execute("""
        UPDATE users
        SET surname = split_part(users.fio, ' ', 1),
            name = split_part(users.fio, ' ', 2),
            last_name = split_part(users.fio, ' ', 3)
    """)

    # Удаление столбца FIO
    op.drop_column('users', 'fio')


def downgrade() -> None:
    op.add_column('users', sa.Column('fio', sa.String()))

    # Обновление столбца FIO на основе новых столбцов
    op.execute("""
        UPDATE users
        SET fio = coalesce(surname || ' ' || name || ' ' || last_name, '')
    """)

    # Удаление новых столбцов
    op.drop_column('users', 'name')
    op.drop_column('users', 'surname')
    op.drop_column('users', 'last_name')
