"""init

Revision ID: 33064e9f1f15
Revises: 
Create Date: 2018-02-05 17:16:37.532599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33064e9f1f15'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('product',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(150), nullable=False),
                    sa.Column('barcode', sa.String(128), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    import app.helpers.model_helper as mh
    mh.upgrade_base_columns('product', op, sa)


def downgrade():
    op.drop_table('product')
