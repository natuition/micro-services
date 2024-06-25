from app.api.models.field import FieldIn, FieldOut
from app.api.models.robot import RobotIn, RobotOut
from app.api.models.session import SessionIn, SessionOut, SessionUpdate
from app.api.models.extracted_weed import ExtractedWeedIn, ExtractedWeedOut
from app.api.models.field_corner import FieldCornerIn, FieldCornerOut
from app.api.models.gps_point import GPSPointIn, GPSPointOut
from app.api.models.point_of_path import PointOfPathIn, PointOfPathOut
from app.api.models.vesc_statistic import VescStatisticIn, VescStatisticOut
from app.api.models.weed_type import WeedTypeIn, WeedTypeOut
from app.api.models.robot_status import RobotStatusInDB, RobotStatusOutDB
from app.api.models.robot_monitoring import RobotMonitoringInDB, RobotMonitoringOutDB
from app.api.models.report import ReportOut, ExtractedWeedWithGPSPointWithWeedTypeOut
from app.api.database.db import fields, robots, sessions, fields_corners, gps_points, points_of_paths, extracted_weeds, vesc_statistics, weed_types, robots_synthesis, robots_monitoring, database, database_url
from sqlalchemy import desc, select


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


async def get_session(id: int) -> SessionOut:
    query = sessions.select().where(sessions.c.id == id)
    return await database.fetch_one(query=query)


async def update_session(id: int, payload: SessionUpdate):
    query = (
        sessions
        .update()
        .where(id == sessions.c.id)
        .values(**payload.dict(exclude_unset=True))
    )
    await database.fetch_one(query=query)


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


async def get_weed_type(payload: WeedTypeIn) -> WeedTypeOut:
    query = weed_types.select().where(
        weed_types.c.label == payload.label)
    return await database.fetch_one(query=query)


async def deletion_of_all_data_from_the_database():
    await database.execute("SET foreign_key_checks = 0")
    query = f"SELECT Concat('TRUNCATE TABLE ', TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='{database_url.database}'"
    truncates = await database.fetch_all(query=query)
    for truncate in truncates:
        await database.execute(truncate[0])
    await database.execute("SET foreign_key_checks = 0")


async def add_robot_synthesis(payload: RobotStatusInDB):
    query = robots_synthesis.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_robot_synthesis(serial_number: str) -> RobotStatusOutDB:
    query = robots_synthesis.select().where(
        robots_synthesis.c.robot_serial_number == serial_number).order_by(desc(robots_synthesis.c.heartbeat_timestamp))
    return await database.fetch_one(query=query)


async def add_robot_monitoring(payload: RobotMonitoringInDB):
    query = robots_monitoring.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_robot_monitoring(serial_number: str) -> RobotMonitoringOutDB:
    query = robots_monitoring.select().where(
        robots_monitoring.c.robot_serial_number == serial_number).order_by(desc(robots_monitoring.c.heartbeat_timestamp))
    return await database.fetch_one(query=query)


async def get_report_data_one_session(session_id: int) -> ReportOut:
    session_query = sessions.select().where(sessions.c.id == session_id)
    res_session: SessionOut= await database.fetch_one(query=session_query)

    extracted_weed_with_GPS_point_with_weed_type_query = select(gps_points.c.latitude, gps_points.c.longitude, extracted_weeds.c.number, weed_types.c.label)\
        .join(points_of_paths, points_of_paths.c.id == extracted_weeds.c.point_of_path_id)\
        .join(weed_types, weed_types.c.id == extracted_weeds.c.weed_type_id)\
        .join(gps_points, gps_points.c.id == points_of_paths.c.gps_point_id)\
        .where(extracted_weeds.c.session_id == res_session.id)
    res_extracted_weed_with_GPS_point_with_weed_type: list[ExtractedWeedWithGPSPointWithWeedTypeOut] = await database.fetch_all(query=extracted_weed_with_GPS_point_with_weed_type_query)

    points_of_paths_gps_points_query = gps_points.select().join(points_of_paths, gps_points.c.id == points_of_paths.c.gps_point_id).where(points_of_paths.c.session_id == res_session.id)
    res_points_of_paths_gps_points: GPSPointOut = await database.fetch_all(query=points_of_paths_gps_points_query)

    field_query = fields.select().where(fields.c.id == res_session.field_id)
    res_field: FieldOut= await database.fetch_one(query=field_query)

    fields_corners_gps_points_query = gps_points.select().join(fields_corners, gps_points.c.id == fields_corners.c.gps_point_id).where(fields_corners.c.field_id == res_field.id)
    res_fields_corners_gps_points: GPSPointOut = await database.fetch_all(query=fields_corners_gps_points_query)

    return {
        "session": res_session,
        "extracted_weed_with_GPS_point_with_weed_type": res_extracted_weed_with_GPS_point_with_weed_type,
        "points_of_paths": res_points_of_paths_gps_points,
        "field": res_field,
        "fields_corners": res_fields_corners_gps_points
    }