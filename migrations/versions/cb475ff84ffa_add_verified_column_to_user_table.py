"""Add verified column to User table

Revision ID: cb475ff84ffa
Revises: 
Create Date: 2023-09-09 22:46:47.832573

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import expression

# revision identifiers, used by Alembic.
revision = 'cb475ff84ffa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profile')
    op.drop_table('user')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verified', sa.Boolean(), nullable=True, server_default=expression.false()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('verified')

    op.create_table('user',
                    sa.Column('user_id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
                    sa.Column('password_hash', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('user_id', name='user_pkey')
                    )
    op.create_table('user_profile',
                    sa.Column('profile_id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('first_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('last_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('full_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
                    sa.Column('date_of_birth', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('profile_picture', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
                    sa.Column('other_profile_info', postgresql.JSON(astext_type=sa.Text()), autoincrement=False,
                              nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_profile_user_id_fkey'),
                    sa.PrimaryKeyConstraint('profile_id', name='user_profile_pkey'),
                    sa.UniqueConstraint('user_id', name='user_profile_user_id_key')
                    )

    # ### end Alembic commands ###
