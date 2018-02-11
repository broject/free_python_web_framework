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
    import app.helpers.model_helper as mh
    mh.upgrade_default_entities(op, sa)


def downgrade():
    import app.helpers.model_helper as mh
    mh.downgrade_default_entities(op)
