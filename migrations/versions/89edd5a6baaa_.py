"""empty message

Revision ID: 89edd5a6baaa
Revises: e007718609ce
Create Date: 2018-03-14 23:21:24.164004

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '89edd5a6baaa'
down_revision = 'e007718609ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('porto_door_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.Column('door_opened', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_porto_door_status_date'), 'porto_door_status', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_porto_door_status_date'), table_name='porto_door_status')
    op.drop_table('porto_door_status')
    # ### end Alembic commands ###