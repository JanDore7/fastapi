"""room_id вместо rooms_id

Revision ID: b79c592b1f8f
Revises: 667f15fbc4c8
Create Date: 2024-11-18 02:04:46.457182

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b79c592b1f8f"
down_revision: Union[str, None] = "667f15fbc4c8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "rooms_facilities", sa.Column("room_id", sa.BIGINT(), nullable=False)
    )
    op.drop_constraint(
        "rooms_facilities_rooms_id_fkey",
        "rooms_facilities",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None, "rooms_facilities", "rooms", ["room_id"], ["id"]
    )
    op.drop_column("rooms_facilities", "rooms_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "rooms_facilities",
        sa.Column(
            "rooms_id", sa.BIGINT(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        "rooms_facilities_rooms_id_fkey",
        "rooms_facilities",
        "rooms",
        ["rooms_id"],
        ["id"],
    )
    op.drop_column("rooms_facilities", "room_id")
    # ### end Alembic commands ###
