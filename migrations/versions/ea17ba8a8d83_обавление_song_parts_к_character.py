"""обавление song_parts к Character

Revision ID: ea17ba8a8d83
Revises: f6cc8ce1c87c
Create Date: 2024-05-23 01:42:21.770147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea17ba8a8d83'
down_revision = 'f6cc8ce1c87c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('song_parts', sa.Integer(), nullable=True))
        batch_op.drop_column('attacks_needed')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('attacks_needed', sa.INTEGER(), nullable=True))
        batch_op.drop_column('song_parts')

    # ### end Alembic commands ###
