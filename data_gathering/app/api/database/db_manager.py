from app.api.models.field import FieldIn, FieldOut, FieldWithGPSPoints
from app.api.models.robot import RobotIn, RobotOut
from app.api.models.session import SessionIn, SessionOut, SessionUpdate
from app.api.models.extracted_weed import ExtractedWeedIn, ExtractedWeedOut
from app.api.models.field_corner import FieldCornerIn, FieldCornerOut
from app.api.models.gps_point import GPSPointIn, GPSPointOut
from app.api.models.point_of_path import PointOfPathIn, PointOfPathOut
from app.api.models.vesc_statistic import VescStatisticIn, VescStatisticOut
from app.api.models.weed_type import WeedTypeIn, WeedTypeOut
from app.api.models.robot_status import RobotStatusInDB, RobotStatusOutDB
from app.api.models.robot_subscriber import RobotSubscriberIn, RobotSubscriberOut
from app.api.models.robot_monitoring import RobotMonitoringInDB, RobotMonitoringOutDB
from app.api.models.report import ReportOut, ExtractedWeedWithGPSPointWithWeedTypeOut
from app.api.models.robot_of_customer import RobotOfCustomerIn, RobotOfCustomerOut, RobotOfCustomerInForm
from app.api.models.customer import CustomerIn, CustomerOut
from app.api.database.db import fields, robots, sessions, fields_corners, gps_points, points_of_paths, extracted_weeds, vesc_statistics, weed_types, robots_synthesis, robots_monitoring, database, database_url, robots_of_subscribers, robots_of_customers, customers
from sqlalchemy import desc, select

# --- Field ---

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


async def get_field_of_session(session_id: int) -> FieldWithGPSPoints:
    session_query = sessions.select().where(sessions.c.id == session_id)
    res_session: SessionOut= await database.fetch_one(query=session_query)

    field_query = fields.select().where(fields.c.id == res_session.field_id)
    res_field: FieldOut= await database.fetch_one(query=field_query)

    fields_corners_gps_points_query = gps_points.select().join(fields_corners, gps_points.c.id == fields_corners.c.gps_point_id).where(fields_corners.c.field_id == res_field.id)
    res_fields_corners_gps_points: list[GPSPointOut] = await database.fetch_all(query=fields_corners_gps_points_query)

    return {
        "session": res_session,
        "field": res_field,
        "fields_corners": res_fields_corners_gps_points
    }

# --- Subscriber ---

async def add_subscriber_of_robot(payload: RobotSubscriberIn):
    query = robots_of_subscribers.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_subscriber_with_robot() -> list[RobotSubscriberOut]:
    query = robots_of_subscribers.select()
    return await database.fetch_all(query=query)


async def get_all_robot_of_one_subscriber(subscriber_username: str) -> list[RobotOut]:
    query = robots.select() \
    .join(robots_of_subscribers, robots.c.serial_number == robots_of_subscribers.c.robot_serial_number) \
    .where(robots_of_subscribers.c.subscriber_username == subscriber_username)
    return await database.fetch_all(query=query)


async def remove_one_robot_of_one_subscriber(subscriber_username: str, robot_serial_number: str):
    query = robots_of_subscribers.delete() \
    .where((robots_of_subscribers.c.subscriber_username == subscriber_username) & (robots_of_subscribers.c.robot_serial_number == robot_serial_number) )
    return await database.execute(query=query)

# --- Robot of customer administration ---

async def add_one_robot_of_one_customer(payload: RobotOfCustomerInForm):
    query = select(customers.c.id) .where(customers.c.email == payload.customer_email)
    customers_id = await database.fetch_one(query=query)
    customers_id = customers_id[0]
    
    query = robots_of_customers.select().where((robots_of_customers.c.customer_id == customers_id) & (robots_of_customers.c.robot_serial_number == payload.robot_serial_number))
    exist = await database.fetch_one(query=query)
    
    if exist is None:
        query = robots_of_customers.insert().values(robot_serial_number=payload.robot_serial_number, customer_id=customers_id)
        robot_customer_id = await database.execute(query=query)
        return {
            "robot_serial_number" : payload.robot_serial_number,
            "id" : robot_customer_id,
            "customer_id" : customers_id
        }
    return {
        "id" : exist[0],
        "robot_serial_number" : exist[1],
        "customer_id" : exist[2]
    }

async def get_all_customer_with_robot() -> list[RobotOfCustomerOut]:
    query = robots_of_customers.select()
    return await database.fetch_all(query=query)

# --- Robot ---

async def add_robot(payload: RobotIn):
    query = robots.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_robots() -> list[RobotOut]:
    query = robots.select()
    return await database.fetch_all(query=query)

# --- Session ---

async def add_session(payload: SessionIn):
    query = sessions.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_sessions() -> list[SessionOut]:
    query = sessions.select()
    return await database.fetch_all(query=query)


async def get_all_sessions_of_robot(robot_sn: str) -> list[SessionOut]:
    query = sessions.select().where(sessions.c.robot_serial_number == robot_sn).order_by(desc(sessions.c.start_time))
    return await database.fetch_all(query=query)


async def get_last_session_of_robot(robot_sn: str) -> SessionOut:
    query = sessions.select().where(sessions.c.robot_serial_number == robot_sn).order_by(desc(sessions.c.start_time))
    return await database.fetch_one(query=query)


async def get_last_10_sessions_of_robot_with_offset(robot_sn: str, offset: int = 0) -> list[SessionOut]:
    query = sessions.select().where(sessions.c.robot_serial_number == robot_sn).order_by(desc(sessions.c.start_time)).limit(10).offset(offset)
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

# --- ExtractedWeed ---

async def add_extracted_weed(payload: ExtractedWeedIn):
    query = extracted_weeds.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_extracted_weeds() -> list[ExtractedWeedOut]:
    query = extracted_weeds.select()
    return await database.fetch_all(query=query)


async def get_all_extracted_weeds_of_session(session_id: int) -> list[ExtractedWeedOut]:
    query = extracted_weeds.select().where(extracted_weeds.c.session_id == session_id)
    return await database.fetch_all(query=query)

# --- FieldCorner ---

async def add_field_corner(payload: FieldCornerIn):
    query = fields_corners.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_fields_corners() -> list[FieldCornerOut]:
    query = fields_corners.select()
    return await database.fetch_all(query=query)


async def get_field_corners(field_id : int) -> list[FieldCornerOut]:
    query = fields_corners.select().where(fields_corners.c.field_id == field_id)
    return await database.fetch_all(query=query)

# --- GPSPoint ---

async def add_gps_point(payload: GPSPointIn):
    query = gps_points.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_gps_points() -> list[GPSPointOut]:
    query = gps_points.select()
    return await database.fetch_all(query=query)

async def get_gps_point(gps_point_id : int) -> GPSPointOut:
    query = gps_points.select().where(gps_points.c.id == gps_point_id)
    return await database.fetch_all(query=query)

# --- PointOfPath ---

async def add_point_of_path(payload: PointOfPathIn):
    query = points_of_paths.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_points_of_paths() -> list[PointOfPathOut]:
    query = points_of_paths.select()
    return await database.fetch_all(query=query)


async def get_all_points_of_path_of_session(session_id: int) -> list[PointOfPathOut]:
    query = points_of_paths.select().where(points_of_paths.c.session_id == session_id)
    return await database.fetch_all(query=query)

# --- VescStatistic ---

async def add_vesc_statistic(payload: VescStatisticIn):
    query = vesc_statistics.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_vesc_statistics() -> list[VescStatisticOut]:
    query = vesc_statistics.select()
    return await database.fetch_all(query=query)


async def get_last_vesc_statistic_of_session(session_id: int) -> VescStatisticOut:
    query = vesc_statistics.select().where(vesc_statistics.c.session_id == session_id).order_by(desc(vesc_statistics.c.timestamp))
    return await database.fetch_one(query=query)

# --- WeedType ---

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

# --- Admin ---

async def deletion_of_all_data_from_the_database():
    await database.execute("SET foreign_key_checks = 0")
    query = f"SELECT Concat('TRUNCATE TABLE ', TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='{database_url.database}'"
    truncates = await database.fetch_all(query=query)
    for truncate in truncates:
        await database.execute(truncate[0])
    await database.execute("SET foreign_key_checks = 0")

# --- RobotStatus ---

async def add_robot_synthesis(payload: RobotStatusInDB):
    query = robots_synthesis.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_robot_synthesis(serial_number: str) -> RobotStatusOutDB:
    query = robots_synthesis.select().where(
        robots_synthesis.c.robot_serial_number == serial_number).order_by(desc(robots_synthesis.c.heartbeat_timestamp))
    return await database.fetch_one(query=query)

# --- RobotMonitoring ---

async def add_robot_monitoring(payload: RobotMonitoringInDB):
    query = robots_monitoring.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_robot_monitoring(serial_number: str) -> RobotMonitoringOutDB:
    query = robots_monitoring.select().where(
        robots_monitoring.c.robot_serial_number == serial_number).order_by(desc(robots_monitoring.c.heartbeat_timestamp))
    return await database.fetch_one(query=query)

# --- Report ---

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

# --- Customer ---

async def add_customer(payload: CustomerIn):
    query = customers.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_customers() -> list[CustomerOut]:
    query = customers.select()
    return await database.fetch_all(query=query)