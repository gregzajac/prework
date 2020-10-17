"""books table

Revision ID: 04173cfb636c
Revises: c6e57afbaa08
Create Date: 2020-10-16 12:38:57.439689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04173cfb636c'
down_revision = 'c6e57afbaa08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('isbn', sa.BigInteger(), nullable=False),
    sa.Column('number_of_pages', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###