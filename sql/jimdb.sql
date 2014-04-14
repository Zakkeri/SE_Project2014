CREATE DATABASE  IF NOT EXISTS `cardb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `cardb`;
-- MySQL dump 10.13  Distrib 5.6.13, for Win32 (x86)
--
-- Host: localhost    Database: cardb
-- ------------------------------------------------------
-- Server version	5.6.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `car`
--

DROP TABLE IF EXISTS `car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `car` (
  `vin` varchar(20) NOT NULL,
  `make` varchar(30) DEFAULT NULL,
  `model` varchar(30) DEFAULT NULL,
  `year` varchar(4) DEFAULT NULL,
  `retail` varchar(30) DEFAULT NULL,
  `avail_purchase` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`vin`),
  UNIQUE KEY `vin` (`vin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car`
--

LOCK TABLES `car` WRITE;
/*!40000 ALTER TABLE `car` DISABLE KEYS */;
INSERT INTO `car` VALUES ('12345672901234567890','Toyota','Venza','2014','32000',0),('12345678101234567890','Toyota','Venza','2010','27000',0),('12345678901234567290','Toyota','Venza','2009','26000',0),('12345678901234567890','Toyota','Venza','2009','25000',0),('12345678901234567897','Nissan','Nissan GTR','2014','100000',0),('12362595147894561235','Honda','Civic','2014','18000',0),('12365478973698527411','Toyota','Corolla','2014','17000',0),('75395145683571594568','Toyota','Prius','2010','40000',1);
/*!40000 ALTER TABLE `car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_features`
--

DROP TABLE IF EXISTS `car_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `car_features` (
  `vin` varchar(20) NOT NULL,
  `feat_type` varchar(40) NOT NULL,
  `descr` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`vin`,`feat_type`),
  CONSTRAINT `car_features_ibfk_1` FOREIGN KEY (`vin`) REFERENCES `car` (`vin`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_features`
--

LOCK TABLES `car_features` WRITE;
/*!40000 ALTER TABLE `car_features` DISABLE KEYS */;
INSERT INTO `car_features` VALUES ('12345678901234567890','Audio_System','Deafen Now'),('12345678901234567890','Comfort_and_Convenience','50 Cup Holders'),('12345678901234567890','Exterior_Design','Black Matte'),('12345678901234567890','Extras_Package','Deluxe Doomsday'),('12345678901234567890','Handling','4th Dimension Drift'),('12345678901234567890','Instrumentation_and_Controls','Doctor Who Dashboard'),('12345678901234567890','Interior_Design','Leather Everywhere'),('12345678901234567890','Maintenance_Programs','Replace new every day'),('12345678901234567890','Performance','Global Warming V4096'),('12345678901234567890','Safety_and_Security','American Freedom Missile'),('12345678901234567890','Warranties','Lifetime'),('12365478973698527411','Audio_System','7'),('12365478973698527411','Comfort_and_Convenience','8'),('12365478973698527411','Exterior_Design','5'),('12365478973698527411','Extras_Package','11'),('12365478973698527411','Handling','2'),('12365478973698527411','Instrumentation_and_Controls','3'),('12365478973698527411','Interior_Design','6'),('12365478973698527411','Maintenance_Programs','9'),('12365478973698527411','Performance','1'),('12365478973698527411','Safety_and_Security','4'),('12365478973698527411','Warranties','10'),('75395145683571594568','Audio_System','FM & AM Radio'),('75395145683571594568','Comfort_and_Convenience','Seat warmer'),('75395145683571594568','Exterior_Design','Black matte'),('75395145683571594568','Extras_Package','None'),('75395145683571594568','Handling','360 Turning'),('75395145683571594568','Instrumentation_and_Controls','Standard Dashboard'),('75395145683571594568','Interior_Design','Leather seats'),('75395145683571594568','Maintenance_Programs','5 year services'),('75395145683571594568','Performance','V6 Engine'),('75395145683571594568','Safety_and_Security','Airbags'),('75395145683571594568','Warranties','2 year manufacturer');
/*!40000 ALTER TABLE `car_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_pics`
--

DROP TABLE IF EXISTS `car_pics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `car_pics` (
  `picname` varchar(100) NOT NULL,
  `vin` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`picname`),
  KEY `vin` (`vin`),
  CONSTRAINT `car_pics_ibfk_1` FOREIGN KEY (`vin`) REFERENCES `car` (`vin`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_pics`
--

LOCK TABLES `car_pics` WRITE;
/*!40000 ALTER TABLE `car_pics` DISABLE KEYS */;
INSERT INTO `car_pics` VALUES ('12345678901234567890assassin-cros-1-1.jpg','12345678901234567890'),('12345678901234567890assassin-man-1.jpg','12345678901234567890'),('12345678901234567890bg_00.jpg','12345678901234567890'),('12345678901234567890bg_01.jpg','12345678901234567890');
/*!40000 ALTER TABLE `car_pics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_info`
--

DROP TABLE IF EXISTS `customer_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_info` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `addr1` varchar(200) DEFAULT NULL,
  `addr2` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(200) DEFAULT NULL,
  `pcode` varchar(6) DEFAULT NULL,
  `country` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`cid`),
  UNIQUE KEY `cid` (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_info`
--

LOCK TABLES `customer_info` WRITE;
/*!40000 ALTER TABLE `customer_info` DISABLE KEYS */;
INSERT INTO `customer_info` VALUES (1,'Bo','123','123','Tampa','Florida','33600','US'),(2,'To','123','123','Tampa','Florida','33600','US'),(3,'Tio','123','123','Tampa','Florida','33610','US'),(4,'123','123','123','123','123','123123','AF'),(5,'1234','123','123','123','123','123123','AF'),(6,'Jim','1234 Fake Street','4321 Street Fake','Fake Town','Fake State','13337','AF');
/*!40000 ALTER TABLE `customer_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_info`
--

DROP TABLE IF EXISTS `order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_info` (
  `oid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NOT NULL,
  `vin` varchar(20) NOT NULL,
  `sname` varchar(100) DEFAULT NULL,
  `fprice` varchar(30) DEFAULT NULL,
  `ddate` varchar(20) DEFAULT NULL,
  `update` date DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `delivered` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`oid`,`vin`),
  KEY `cid` (`cid`),
  KEY `vin` (`vin`),
  CONSTRAINT `order_info_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customer_info` (`cid`) ON UPDATE CASCADE,
  CONSTRAINT `order_info_ibfk_2` FOREIGN KEY (`vin`) REFERENCES `car` (`vin`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_info`
--

LOCK TABLES `order_info` WRITE;
/*!40000 ALTER TABLE `order_info` DISABLE KEYS */;
INSERT INTO `order_info` VALUES (1,1,'12345672901234567890','Sale Out','20000','March 2, 2014','2014-04-13','Canceled',0),(2,2,'12345678101234567890','Sale Out 2','20000','March 3, 2014','2014-04-13','Canceled',0),(3,4,'12345678901234567290','123','123','123','2014-04-13','Canceled',0),(4,5,'12345678901234567897','123','123','123','2014-04-13','Canceled',0),(5,6,'12345678901234567890','Ping Pong','300000','March 15, 2014','2014-04-13','Canceled',0),(6,4,'12345672901234567890','123','123','123','2014-04-13','Delivered',0),(7,4,'12345678101234567890','123','123','123','2014-04-13','Canceled',0),(8,4,'12345678101234567890','123','123','123','2014-04-13','Delivered',0),(9,6,'12345678901234567290','Discount Saving','20000','March 2, 2014','2014-04-13','Delivered',1),(10,6,'12345678901234567890','123','123','123','2014-04-14','Delivered',1),(11,4,'12345678901234567897','123','123','123','2014-04-14','Delivered',1),(12,4,'12362595147894561235','123','123','123','2014-04-14','Delivered',1),(13,5,'12365478973698527411','123','123','123','2014-04-14','Delivered',1);
/*!40000 ALTER TABLE `order_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_info`
--

DROP TABLE IF EXISTS `service_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_info` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NOT NULL,
  `vin` varchar(20) NOT NULL,
  `sdesc` varchar(250) DEFAULT NULL,
  `scost` int(11) DEFAULT NULL,
  `sdate` varchar(100) DEFAULT NULL,
  `stats` int(11) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `cid` (`cid`),
  KEY `vin` (`vin`),
  CONSTRAINT `service_info_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customer_info` (`cid`) ON UPDATE CASCADE,
  CONSTRAINT `service_info_ibfk_2` FOREIGN KEY (`vin`) REFERENCES `car` (`vin`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_info`
--

LOCK TABLES `service_info` WRITE;
/*!40000 ALTER TABLE `service_info` DISABLE KEYS */;
INSERT INTO `service_info` VALUES (1,6,'12345678901234567290','Oil Change',20,'March 1, 2014',2),(2,6,'12345678901234567290','Oil Change',20,'March 1, 2014',0),(3,6,'12345678901234567290','Oil Change',20,'March 1, 2014',2),(4,6,'12345678901234567290','Lol',1,'Never',0),(5,5,'12365478973698527411','123',123,'123',1);
/*!40000 ALTER TABLE `service_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(45) DEFAULT NULL,
  `salt` varchar(32) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `role` varchar(45) DEFAULT NULL,
  `isadmin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `uname` (`uname`),
  UNIQUE KEY `salt` (`salt`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','c90c87caf79cbd16856da621ca3a4c0e','7d36d3cfba9a69679716bec702c56888ba0ae210fbdbb471fff7b61dc5451c68','Admin',1),(2,'jimch','e3b04ce6e99cfd89e9fe6c33e171fef8','f09931ea4497a2d63e6018dca5c5f67eca94c2f3a74f0d1a877b88f174e38b33','Admin',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-14  1:06:01
