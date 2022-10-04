"""empty message

Revision ID: d386be743749
Revises: 2ec30b1a6dab
Create Date: 2022-10-03 15:00:10.056364

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd386be743749'
down_revision = '2ec30b1a6dab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendence', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('attendence', 'num')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendence', sa.Column('num', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('attendence', 'id')
    # ### end Alembic commands ###
