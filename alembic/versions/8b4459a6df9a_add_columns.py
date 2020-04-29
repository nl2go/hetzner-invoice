"""Add columns

Revision ID: 8b4459a6df9a
Revises: 9e667ecbb5e7
Create Date: 2020-04-24 10:31:04.087955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8b4459a6df9a"
down_revision = "9e667ecbb5e7"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("invoices", sa.Column("invoice_nr", sa.String(11)))
    op.add_column("invoices", sa.Column("last_updated", sa.DateTime))
    pass


def downgrade():
    op.drop_column("invoices", "invoice_nr")
    op.drop_column("invoices", "last_updated")
    pass
