"""create table product

Revision ID: 510b22760a2c
Revises: 
Create Date: 2018-01-18 12:23:52.170013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '510b22760a2c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('product')
