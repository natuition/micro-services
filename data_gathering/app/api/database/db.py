import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        DECIMAL as Decimal)

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

metadata = MetaData()

fields = Table(
    'Fields',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('label', String(255))
)

robots = Table(
    'Robots',
    metadata,
    Column('serial_number', String(5), primary_key=True)
)

sessions = Table(
    'Sessions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('start_time', DateTime),
    Column('end_time', DateTime),
    Column('field_id', Integer),
    Column('robot_serial_number', String(5)),
    Column('previous_sessions_id', Integer, nullable=True)
)

fields_corners = Table(
    'Fields_corners',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('field_id', Integer),
    Column('gps_point_id', Integer)
)

gps_points = Table(
    'GPS_points',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('quality', Integer),
    Column('latitude', Decimal(20, 18)),
    Column('longitude', Decimal(20, 18))
)

points_of_paths = Table(
    'Points_of_paths',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('point_number', Integer),
    Column('session_id', Integer),
    Column('gps_point_id', Integer)
)

extracted_weeds = Table(
    'Extracted_weeds',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('point_of_path_id', Integer),
    Column('weed_type_id', Integer),
    Column('session_id', Integer),
    Column('number', Integer)
)

vesc_statistics = Table(
    'Vesc_statistics',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('session_id', Integer),
    Column('voltage', Decimal(5, 2)),
    Column('timestamp', DateTime)
)

weed_types = Table(
    'Weed_types',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('label', String(255))
)

database = Database(DATABASE_URI)
