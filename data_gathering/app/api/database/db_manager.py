from app.api.models.field import FieldIn, FieldOut
from app.api.models.robot import RobotIn, RobotOut
from app.api.models.session import SessionIn, SessionOut
from app.api.models.extracted_weed import ExtractedWeedIn, ExtractedWeedOut
from app.api.models.field_corner import FieldCornerIn, FieldCornerOut
from app.api.models.gps_point import GPSPointIn, GPSPointOut
from app.api.models.point_of_path import PointOfPathIn, PointOfPathOut
from app.api.models.vesc_statistic import VescStatisticIn, VescStatisticOut
from app.api.models.weed_type import WeedTypeIn, WeedTypeOut
from app.api.database.db import fields, robots, sessions, fields_corners, gps_points, points_of_paths, extracted_weeds, vesc_statistics, weed_types, database


async def add_field(payload: FieldIn):
    query = fields.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_fields() -> list[FieldOut]:
    query = fields.select()
    return await database.fetch_all(query=query)


async def get_field(payload: FieldIn) -> FieldOut:
    query = fields.select().where(
        (fields.c.label == payload.label) & (fields.c.robot_serial_number == payload.robot_serial_number))
    return await database.fetch_one(query=query)


async def add_robot(payload: RobotIn):
    query = robots.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_robots() -> list[RobotOut]:
    query = robots.select()
    return await database.fetch_all(query=query)


async def add_session(payload: SessionIn):
    query = sessions.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_sessions() -> list[SessionOut]:
    query = sessions.select()
    return await database.fetch_all(query=query)


async def add_extracted_weed(payload: ExtractedWeedIn):
    query = extracted_weeds.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_extracted_weeds() -> list[ExtractedWeedOut]:
    query = extracted_weeds.select()
    return await database.fetch_all(query=query)


async def add_field_corner(payload: FieldCornerIn):
    query = fields_corners.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_fields_corners() -> list[FieldCornerOut]:
    query = fields_corners.select()
    return await database.fetch_all(query=query)


async def add_gps_point(payload: GPSPointIn):
    query = gps_points.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_gps_points() -> list[GPSPointOut]:
    query = gps_points.select()
    return await database.fetch_all(query=query)


async def add_point_of_path(payload: PointOfPathIn):
    query = points_of_paths.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_points_of_paths() -> list[PointOfPathOut]:
    query = points_of_paths.select()
    return await database.fetch_all(query=query)


async def add_vesc_statistic(payload: VescStatisticIn):
    query = vesc_statistics.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_vesc_statistics() -> list[VescStatisticOut]:
    query = vesc_statistics.select()
    return await database.fetch_all(query=query)


async def add_weed_type(payload: WeedTypeIn):
    query = weed_types.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_weed_types() -> list[WeedTypeOut]:
    query = weed_types.select()
    return await database.fetch_all(query=query)
