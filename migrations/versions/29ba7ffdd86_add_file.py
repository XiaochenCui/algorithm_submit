"""add file

Revision ID: 29ba7ffdd86
Revises: ca3cb361d4
Create Date: 2016-06-13 12:00:56.621059

"""

# revision identifiers, used by Alembic.
revision = '29ba7ffdd86'
down_revision = 'ca3cb361d4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=64), nullable=True),
    sa.Column('path', sa.Unicode(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    ### end Alembic commands ###
