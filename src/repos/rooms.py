from src.database import engine
from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from sqlalchemy import select, func


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        """
        with rooms_count as (
	        select room_id, count(*) as rooms_booked from bookings
	        where date_from <= '2024-11-30' and date_to >= '2024-10-02'
	        group by room_id
        ),
        rooms_left_table as (
	        select rooms.id as room_id, quantity, quantity - coalesce(rooms_booked, 0) as room_left
	        from rooms
	        left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where room_left > 0
        ;
        """


        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("room_left")
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_for_hotel")
        )

        rooms_ids_to_get = (
            select(rooms_left_table.c.room.id)
            .filter(rooms_left_table.c.room_left > 0,
                    rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
            )
        )

        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))