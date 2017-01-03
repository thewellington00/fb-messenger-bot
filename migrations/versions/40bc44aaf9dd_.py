"""empty message

Revision ID: 40bc44aaf9dd
Revises: 201626a58dfd
Create Date: 2017-01-02 18:22:33.100981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40bc44aaf9dd'
down_revision = '201626a58dfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('last_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fb_uid', sa.Integer(), nullable=True),
    sa.Column('last_user_message', sa.Unicode(), nullable=True),
    sa.Column('last_bot_response', sa.Unicode(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('last_message')
    # ### end Alembic commands ###
