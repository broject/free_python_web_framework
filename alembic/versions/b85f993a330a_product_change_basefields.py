"""product_change_basefields

Revision ID: b85f993a330a
Revises: 510b22760a2c
Create Date: 2018-01-18 15:59:23.159895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b85f993a330a'
down_revision = '510b22760a2c'
branch_labels = None
depends_on = None


def upgrade():
    import datetime
    from sqlalchemy import func, text
    op.add_column('product', sa.Column(
        'created', sa.TIMESTAMP, nullable=False,
        server_default=text('CURRENT_TIMESTAMP')))
    op.add_column('product', sa.Column(
        'updated', sa.TIMESTAMP, nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))


def downgrade():
    op.drop_column('product', 'created')
    op.drop_column('product', 'updated')
