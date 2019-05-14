"""empty message

Revision ID: ffed3e713061
Revises: 
Create Date: 2019-05-12 03:01:14.232279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ffed3e713061"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=50), nullable=False),
        sa.Column("content_fem", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("content"),
        sa.UniqueConstraint("content_fem"),
    )
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=30), nullable=False),
        sa.Column("passive", sa.String(length=30), nullable=False),
        sa.Column("gif", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("gif"),
        sa.UniqueConstraint("passive"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=30), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("city", sa.String(length=40), nullable=True),
        sa.Column("sex", sa.Boolean(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("birthday", sa.DateTime(), nullable=True),
        sa.Column("instagram", sa.String(length=30), nullable=True),
        sa.Column("vk", sa.String(length=32), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "answers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=40), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "decisions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("hate", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("asker_id", sa.Integer(), nullable=False),
        sa.Column("receiver_id", sa.Integer(), nullable=False),
        sa.Column("accepted", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["asker_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["receiver_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("boy_id", sa.Integer(), nullable=False),
        sa.Column("girl_id", sa.Integer(), nullable=False),
        sa.Column("boy_request_id", sa.Integer(), nullable=False),
        sa.Column("girl_request_id", sa.Integer(), nullable=False),
        sa.Column(
            "date_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["boy_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["boy_request_id"], ["requests.id"]),
        sa.ForeignKeyConstraint(["girl_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["girl_request_id"], ["requests.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "guesses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("correct_id", sa.Integer(), nullable=False),
        sa.Column("answer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["answer_id"], ["answers.id"]),
        sa.ForeignKeyConstraint(["correct_id"], ["answers.id"]),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
        sa.ForeignKeyConstraint(["request_id"], ["requests.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=True),
        sa.Column("correct_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["correct_id"], ["answers.id"]),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("lines")
    op.drop_table("guesses")
    op.drop_table("contacts")
    op.drop_table("requests")
    op.drop_table("decisions")
    op.drop_table("answers")
    op.drop_table("users")
    op.drop_table("topics")
    op.drop_table("questions")
    # ### end Alembic commands ###
