CREATE TABLE IF NOT EXISTS
    Customers(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `name` VARCHAR(255) NOT NULL,
        `email` VARCHAR(255) NOT NULL,
        `phone` VARCHAR(20) NOT NULL COMMENT 'Customer phone with area code',
        `hash_pwd` VARCHAR(255) NOT NULL COMMENT 'Customer pwd in MD5',
        CONSTRAINT `UC_Customer` UNIQUE (email)
    );

CREATE TABLE IF NOT EXISTS
    Robots(
        `serial_number` VARCHAR(5) NOT NULL PRIMARY KEY
    );

CREATE TABLE IF NOT EXISTS
    Robots_of_customers(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `robot_serial_number` VARCHAR(5) NOT NULL,
        `customer_id` int NOT NULL,
        CONSTRAINT `Robots_of_customers_robot_serial_number__Robot_serial_number` FOREIGN KEY(`robot_serial_number`) REFERENCES Robots(`serial_number`),
        CONSTRAINT `Robots_of_customers_customer_id__Customers_id` FOREIGN KEY(`customer_id`) REFERENCES Customers(`id`)
    );

CREATE TABLE IF NOT EXISTS
    GPS_points(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `quality` int NOT NULL,
        `latitude` DECIMAL(20, 18) NOT NULL,
        `longitude` DECIMAL(20, 18) NOT NULL
    );

CREATE TABLE IF NOT EXISTS
    Fields(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `label` VARCHAR(255) NOT NULL
    );

CREATE TABLE IF NOT EXISTS
    Fields_corners(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `field_id` int NOT NULL,
        `gps_point_id` int NOT NULL,
        CONSTRAINT `Fields_corners_field_id__Fields_id` FOREIGN KEY(`field_id`) REFERENCES Fields(`id`),
        CONSTRAINT `Fields_corners_gps_point_id__GPS_points_id` FOREIGN KEY(`gps_point_id`) REFERENCES GPS_points(`id`)
    );

CREATE TABLE IF NOT EXISTS
    Sessions(
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

CREATE TABLE IF NOT EXISTS
    Vesc_statistics(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `session_id` int NOT NULL,
        `voltage` DECIMAL(5, 2) NOT NULL,
        `timestamp` TIMESTAMP(0) NOT NULL,
        CONSTRAINT `Vesc_statistics_session_id__Sessions_id` FOREIGN KEY(`session_id`) REFERENCES Sessions(`id`)
    );

CREATE TABLE IF NOT EXISTS
    Points_of_paths(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `point_number` int NOT NULL,
        `session_id` int NOT NULL,
        `gps_point_id` int NOT NULL,
        CONSTRAINT `Points_of_paths_session_id__Sessions_id` FOREIGN KEY(`session_id`) REFERENCES Sessions(`id`),
        CONSTRAINT `Points_of_paths_gps_point_id__GPS_points_id` FOREIGN KEY(`gps_point_id`) REFERENCES GPS_points(`id`)
    );

CREATE TABLE IF NOT EXISTS
    Weed_types(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `label` VARCHAR(255) NOT NULL
    );

CREATE TABLE IF NOT EXISTS
    Extracted_weeds(
        `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `point_of_path_id` int NOT NULL,
        `weed_type_id` int NOT NULL,
        `session_id` int NOT NULL,
        `number` int NOT NULL DEFAULT 1,
        CONSTRAINT `Extracted_weeds_session_id__Sessions_id` FOREIGN KEY(`session_id`) REFERENCES Sessions(`id`),
        CONSTRAINT `Extracted_weeds_point_of_path_id__Points_of_paths_id` FOREIGN KEY(`point_of_path_id`) REFERENCES Points_of_paths(`id`),
        CONSTRAINT `Extracted_weeds_weed_type_id__Weed_types_id` FOREIGN KEY(`weed_type_id`) REFERENCES Weed_types(`id`)
    );