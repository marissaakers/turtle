"""empty message

Revision ID: cb0e239aa405
Revises: 98a49495dea2
Create Date: 2020-04-23 13:57:32.250287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb0e239aa405'
down_revision = '98a49495dea2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offshore_encounter', sa.Column('entered_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offshore_encounter', 'entered_date')
    # ### end Alembic commands ###
