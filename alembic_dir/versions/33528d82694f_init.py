"""init

Revision ID: 33528d82694f
Revises: 
Create Date: 2017-08-31 13:14:37.749071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33528d82694f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=20), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('hash_password', sa.VARCHAR(length=128), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('email'),
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('view_num', sa.Integer(), nullable=False, server_default=b'0'),
    sa.Column('title', sa.VARCHAR(length=64), nullable=True),
    sa.Column('slug', sa.VARCHAR(length=200), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('html', sa.Text(), nullable=True),
    sa.Column('markdown', sa.Text(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], )
    )
    op.create_index(op.f('ix_articles_create_time'), 'articles', ['created_time'], unique=False)
    op.create_index(op.f('ix_articles_update_time'), 'articles', ['update_time'], unique=False)
    op.create_index(op.f('ix_articles_title'), 'articles', ['title'], unique=False)
    op.create_index(op.f('ix_articles_slug'), 'articles', ['slug'], unique=False)
    op.create_index(op.f('ix_user_username'), 'users', ['username'], unique=False)
    op.create_index(op.f('ix_user_email'), 'users', ['email'], unique=False)


def downgrade():
    pass

