# flake8: noqa
"""create invoice table

Revision ID: 9e667ecbb5e7
Revises: 
Create Date: 2020-02-13 15:57:26.798710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9e667ecbb5e7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "invoices",
        sa.Column("type", sa.Text),
        sa.Column("description", sa.Text),
        sa.Column("start_date", sa.Text),
        sa.Column("end_date", sa.Text),
        sa.Column("quantity", sa.Integer),
        sa.Column("unit_price", sa.Integer),
        sa.Column("price", sa.Integer),
        sa.Column("role", sa.Text),
        sa.Column("id", sa.String(8)),
        sa.Column("environment", sa.Text),
        sa.Column("cores", sa.Integer),
        sa.Column("memory", sa.Integer),
        sa.Column("disk", sa.Integer),
        sa.Column("price_monthly", sa.Integer),
    )
    pass


def downgrade():
    op.drop_table("invoice")
    pass
