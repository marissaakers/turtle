"""empty message

Revision ID: f39f2d282d5e
Revises: c02957d2cb8a
Create Date: 2020-03-26 00:51:04.046414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f39f2d282d5e'
down_revision = 'c02957d2cb8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'encounter', ['filename'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'encounter', type_='unique')
    # ### end Alembic commands ###