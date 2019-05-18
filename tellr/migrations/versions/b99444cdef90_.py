"""empty message

Revision ID: b99444cdef90
Revises: 
Create Date: 2019-05-18 21:15:45.566854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b99444cdef90"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("avatar_big", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "avatar_big")
    # ### end Alembic commands ###
