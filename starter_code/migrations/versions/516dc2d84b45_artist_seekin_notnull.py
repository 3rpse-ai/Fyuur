"""Artist Seekin NotNull

Revision ID: 516dc2d84b45
Revises: 8bdfcebe8afc
Create Date: 2020-09-08 09:56:02.348740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '516dc2d84b45'
down_revision = '8bdfcebe8afc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###