"""empty message

Revision ID: 1c85f6495828
Revises: ffed3e713061
Create Date: 2019-05-12 03:16:56.352165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c85f6495828'
down_revision = 'ffed3e713061'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('questions_content_fem_key', 'questions', type_='unique')
    op.drop_column('questions', 'content_fem')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('content_fem', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.create_unique_constraint('questions_content_fem_key', 'questions', ['content_fem'])
    # ### end Alembic commands ###
