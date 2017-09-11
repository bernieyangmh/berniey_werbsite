"""add feedback

Revision ID: 9bef54205461
Revises: 33528d82694f
Create Date: 2017-09-10 21:39:40.240977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bef54205461'
down_revision = '33528d82694f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('user_name', sa.VARCHAR(64), nullable=False, server_default="anonymous"),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_feedback_user_name'), 'feedback', ['user_name'], unique=False)


def downgrade():
    pass
