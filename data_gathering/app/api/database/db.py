import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        DECIMAL as Decimal, UniqueConstraint, ForeignKeyConstraint, Enum)
from app.api.database.enum.robot_monitoring import RobotMonitoring
from app.api.database.enum.robot_synthesis import RobotSynthesis
from app.api.database.enum.role import Role

from databases import Database, DatabaseURL

DATABASE_URI = os.getenv('DATABASE_URI')

metadata = MetaData()

"""
CREATE TABLE
    IF NOT EXISTS Customers(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `name` VARCHAR(255) NOT NULL,
        `email` VARCHAR(255) NOT NULL,
        `phone` VARCHAR(20) NOT NULL COMMENT 'Customer phone with area code',
        `hash_pwd` VARCHAR(255) NOT NULL COMMENT 'Customer pwd in MD5',
        `hash_rt` VARCHAR(255) NULL COMMENT 'Customer token in MD5',
        `role` ENUM ('ADMIN','DISTRIBUTOR','USER') NOT NULL COMMENT 'Customer role',
        CONSTRAINT `UC_Customer` UNIQUE (email)
    );
"""
customers = Table(
    'Customers',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('email', String(255), nullable=False),
    Column('phone', String(20), nullable=False),
    Column('hash_pwd', String(255), nullable=False),
    Column('hash_rt', String(255), nullable=True),
    Column('role', Enum(Role)),
    UniqueConstraint('email', name='UC_Customer'),
)

"""
CREATE TABLE
    IF NOT EXISTS Robots_of_subscribers(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `robot_serial_number` VARCHAR(5) NOT NULL,
        `subscriber_username` VARCHAR(255) NOT NULL,
        `role` ENUM ('ADMIN','DISTRIBUTOR','USER') NOT NULL,
        CONSTRAINT `Robots_of_subscribers_robot_serial_number__Robot_serial_number` FOREIGN KEY(`robot_serial_number`) REFERENCES Robots(`serial_number`),
    );
"""
robots_of_subscribers = Table(
    'Robots_of_subscribers',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('robot_serial_number', String(5), nullable=False),
    Column('subscriber_username', String(255), nullable=False),
    Column('role', Enum(Role), default=Role.USER),
    ForeignKeyConstraint(["robot_serial_number"], [
                         "Robots.serial_number"], name="Robots_of_subscribers_robot_serial_number__Robot_serial_number")
)


"""
CREATE TABLE
    IF NOT EXISTS Robots_of_customers(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `robot_serial_number` VARCHAR(5) NOT NULL,
        `customer_id` int NOT NULL,
        CONSTRAINT `Robots_of_customers_robot_serial_number__Robot_serial_number` FOREIGN KEY(`robot_serial_number`) REFERENCES Robots(`serial_number`),
        CONSTRAINT `Robots_of_customers_customer_id__Customers_id` FOREIGN KEY(`customer_id`) REFERENCES Customers(`id`)
    );
"""

robots_of_customers = Table(
    'Robots_of_customers',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('robot_serial_number', String(5), nullable=False),
    Column('customer_id', Integer(), nullable=False),
    ForeignKeyConstraint(["robot_serial_number"], [
                         "Robots.serial_number"], name="Robots_of_customers_robot_serial_number__Robot_serial_number"),
    ForeignKeyConstraint(["customer_id"], [
                         "Customers.id"], name="Robots_of_customers_customer_id__Customers_id")
)

"""
CREATE TABLE
IF NOT EXISTS Robots_monitoring(
    'id' int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `heartbeat_timestamp` datetime NOT NULL,
    'robot_monitoring' enum ('BLOCKING_PAGE_1_TO_2', 'BLOCKING_DURING_OPERATION') NOT NULL,
    `robot_serial_number` VARCHAR(5) NOT NULL,
    CONSTRAINT `Robots_monitoring_robot_serial_number__Robot_serial_number` FOREIGN KEY(`robot_serial_number`) REFERENCES Robots(`serial_number`)
);
"""
robots_monitoring = Table(
    'Robots_monitoring',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('heartbeat_timestamp', DateTime, nullable=False),
    Column('robot_monitoring', Enum(RobotMonitoring), nullable=False),
    Column('robot_serial_number', String(5), nullable=False),
    ForeignKeyConstraint(["robot_serial_number"], [
                         "Robots.serial_number"], name="Robots_monitoring_robot_serial_number__Robot_serial_number")
)

"""
CREATE TABLE
IF NOT EXISTS Robots_synthesis(
    'id' int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `heartbeat_timestamp` datetime NOT NULL,
    'robot_synthesis' enum ('OP', 'HS', 'ANTI_THEFT') NOT NULL,
    `robot_serial_number` VARCHAR(5) NOT NULL,
    CONSTRAINT `Robots_synthesis_robot_serial_number__Robot_serial_number` FOREIGN KEY(`robot_serial_number`) REFERENCES Robots(`serial_number`)
);
"""
robots_synthesis = Table(
    'Robots_synthesis',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('heartbeat_timestamp', DateTime, nullable=False),
    Column('robot_synthesis', Enum(RobotSynthesis), nullable=False),
    Column('robot_serial_number', String(5), nullable=False),
    ForeignKeyConstraint(["robot_serial_number"], [
                         "Robots.serial_number"], name="Robots_synthesis_robot_serial_number__Robot_serial_number")
)

"""
CREATE TABLE
IF NOT EXISTS Robots(
    `serial_number` VARCHAR(5) NOT NULL PRIMARY KEY
);
"""
robots = Table(
    'Robots',
    metadata,
    Column('serial_number', String(5), primary_key=True,
           index=True)
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
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('quality', Integer, nullable=False),
    Column('latitude', Decimal(20, 18), nullable=False),
    Column('longitude', Decimal(20, 18), nullable=False)
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
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('label', String(255), nullable=False),
    Column('robot_serial_number', String(5), nullable=False),
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
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('field_id', Integer, nullable=False),
    Column('gps_point_id', Integer, nullable=False),
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
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('start_time', DateTime, nullable=False),
    Column('end_time', DateTime, nullable=False),
    Column('field_id', Integer, nullable=False),
    Column('robot_serial_number', String(5), nullable=False),
    Column('previous_sessions_id', Integer, nullable=True),
    ForeignKeyConstraint(["previous_sessions_id"], ["Sessions.id"],
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
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('session_id', Integer, nullable=False),
    Column('voltage', Decimal(5, 2), nullable=False),
    Column('timestamp', DateTime, nullable=False),
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
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('point_number', Integer, nullable=False),
    Column('session_id', Integer, nullable=False),
    Column('gps_point_id', Integer, nullable=False),
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
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('point_of_path_id', Integer, nullable=False),
    Column('weed_type_id', Integer, nullable=False),
    Column('session_id', Integer, nullable=False),
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
        `label` VARCHAR(255) NOT NULL,
        CONSTRAINT `UC_Weed_types` UNIQUE (label)
    );
"""
weed_types = Table(
    'Weed_types',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('label', String(255), nullable=False),
    UniqueConstraint('label', name='UC_Weed_types')
)

database = Database(DATABASE_URI)

database_url = DatabaseURL(DATABASE_URI)
