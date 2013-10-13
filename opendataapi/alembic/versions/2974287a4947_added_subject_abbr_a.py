"""Added subject_abbr and subject_full fields, removed subject field

Revision ID: 2974287a4947
Revises: c950627a461
Create Date: 2013-10-12 15:39:13.794608

"""

# revision identifiers, used by Alembic.
revision = '2974287a4947'
down_revision = 'c950627a461'

from alembic import op
import sqlalchemy as sa

def upgrade():
    ### added indexing
    op.add_column('uclass', sa.Column(
        'subject_abbr',
        sa.String(length=120),
        nullable=True,
        index=True,
        ))
    op.add_column('uclass', sa.Column(
        'subject_full',
        sa.String(length=600),
        nullable=True,
        index=True
        ))
    op.drop_column('uclass', u'subject')
    ### end Alembic commands ###

def downgrade():
    ### added indexing
    op.add_column('uclass', sa.Column(
        u'subject',
        sa.VARCHAR(length=600),
        nullable=True,
        index=True,
        ))
    op.drop_column('uclass', 'subject_full')
    op.drop_column('uclass', 'subject_abbr')
    ### end Alembic commands ###
