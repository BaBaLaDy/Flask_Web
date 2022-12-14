"""empty message

Revision ID: f9ab36fa2a39
Revises: d766e9a91aa8
Create Date: 2022-10-03 14:34:24.795389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ab36fa2a39'
down_revision = 'd766e9a91aa8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendence', sa.Column('num', sa.Integer(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('attendence', 'num')
    # ### end Alembic commands ###
