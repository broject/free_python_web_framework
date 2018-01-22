"""product_fields_add

Revision ID: e9856e3b595b
Revises: a0964724bad9
Create Date: 2018-01-22 10:21:42.582244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9856e3b595b'
down_revision = 'b85f993a330a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('product',
                  sa.Column('barcode', sa.String(255), index=True))


def downgrade():
    op.drop_column('product', 'barcode')
