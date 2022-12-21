import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        DECIMAL as Decimal, UniqueConstraint, ForeignKeyConstraint)

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

metadata = MetaData()

"""
CREATE TABLE
IF NOT EXISTS Robots(
    `serial_number` VARCHAR(5) NOT NULL PRIMARY KEY
);
"""
robots = Table(
    'Robots',
    metadata,
    Column('serial_number', String(5), primary_key=True, index=True)
)

"""
CREATE TABLE
    IF NOT EXISTS GPS_points(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `quality` int NOT NULL,
        `latitude` DECIMAL(20, 18) NOT NULL,
        `longitude` DECIMAL(20, 18) NOT NULL
    );
"""
gps_points = Table(
    'GPS_points',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('quality', Integer),
    Column('latitude', Decimal(20, 18)),
    Column('longitude', Decimal(20, 18))
)

"""
CREATE TABLE
    IF NOT EXISTS Fields(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `label` VARCHAR(255) NOT NULL,
        `robot_serial_number` VARCHAR(5) NOT NULL,
        CONSTRAINT `Fields_robot_serial_number__Robot_serial_number` FOREIGN KEY(`robot_serial_number`) REFERENCES Robots(`serial_number`),
        CONSTRAINT `UC_Fields` UNIQUE (label, robot_serial_number)
    );
"""
fields = Table(
    'Fields',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('label', String(255)),
    Column('robot_serial_number', String(5)),
    UniqueConstraint('label', 'robot_serial_number', name='UC_Fields'),
    ForeignKeyConstraint(
        ["robot_serial_number"], ["Robots.serial_number"], name="Fields_robot_serial_number__Robot_serial_number")
)

"""
CREATE TABLE
    IF NOT EXISTS Fields_corners(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `field_id` int NOT NULL,
        `gps_point_id` int NOT NULL,
        CONSTRAINT `Fields_corners_field_id__Fields_id` FOREIGN KEY(`field_id`) REFERENCES Fields(`id`),
        CONSTRAINT `Fields_corners_gps_point_id__GPS_points_id` FOREIGN KEY(`gps_point_id`) REFERENCES GPS_points(`id`)
    );
"""
fields_corners = Table(
    'Fields_corners',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('field_id', Integer),
    Column('gps_point_id', Integer),
    ForeignKeyConstraint(["field_id"], ["Fields.id"],
                         name="Fields_corners_field_id__Fields_id"),
    ForeignKeyConstraint(["gps_point_id"], ["GPS_points.id"],
                         name="Fields_corners_gps_point_id__GPS_points_id")
)

"""
CREATE TABLE
    IF NOT EXISTS Sessions(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `start_time` TIMESTAMP(0) NOT NULL,
        `end_time` TIMESTAMP(0) NOT NULL,
        `previous_sessions_id` int NULL,
        `robot_serial_number` VARCHAR(5) NOT NULL,
        `field_id` int NOT NULL,
        CONSTRAINT `Sessions_previous_sessions_id__Sessions_id` FOREIGN KEY(`previous_sessions_id`) REFERENCES Sessions(`id`),
        CONSTRAINT `Sessions_robot_serial_number__Robot_serial_number` FOREIGN KEY(`robot_serial_number`) REFERENCES Robots(`serial_number`),
        CONSTRAINT `Sessions_field_id__Fields_id` FOREIGN KEY(`field_id`) REFERENCES Fields(`id`)
    );
"""
sessions = Table(
    'Sessions',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('start_time', DateTime),
    Column('end_time', DateTime),
    Column('field_id', Integer),
    Column('robot_serial_number', String(5)),
    Column('previous_sessions_id', Integer, nullable=True),
    ForeignKeyConstraint(["id"], ["Sessions.id"],
                         name="Sessions_previous_sessions_id__Sessions_id", ondelete="CASCADE", use_alter=True),
    ForeignKeyConstraint(["field_id"], ["Fields.id"],
                         name="Sessions_field_id__Fields_id"),
    ForeignKeyConstraint(["robot_serial_number"], [
                         "Robots.serial_number"], name="Sessions_robot_serial_number__Robot_serial_number")
)

"""
CREATE TABLE
    IF NOT EXISTS Vesc_statistics(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `session_id` int NOT NULL,
        `voltage` DECIMAL(5, 2) NOT NULL,
        `timestamp` TIMESTAMP(0) NOT NULL,
        CONSTRAINT `Vesc_statistics_session_id__Sessions_id` FOREIGN KEY(`session_id`) REFERENCES Sessions(`id`)
    );
"""
vesc_statistics = Table(
    'Vesc_statistics',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('session_id', Integer),
    Column('voltage', Decimal(5, 2)),
    Column('timestamp', DateTime),
    ForeignKeyConstraint(["session_id"], ["Sessions.id"],
                         name="Vesc_statistics_session_id__Sessions_id")
)

"""
CREATE TABLE
    IF NOT EXISTS Points_of_paths(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `point_number` int NOT NULL,
        `session_id` int NOT NULL,
        `gps_point_id` int NOT NULL,
        CONSTRAINT `Points_of_paths_session_id__Sessions_id` FOREIGN KEY(`session_id`) REFERENCES Sessions(`id`),
        CONSTRAINT `Points_of_paths_gps_point_id__GPS_points_id` FOREIGN KEY(`gps_point_id`) REFERENCES GPS_points(`id`)
    );
"""
points_of_paths = Table(
    'Points_of_paths',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('point_number', Integer),
    Column('session_id', Integer),
    Column('gps_point_id', Integer),
    ForeignKeyConstraint(["session_id"], ["Sessions.id"],
                         name="Points_of_paths_session_id__Sessions_id"),
    ForeignKeyConstraint(["gps_point_id"], ["GPS_points.id"],
                         name="Points_of_paths_gps_point_id__GPS_points_id")
)

"""
CREATE TABLE
    IF NOT EXISTS Extracted_weeds(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `point_of_path_id` int NOT NULL,
        `weed_type_id` int NOT NULL,
        `session_id` int NOT NULL,
        `number` int NOT NULL DEFAULT 1,
        CONSTRAINT `Extracted_weeds_session_id__Sessions_id` FOREIGN KEY(`session_id`) REFERENCES Sessions(`id`),
        CONSTRAINT `Extracted_weeds_point_of_path_id__Points_of_paths_id` FOREIGN KEY(`point_of_path_id`) REFERENCES Points_of_paths(`id`),
        CONSTRAINT `Extracted_weeds_weed_type_id__Weed_types_id` FOREIGN KEY(`weed_type_id`) REFERENCES Weed_types(`id`)
    );
"""
extracted_weeds = Table(
    'Extracted_weeds',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('point_of_path_id', Integer),
    Column('weed_type_id', Integer),
    Column('session_id', Integer),
    Column('number', Integer),
    ForeignKeyConstraint(["point_of_path_id"], ["Points_of_paths.id"],
                         name="Extracted_weeds_point_of_path_id__Points_of_paths_id"),
    ForeignKeyConstraint(["weed_type_id"], ["Weed_types.id"],
                         name="Extracted_weeds_weed_type_id__Weed_types_id"),
    ForeignKeyConstraint(["session_id"], ["Sessions.id"],
                         name="Extracted_weeds_session_id__Sessions_id")
)

"""
CREATE TABLE
    IF NOT EXISTS Weed_types(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `label` VARCHAR(255) NOT NULL
    );
"""
weed_types = Table(
    'Weed_types',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('label', String(255))
)

database = Database(DATABASE_URI)
