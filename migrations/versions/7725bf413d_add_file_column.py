"""add file column

Revision ID: 7725bf413d
Revises: 29ba7ffdd86
Create Date: 2016-06-15 15:28:57.442712

"""

# revision identifiers, used by Alembic.
revision = '7725bf413d'
down_revision = '29ba7ffdd86'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_columns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('file', sa.Column('file_column_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'file_column_id')
    op.drop_table('file_columns')
    ### end Alembic commands ###
