"""Update Transaction model with optional source and category fields

Revision ID: b7c1e2fa95c4
Revises: 
Create Date: 2025-03-14 23:36:12.566373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7c1e2fa95c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=50), nullable=True))
        batch_op.alter_column('source',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.alter_column('source',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.drop_column('category')

    # ### end Alembic commands ###
