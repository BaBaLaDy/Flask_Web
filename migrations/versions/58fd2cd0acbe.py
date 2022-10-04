"""empty message

Revision ID: 58fd2cd0acbe
Revises: c847a2e66983
Create Date: 2022-10-03 16:43:31.209108

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '58fd2cd0acbe'
down_revision = 'c847a2e66983'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendence',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('course_name', sa.String(length=50), nullable=True),
    sa.Column('attendance_state', sa.String(length=50), nullable=False),
    sa.Column('attendance_time', sa.String(length=50), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('lessons_time', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['course_name'], ['course.course_name'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('attendencetable')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendencetable',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('course_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('attendance_state', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('attendance_time', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('student_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lessons_time', mysql.VARCHAR(length=50), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name='attendencetable_ibfk_1'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='attendencetable_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('attendence')
    # ### end Alembic commands ###