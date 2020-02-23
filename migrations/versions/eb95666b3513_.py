"""empty message

Revision ID: eb95666b3513
Revises: 3527b03f33f5
Create Date: 2020-02-15 18:40:41.679208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb95666b3513'
down_revision = '3527b03f33f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('beach_encounter', sa.Column('location_detail', sa.String(length=150), nullable=True))
    op.drop_column('beach_encounter', 'location')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('beach_encounter', sa.Column('location', sa.REAL(), autoincrement=False, nullable=True))
    op.drop_column('beach_encounter', 'location_detail')
    # ### end Alembic commands ###