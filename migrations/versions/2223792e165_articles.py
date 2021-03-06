"""articles

Revision ID: 2223792e165
Revises: 13d42a02406
Create Date: 2016-03-19 21:58:27.811507

"""

# revision identifiers, used by Alembic.
revision = '2223792e165'
down_revision = '13d42a02406'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_article_timestamp'), 'article', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_article_timestamp'), table_name='article')
    op.drop_table('article')
    ### end Alembic commands ###
