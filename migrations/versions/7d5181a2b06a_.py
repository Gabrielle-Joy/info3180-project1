"""empty message

Revision ID: 7d5181a2b06a
Revises: fbbf34a51474
Create Date: 2020-03-14 15:24:58.567521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d5181a2b06a'
down_revision = 'fbbf34a51474'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profiles', sa.Column('file_location', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profiles', 'file_location')
    # ### end Alembic commands ###
