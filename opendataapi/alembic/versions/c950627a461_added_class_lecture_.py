"""Added class lecture tables

Revision ID: c950627a461
Revises: None
Create Date: 2013-10-06 16:56:25.313809

"""

# revision identifiers, used by Alembic.
revision = 'c950627a461'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    # manually added indexing
    op.create_table('uclass',
            sa.Column('id', sa.String(length=64), nullable=False),
            sa.Column('term', sa.String(length=64), nullable=True),
            sa.Column(
                'subject',
                sa.String(length=600),
                nullable=True,
                index=True
                ),
            sa.Column(
                'name',
                sa.String(length=600),
                nullable=False,
                index=True
                ),
            sa.Column(
                'number',
                sa.String(length=120),
                nullable=True,
                index=True
                ),
            sa.Column('last_updated', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
            )
    # manually added indexing
    op.create_table('lecture',
            sa.Column('uclass', sa.String(length=64), nullable=False),
            sa.Column('sec_num', sa.String(length=64), nullable=False),
            sa.Column('start_time', sa.DateTime(), nullable=True),
            sa.Column('end_time', sa.DateTime(), nullable=True),
            sa.Column('days', sa.String(length=64), nullable=True),
            sa.Column('credits', sa.String(length=64), nullable=True),
            sa.Column('class_type', sa.String(length=64), nullable=True),
            sa.Column(
                'classnum',
                sa.String(length=64),
                nullable=True,
                index=True,
                ),
            sa.Column(
                'mode',
                sa.String(length=600),
                nullable=True,
                index=True,
                ),
            sa.Column('instructors',
                sa.String(length=600),
                nullable=True,
                index=True,
                ),
            sa.Column('location', sa.String(length=120), nullable=True),
            sa.Column('last_updated', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['uclass'], ['uclass.id'], ),
            sa.PrimaryKeyConstraint('uclass', 'sec_num')
            )
    ### end Alembic commands ###

def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lecture')
    op.drop_table('uclass')
    ### end Alembic commands ###