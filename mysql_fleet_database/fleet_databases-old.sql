-- MySQL dump 10.13  Distrib 8.0.30, for Linux (aarch64)

--

-- Host: localhost    Database: fleet

-- ------------------------------------------------------

-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */

;

/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */

;

/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */

;

/*!50503 SET NAMES utf8mb4 */

;

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */

;

/*!40103 SET TIME_ZONE='+00:00' */

;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */

;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */

;

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */

;

/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */

;

--

-- Table structure for table `Customers`

--

DROP TABLE IF EXISTS `Customers`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Customers` (
        `id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        `email` varchar(255) NOT NULL,
        `phone` varchar(20) NOT NULL COMMENT 'Customer phone with area code',
        `hash_pwd` varchar(255) NOT NULL COMMENT 'Customer pwd in MD5',
        PRIMARY KEY (`id`),
        UNIQUE KEY `UC_Customer` (`email`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Customers`

--

LOCK TABLES `Customers` WRITE;

/*!40000 ALTER TABLE `Customers` DISABLE KEYS */

;

INSERT INTO `Customers`
VALUES (
        1,
        'Vladimir',
        'v.modylevskii@natuition.com',
        '+33601020304',
        '5f4dcc3b5aa765d61d8327deb882cf99'
    ), (
        2,
        'Vincent',
        'v.lambert@natuition.com',
        '+33605060708',
        '5f4dcc3b5aa765d61d8327deb882cf99'
    );

/*!40000 ALTER TABLE `Customers` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Extracted_weeds`

--

DROP TABLE IF EXISTS `Extracted_weeds`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Extracted_weeds` (
        `id` int NOT NULL AUTO_INCREMENT,
        `point_of_path_id` int NOT NULL,
        `weed_type_id` int NOT NULL,
        `number` int NOT NULL DEFAULT 1,
        PRIMARY KEY (`id`),
        KEY `Extracted_weeds_point_of_path_id__Points_of_paths_id` (`point_of_path_id`),
        KEY `Extracted_weeds_weed_type_id__Weed_types_id` (`weed_type_id`),
        CONSTRAINT `Extracted_weeds_point_of_path_id__Points_of_paths_id` FOREIGN KEY (`point_of_path_id`) REFERENCES `Points_of_paths` (`id`),
        CONSTRAINT `Extracted_weeds_weed_type_id__Weed_types_id` FOREIGN KEY (`weed_type_id`) REFERENCES `Weed_types` (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 7 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Extracted_weeds`

--

LOCK TABLES `Extracted_weeds` WRITE;

/*!40000 ALTER TABLE `Extracted_weeds` DISABLE KEYS */

;

INSERT INTO `Extracted_weeds`
VALUES (2, 731, 1, 1), (3, 731, 2, 3), (4, 740, 3, 2), (5, 750, 4, 6), (6, 770, 2, 10);

/*!40000 ALTER TABLE `Extracted_weeds` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Fields`

--

DROP TABLE IF EXISTS `Fields`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Fields` (
        `id` int NOT NULL AUTO_INCREMENT,
        `label` varchar(255) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Fields`

--

LOCK TABLES `Fields` WRITE;

/*!40000 ALTER TABLE `Fields` DISABLE KEYS */

;

INSERT INTO `Fields` VALUES (1,'Field1'),(2,'Field2'),(3,'Field3');

/*!40000 ALTER TABLE `Fields` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Fields_corners`

--

DROP TABLE IF EXISTS `Fields_corners`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Fields_corners` (
        `id` int NOT NULL AUTO_INCREMENT,
        `field_id` int NOT NULL,
        `gps_point_id` int NOT NULL,
        PRIMARY KEY (`id`),
        KEY `Fields_corners_field_id__Fields_id` (`field_id`),
        KEY `Fields_corners_gps_point_id__GPS_points_id` (`gps_point_id`),
        CONSTRAINT `Fields_corners_field_id__Fields_id` FOREIGN KEY (`field_id`) REFERENCES `Fields` (`id`),
        CONSTRAINT `Fields_corners_gps_point_id__GPS_points_id` FOREIGN KEY (`gps_point_id`) REFERENCES `GPS_points` (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 13 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Fields_corners`

--

LOCK TABLES `Fields_corners` WRITE;

/*!40000 ALTER TABLE `Fields_corners` DISABLE KEYS */

;

INSERT INTO `Fields_corners`
VALUES (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), (5, 2, 5), (6, 2, 6), (7, 2, 7), (8, 2, 8), (9, 3, 9), (10, 3, 10), (11, 3, 11), (12, 3, 12);

/*!40000 ALTER TABLE `Fields_corners` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `GPS_points`

--

DROP TABLE IF EXISTS `GPS_points`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `GPS_points` (
        `id` int NOT NULL AUTO_INCREMENT,
        `quality` int NOT NULL,
        `latitude` decimal(20, 18) DEFAULT NULL,
        `longitude` decimal(20, 18) DEFAULT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 2842 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `GPS_points`

--

LOCK TABLES `GPS_points` WRITE;

/*!40000 ALTER TABLE `GPS_points` DISABLE KEYS */

;

INSERT INTO `GPS_points`
VALUES (
        1,
        4,
        46.157598702772680000,
        -1.134768798405673000
    ), (
        2,
        4,
        46.157412412473484000,
        -1.134596522779060900
    ), (
        3,
        4,
        46.157296465276690000,
        -1.134857835921499400
    ), (
        4,
        4,
        46.157482755625495000,
        -1.135030112862389400
    ), (
        5,
        4,
        50.598099505740926000,
        3.247232303422537000
    ), (
        6,
        4,
        50.598389333326956000,
        3.246859617955771000
    ), (
        7,
        4,
        50.598526583555750000,
        3.247124529450245000
    ), (
        8,
        4,
        50.598236756080304000,
        3.247497213049189000
    ), (
        9,
        4,
        52.347036175000035000,
        4.946393412501553000
    ), (
        10,
        4,
        52.347199234544700000,
        4.946140023165029000
    ), (
        11,
        5,
        52.347318859510956000,
        4.946346311432701000
    ), (
        12,
        2,
        52.347155800000000000,
        4.946599700000001000
    ), (
        2802,
        4,
        46.157586200000000000,
        -1.134749200000000000
    ), (
        2803,
        4,
        46.157586200000000000,
        -1.134749200000000000
    ), (
        2804,
        4,
        46.157584200000000000,
        -1.134747500000000000
    ), (
        2805,
        4,
        46.157583800000000000,
        -1.134747200000000000
    ), (
        2806,
        4,
        46.157582700000000000,
        -1.134746200000000000
    ), (
        2807,
        4,
        46.157582700000000000,
        -1.134746200000000000
    ), (
        2808,
        4,
        46.157581300000000000,
        -1.134745000000000000
    ), (
        2809,
        4,
        46.157580200000000000,
        -1.134743800000000000
    ), (
        2810,
        4,
        46.157578800000000000,
        -1.134742800000000000
    ), (
        2811,
        4,
        46.157577500000000000,
        -1.134741700000000000
    ), (
        2812,
        4,
        46.157576000000000000,
        -1.134740500000000000
    ), (
        2813,
        4,
        46.157574500000000000,
        -1.134739300000000000
    ), (
        2814,
        4,
        46.157573300000000000,
        -1.134738500000000000
    ), (
        2815,
        4,
        46.157573300000000000,
        -1.134738500000000000
    ), (
        2816,
        4,
        46.157571700000000000,
        -1.134737200000000000
    ), (
        2817,
        4,
        46.157571700000000000,
        -1.134737200000000000
    ), (
        2818,
        4,
        46.157570200000000000,
        -1.134736000000000000
    ), (
        2819,
        4,
        46.157569000000000000,
        -1.134735300000000000
    ), (
        2820,
        4,
        46.157567500000000000,
        -1.134734300000000000
    ), (
        2821,
        4,
        46.157566000000000000,
        -1.134733300000000000
    ), (
        2822,
        4,
        50.598236300000000000,
        3.247471000000000000
    ), (
        2823,
        4,
        50.598235000000000000,
        3.247471000000000000
    ), (
        2824,
        4,
        50.598233700000000000,
        3.247470500000000000
    ), (
        2825,
        4,
        50.598232300000000000,
        3.247470200000000000
    ), (
        2826,
        4,
        50.598231000000000000,
        3.247469500000000000
    ), (
        2827,
        4,
        50.598229800000000000,
        3.247468500000000000
    ), (
        2828,
        4,
        50.598228500000000000,
        3.247467300000000000
    ), (
        2829,
        4,
        50.598227300000000000,
        3.247466300000000000
    ), (
        2830,
        4,
        50.598226200000000000,
        3.247465000000000000
    ), (
        2831,
        4,
        50.598225000000000000,
        3.247463800000000000
    ), (
        2832,
        4,
        52.347166000000000000,
        4.946527800000000000
    ), (
        2833,
        4,
        52.347165800000000000,
        4.946527800000000000
    ), (
        2834,
        4,
        52.347165700000000000,
        4.946529000000000000
    ), (
        2835,
        4,
        52.347165700000000000,
        4.946529000000000000
    ), (
        2836,
        4,
        52.347165700000000000,
        4.946529000000000000
    ), (
        2837,
        4,
        52.347165700000000000,
        4.946529000000000000
    ), (
        2838,
        4,
        52.347165700000000000,
        4.946529000000000000
    ), (
        2839,
        4,
        52.347165700000000000,
        4.946529000000000000
    ), (
        2840,
        4,
        52.347165700000000000,
        4.946529000000000000
    ), (
        2841,
        4,
        52.347165700000000000,
        4.946529000000000000
    );

/*!40000 ALTER TABLE `GPS_points` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Points_of_paths`

--

DROP TABLE IF EXISTS `Points_of_paths`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Points_of_paths` (
        `id` int NOT NULL AUTO_INCREMENT,
        `point_number` int NOT NULL,
        `session_id` int NOT NULL,
        `gps_point_id` int NOT NULL,
        PRIMARY KEY (`id`),
        KEY `Points_of_paths_session_id__Sessions_id` (`session_id`),
        KEY `Points_of_paths_gps_point_id__GPS_points_id` (`gps_point_id`),
        CONSTRAINT `Points_of_paths_gps_point_id__GPS_points_id` FOREIGN KEY (`gps_point_id`) REFERENCES `GPS_points` (`id`),
        CONSTRAINT `Points_of_paths_session_id__Sessions_id` FOREIGN KEY (`session_id`) REFERENCES `Sessions` (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 771 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Points_of_paths`

--

LOCK TABLES `Points_of_paths` WRITE;

/*!40000 ALTER TABLE `Points_of_paths` DISABLE KEYS */

;

INSERT INTO `Points_of_paths`
VALUES (731, 1, 1, 2802), (732, 2, 1, 2803), (733, 3, 1, 2804), (734, 4, 1, 2805), (735, 5, 1, 2806), (736, 6, 1, 2807), (737, 7, 1, 2808), (738, 8, 1, 2809), (739, 9, 1, 2810), (740, 10, 1, 2811), (741, 1, 2, 2812), (742, 2, 2, 2813), (743, 3, 2, 2814), (744, 4, 2, 2815), (745, 5, 2, 2816), (746, 6, 2, 2817), (747, 7, 2, 2818), (748, 8, 2, 2819), (749, 9, 2, 2820), (750, 10, 2, 2821), (751, 1, 3, 2822), (752, 2, 3, 2823), (753, 3, 3, 2824), (754, 4, 3, 2825), (755, 5, 3, 2826), (756, 6, 3, 2827), (757, 7, 3, 2828), (758, 8, 3, 2829), (759, 9, 3, 2830), (760, 10, 3, 2831), (761, 1, 4, 2832), (762, 2, 4, 2833), (763, 3, 4, 2834), (764, 4, 4, 2835), (765, 5, 4, 2836), (766, 6, 4, 2837), (767, 7, 4, 2838), (768, 8, 4, 2839), (769, 9, 4, 2840), (770, 10, 4, 2841);

/*!40000 ALTER TABLE `Points_of_paths` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Robots`

--

DROP TABLE IF EXISTS `Robots`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Robots` (
        `serial_number` varchar(5) NOT NULL,
        PRIMARY KEY (`serial_number`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Robots`

--

LOCK TABLES `Robots` WRITE;

/*!40000 ALTER TABLE `Robots` DISABLE KEYS */

;

INSERT INTO `Robots` VALUES ('SN001'),('SN002');

/*!40000 ALTER TABLE `Robots` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Robots_of_customers`

--

DROP TABLE IF EXISTS `Robots_of_customers`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Robots_of_customers` (
        `id` int NOT NULL AUTO_INCREMENT,
        `robot_serial_number` varchar(5) NOT NULL,
        `customer_id` int NOT NULL,
        PRIMARY KEY (`id`),
        KEY `Robots_of_customers_robot_serial_number__Robot_serial_number` (`robot_serial_number`),
        KEY `Robots_of_customers_customer_id__Customers_id` (`customer_id`),
        CONSTRAINT `Robots_of_customers_customer_id__Customers_id` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`id`),
        CONSTRAINT `Robots_of_customers_robot_serial_number__Robot_serial_number` FOREIGN KEY (`robot_serial_number`) REFERENCES `Robots` (`serial_number`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Robots_of_customers`

--

LOCK TABLES `Robots_of_customers` WRITE;

/*!40000 ALTER TABLE `Robots_of_customers` DISABLE KEYS */

;

INSERT INTO
    `Robots_of_customers`
VALUES (2, 'SN001', 2), (3, 'SN001', 1), (4, 'SN002', 1);

/*!40000 ALTER TABLE `Robots_of_customers` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Sessions`

--

DROP TABLE IF EXISTS `Sessions`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Sessions` (
        `id` int NOT NULL AUTO_INCREMENT,
        `start_time` timestamp NOT NULL,
        `end_time` timestamp NOT NULL,
        `previous_sessions_id` int DEFAULT NULL,
        `robot_serial_number` varchar(5) NOT NULL,
        `field_id` int NOT NULL,
        PRIMARY KEY (`id`),
        KEY `Sessions_previous_sessions_id__Sessions_id` (`previous_sessions_id`),
        KEY `Sessions_robot_serial_number__Robot_serial_number` (`robot_serial_number`),
        KEY `Sessions_field_id__Fields_id` (`field_id`),
        CONSTRAINT `Sessions_field_id__Fields_id` FOREIGN KEY (`field_id`) REFERENCES `Fields` (`id`),
        CONSTRAINT `Sessions_previous_sessions_id__Sessions_id` FOREIGN KEY (`previous_sessions_id`) REFERENCES `Sessions` (`id`),
        CONSTRAINT `Sessions_robot_serial_number__Robot_serial_number` FOREIGN KEY (`robot_serial_number`) REFERENCES `Robots` (`serial_number`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Sessions`

--

LOCK TABLES `Sessions` WRITE;

/*!40000 ALTER TABLE `Sessions` DISABLE KEYS */

;

INSERT INTO `Sessions`
VALUES (
        1,
        '2021-01-01 08:00:01',
        '2021-01-01 10:00:01',
        NULL,
        'SN001',
        1
    ), (
        2,
        '2021-01-01 11:07:01',
        '2021-01-01 12:00:01',
        1,
        'SN001',
        1
    ), (
        3,
        '2022-05-01 15:00:01',
        '2022-05-01 18:23:01',
        NULL,
        'SN002',
        2
    ), (
        4,
        '2022-07-08 18:00:01',
        '2022-07-09 06:00:01',
        NULL,
        'SN001',
        3
    );

/*!40000 ALTER TABLE `Sessions` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Vesc_statistics`

--

DROP TABLE IF EXISTS `Vesc_statistics`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Vesc_statistics` (
        `id` int NOT NULL AUTO_INCREMENT,
        `sessions_id` int NOT NULL,
        `voltage` decimal(5, 2) NOT NULL,
        `timestamp` timestamp NOT NULL,
        PRIMARY KEY (`id`),
        KEY `Vesc_statistics_sessions_id__Sessions_id` (`sessions_id`),
        CONSTRAINT `Vesc_statistics_sessions_id__Sessions_id` FOREIGN KEY (`sessions_id`) REFERENCES `Sessions` (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Vesc_statistics`

--

LOCK TABLES `Vesc_statistics` WRITE;

/*!40000 ALTER TABLE `Vesc_statistics` DISABLE KEYS */

;

INSERT INTO `Vesc_statistics`
VALUES (
        1,
        1,
        25.50,
        '2021-01-01 08:00:07'
    ), (
        2,
        2,
        26.00,
        '2021-01-01 11:11:06'
    ), (
        3,
        3,
        12.40,
        '2022-05-01 15:05:01'
    ), (
        4,
        4,
        25.90,
        '2022-07-08 18:06:01'
    );

/*!40000 ALTER TABLE `Vesc_statistics` ENABLE KEYS */

;

UNLOCK TABLES;

--

-- Table structure for table `Weed_types`

--

DROP TABLE IF EXISTS `Weed_types`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

CREATE TABLE
    `Weed_types` (
        `id` int NOT NULL AUTO_INCREMENT,
        `label` varchar(255) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

--

-- Dumping data for table `Weed_types`

--

LOCK TABLES `Weed_types` WRITE;

/*!40000 ALTER TABLE `Weed_types` DISABLE KEYS */

;

INSERT INTO `Weed_types`
VALUES (1, 'Plantain'), (2, 'Daisy'), (3, 'Porcelle'), (4, 'Dandelion');

/*!40000 ALTER TABLE `Weed_types` ENABLE KEYS */

;

UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */

;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */

;

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */

;

/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */

;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */

;

/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */

;

/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */

;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */

;

-- Dump completed on 2022-09-02 13:16:16