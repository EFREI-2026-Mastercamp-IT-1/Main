from sqlmodel import Field, SQLModel, create_engine, Session
from enum import Enum

engine = create_engine("data/database.db")


class Stop(SQLModel, table=True):
    stop_id: str = Field(primary_key=True)
    stop_name: str
    stop_lon: float
    stop_lat: float


class StopTime(SQLModel, table=True):
    stop_id: int = Field(foreign_key="stop.stop_id")
    trip_id: int


class Trip(SQLModel, table=True):
    trip_id: int = Field(primary_key=True)
    route_id: int


class Route(SQLModel, table=True):
    class RouteType(Enum):
        TRAMWAY = 0
        METRO = 1
        TRAIN = 2
        BUS = 3
        FUNICULAIRE = 7

    route_id: int = Field(primary_key=True)
    route_type: RouteType


class Transfer(SQLModel, table=True):
    from_stop_id: int = Field(foreign_key="stop.stop_id")
    to_stop_id: int = Field(foreign_key="stop.stop_id")
    min_transfer_time: int


def get_metro_stations() -> list[Stop]:
    with Session(engine) as session:
        stops = session.exec(Stop.select().join(StopTime).join(Trip).join(
            Route).where(Route.route_type == RouteType.metro.value).group_by(Stop.stop_name))
        return stops


def get_metro_pathways() -> list[Transfer]:
    with Session(engine) as session:
        transfers = session.exec(Transfer.select())
        return transfers
