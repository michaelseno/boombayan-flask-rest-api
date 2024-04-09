"""empty message

Revision ID: def5ad4a6e62
Revises: a4ffee1eedb5
Create Date: 2024-04-10 00:35:01.986760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'def5ad4a6e62'
down_revision = 'a4ffee1eedb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
        batch_op.alter_column('admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
