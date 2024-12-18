"""Adding new features

Revision ID: 743872ce2f16
Revises: 99103eb844c1
Create Date: 2024-11-22 22:59:16.310673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '743872ce2f16'
down_revision = '99103eb844c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
