-- MySQL dump 10.13  Distrib 8.0.30, for Linux (aarch64)
--
-- Host: localhost    Database: fleet
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL COMMENT 'Customer phone with area code',
  `hash_pwd` varchar(255) NOT NULL COMMENT 'Customer pwd in MD5',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UC_Customer` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Extracted_weeds`
--

DROP TABLE IF EXISTS `Extracted_weeds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Extracted_weeds` (
  `id` int NOT NULL AUTO_INCREMENT,
  `point_of_path_id` int NOT NULL,
  `weed_type_id` int NOT NULL,
  `session_id` int NOT NULL,
  `number` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `Extracted_weeds_session_id__Sessions_id` (`session_id`),
  KEY `Extracted_weeds_point_of_path_id__Points_of_paths_id` (`point_of_path_id`),
  KEY `Extracted_weeds_weed_type_id__Weed_types_id` (`weed_type_id`),
  CONSTRAINT `Extracted_weeds_point_of_path_id__Points_of_paths_id` FOREIGN KEY (`point_of_path_id`) REFERENCES `Points_of_paths` (`id`),
  CONSTRAINT `Extracted_weeds_session_id__Sessions_id` FOREIGN KEY (`session_id`) REFERENCES `Sessions` (`id`),
  CONSTRAINT `Extracted_weeds_weed_type_id__Weed_types_id` FOREIGN KEY (`weed_type_id`) REFERENCES `Weed_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Fields`
--

DROP TABLE IF EXISTS `Fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fields` (
  `id` int NOT NULL AUTO_INCREMENT,
  `label` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Fields_corners`
--

DROP TABLE IF EXISTS `Fields_corners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fields_corners` (
  `id` int NOT NULL AUTO_INCREMENT,
  `field_id` int NOT NULL,
  `gps_point_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Fields_corners_field_id__Fields_id` (`field_id`),
  KEY `Fields_corners_gps_point_id__GPS_points_id` (`gps_point_id`),
  CONSTRAINT `Fields_corners_field_id__Fields_id` FOREIGN KEY (`field_id`) REFERENCES `Fields` (`id`),
  CONSTRAINT `Fields_corners_gps_point_id__GPS_points_id` FOREIGN KEY (`gps_point_id`) REFERENCES `GPS_points` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GPS_points`
--

DROP TABLE IF EXISTS `GPS_points`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GPS_points` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quality` int NOT NULL,
  `latitude` decimal(20,18) NOT NULL,
  `longitude` decimal(20,18) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Points_of_paths`
--

DROP TABLE IF EXISTS `Points_of_paths`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Points_of_paths` (
  `id` int NOT NULL AUTO_INCREMENT,
  `point_number` int NOT NULL,
  `session_id` int NOT NULL,
  `gps_point_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Points_of_paths_session_id__Sessions_id` (`session_id`),
  KEY `Points_of_paths_gps_point_id__GPS_points_id` (`gps_point_id`),
  CONSTRAINT `Points_of_paths_gps_point_id__GPS_points_id` FOREIGN KEY (`gps_point_id`) REFERENCES `GPS_points` (`id`),
  CONSTRAINT `Points_of_paths_session_id__Sessions_id` FOREIGN KEY (`session_id`) REFERENCES `Sessions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Robots`
--

DROP TABLE IF EXISTS `Robots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Robots` (
  `serial_number` varchar(5) NOT NULL,
  PRIMARY KEY (`serial_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Robots_of_customers`
--

DROP TABLE IF EXISTS `Robots_of_customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Robots_of_customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `robot_serial_number` varchar(5) NOT NULL,
  `customer_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Robots_of_customers_robot_serial_number__Robot_serial_number` (`robot_serial_number`),
  KEY `Robots_of_customers_customer_id__Customers_id` (`customer_id`),
  CONSTRAINT `Robots_of_customers_customer_id__Customers_id` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`id`),
  CONSTRAINT `Robots_of_customers_robot_serial_number__Robot_serial_number` FOREIGN KEY (`robot_serial_number`) REFERENCES `Robots` (`serial_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Sessions`
--

DROP TABLE IF EXISTS `Sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sessions` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Vesc_statistics`
--

DROP TABLE IF EXISTS `Vesc_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Vesc_statistics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` int NOT NULL,
  `voltage` decimal(5,2) NOT NULL,
  `timestamp` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Vesc_statistics_session_id__Sessions_id` (`session_id`),
  CONSTRAINT `Vesc_statistics_session_id__Sessions_id` FOREIGN KEY (`session_id`) REFERENCES `Sessions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Weed_types`
--

DROP TABLE IF EXISTS `Weed_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Weed_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `label` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-12 21:38:50
