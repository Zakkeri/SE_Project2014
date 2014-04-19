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
INSERT INTO `car` VALUES ('0CSX8XJETEQFQUCCH','Toyota','Tacoma','2014','18125',1),('2JYGD7H2LBDJYT8VM','Toyota','Corolla','2014','16800',1),('36KV4KANPB46SDHWZ','Toyota','4Runner','2014','32820',1),('4XVUU42IJWQC4XQ5S','Toyota','RAV4','2014','23550',1),('6K3QE97DOPE7N24Z1','Toyota','Yaris','2014','14430',0),('9KOTMKTREBYMXAULO','Toyota','Land Cruiser','2014','79605',1),('EI7LRQ29GFUFPSQCO','Toyota','Prius','2014','24200',0),('GUB3TIOB73APO2542','Toyota','Highlander','2014','29215',1),('HCWJA6OH7C30R79D2','Toyota','Sienna','2014','26920',1),('LKGIDDNID1T47O106','Toyota','Venza','2014','27950',1),('MHM864EL7EBP8C0G9','Toyota','Avalon','2014','31340',1),('S4U0C31KGZPKIOBHJ','Toyota','Tundra','2014','26200',1),('U39781LGEQC6YLVO7','Toyota','FJ Curiser','2014','27680',1),('VI1KQE21N1RLH8E6I','Toyota','Sequoia','2014','44095',1),('Y36BM59QLBQL0E7A3','Toyota','Camry','2014','22425',1);
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
INSERT INTO `car_features` VALUES ('2JYGD7H2LBDJYT8VM','Audio_System','Tech Audio — includes AM/FM CD player, four speakers, auxiliary audio jack, USB 2.0 port 8 with iPod® 9 connectivity, iPod® 9 interface and hands-free phone capability, phone book access and music streaming via Bluetooth® 10 wireless technology'),('2JYGD7H2LBDJYT8VM','Comfort and Convenience','Adjustable front shoulder anchors, driver and front passenger seatbelt pretensioners with force limiters'),('2JYGD7H2LBDJYT8VM','Exterior Design','15-in. steel wheels with wheel covers and P195/65R15 91S tires'),('2JYGD7H2LBDJYT8VM','Extras_Package',''),('2JYGD7H2LBDJYT8VM','Handling','6-speed manual transmission'),('2JYGD7H2LBDJYT8VM','Instrumentation and Controls','Instrumentation with speedometer and tachometer, odometer, tripmeters, outside temperature, current/average fuel economy, cruising range, shift position; TPMS, 17 ECO indicator, one-touch 3-blink lane-change turn signal indicator, and warning messages (shift position and ECO indicator only on AT and CVT models)'),('2JYGD7H2LBDJYT8VM','Interior Design','Automatic climate control with dust and pollen filter and push-button controls'),('2JYGD7H2LBDJYT8VM','Maintenance Programs','ToyotaCare 25 featuring a no cost maintenance plan with roadside assistance'),('2JYGD7H2LBDJYT8VM','Performance','1.8-Liter 4-Cylinder DOHC 16-Valve with Dual Variable Valve Timing with intelligence (VVT-i); 132 hp @ 6000 rpm, 128 lb.-ft. @ 4400 rpm'),('2JYGD7H2LBDJYT8VM','Safety and Security','Star Safety System™ — includes Enhanced Vehicle Stability Control (VSC), 19 Traction Control (TRAC), Anti-lock Brake System (ABS), Electronic Brake-force Distribution (EBD), Brake Assist (BA) 20 and Smart Stop Technology® (SST) 21'),('2JYGD7H2LBDJYT8VM','Warranties',''),('6K3QE97DOPE7N24Z1','Audio_System','AM/FM CD player, six speakers, HD Radio™, 7 auxiliary audio jack, USB port 8 with iPod® 9 connectivity, auto sound leveling, hands-free phone capability, phone book access, and music streaming'),('6K3QE97DOPE7N24Z1','Comfort and Convenience','60/40 split fold-down rear seat'),('6K3QE97DOPE7N24Z1','Exterior Design','15-in. steel wheels with wheel covers and P175/65R15 88H tires'),('6K3QE97DOPE7N24Z1','Extras_Package',''),('6K3QE97DOPE7N24Z1','Handling','5-speed manual transmission'),('6K3QE97DOPE7N24Z1','Instrumentation and Controls','Sport analog instrumentation with speedometer, tachometer and fuel gauge; LCD display with odometer, tripmeters, clock, outside temperature, current/average fuel economy, distance to empty, average speed and shift-position; ECO Driving Indicator and warning messages'),('6K3QE97DOPE7N24Z1','Interior Design','Fabric-trimmed front seats; 4-way adjustable driver\'s seat; 4-way adjustable front passenger seat with seatback pocket'),('6K3QE97DOPE7N24Z1','Maintenance Programs','ToyotaCare 20 featuring a no cost maintenance plan with roadside assistance'),('6K3QE97DOPE7N24Z1','Performance','1.5-Liter 4-Cylinder DOHC 16-Valve Variable Valve Timing with intelligence (VVT-i); 106 hp @ 6000 rpm; 103 lb.-ft. @ 4200 rpm'),('6K3QE97DOPE7N24Z1','Safety and Security','Star Safety System™ - includes Enhanced Vehicle Stability Control (VSC), Traction Control (TRAC), Anti-lock Brake System (ABS), Electronic Brake-force Distribution (EBD), Brake Assist (BA) and Smart Stop Technology® (SST)'),('6K3QE97DOPE7N24Z1','Warranties','1 Year Manufacturer Warranty'),('EI7LRQ29GFUFPSQCO','Audio_System','Display Audio — includes 6.1-in. touch-screen, AM/FM CD player, six speakers, auxiliary audio jack, USB port, 11 vehicle information, hands-free phone capability and music streaming via Bluetooth®'),('EI7LRQ29GFUFPSQCO','Comfort and Convenience','Engine immobilizer\r\n\r\nHill Start Assist Control \r\n\r\nHead-Up Display (HUD) with speedometer, navigation and Hybrid System Indicator'),('EI7LRQ29GFUFPSQCO','Exterior Design','15-in. 5-spoke alloy wheels with full wheel covers and P195/65R15 tires\r\n\r\nLED Daytime Running Lights (DRL) with on/off feature'),('EI7LRQ29GFUFPSQCO','Extras_Package','Solar Roof Package — includes power tilt/slide moonroof with Solar Powered Ventilation System and Remote Air Conditioning System with sliding sunshade'),('EI7LRQ29GFUFPSQCO','Handling','Electric Power Steering (EPS); power-assisted rack-and-pinion'),('EI7LRQ29GFUFPSQCO','Instrumentation and Controls','Multi-Information Display with fuel consumption history, average fuel economy, distance to empty, average speed, trip distance, energy monitor, Hybrid System Indicator and ECO Savings Record\r\n\r\nDigital instrumentation with speedometer, fuel gauge, odometer, current fuel economy, shift position indicator and EV19/ECO/POWER Mode indicators'),('EI7LRQ29GFUFPSQCO','Interior Design','Automatic climate control with dust and pollen filtration mode\r\n\r\n60/40 split fold-down rear seats with center armrest'),('EI7LRQ29GFUFPSQCO','Maintenance Programs','ToyotaCare featuring a no cost maintenance plan with roadside assistance'),('EI7LRQ29GFUFPSQCO','Performance','1.8-Liter Aluminum 4-cylinder DOHC 16-Valve with Variable Valve Timing with intelligence (VVT-i), EV 19/ECO/POWER Modes; 98 hp @ 5200 rpm (73 kW @ 5200 rpm), 105 lb.-ft. @ 4000 rpm (142 N·m @ 4000 rpm)'),('EI7LRQ29GFUFPSQCO','Safety and Security','Star Safety Syste – includes Enhanced Vehicle Stability Control (VSC), Traction Control (TRAC), Anti-lock Brake System (ABS), Electronic Brake-force Distribution (EBD), Brake Assist (BA) and Smart Stop Technology® (SST)'),('EI7LRQ29GFUFPSQCO','Warranties','1 Year Manufacturer Warranty');
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
INSERT INTO `car_pics` VALUES ('2JYGD7H2LBDJYT8VM209.png','2JYGD7H2LBDJYT8VM'),('6K3QE97DOPE7N24Z1040.png','6K3QE97DOPE7N24Z1'),('6K3QE97DOPE7N24Z1209.png','6K3QE97DOPE7N24Z1'),('6K3QE97DOPE7N24Z13P0.png','6K3QE97DOPE7N24Z1'),('6K3QE97DOPE7N24Z18T0.png','6K3QE97DOPE7N24Z1'),('EI7LRQ29GFUFPSQCO1F7.png','EI7LRQ29GFUFPSQCO'),('EI7LRQ29GFUFPSQCO202.png','EI7LRQ29GFUFPSQCO'),('EI7LRQ29GFUFPSQCO3R3.png','EI7LRQ29GFUFPSQCO'),('EI7LRQ29GFUFPSQCO8S6.png','EI7LRQ29GFUFPSQCO');
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
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_info`
--

LOCK TABLES `customer_info` WRITE;
/*!40000 ALTER TABLE `customer_info` DISABLE KEYS */;
INSERT INTO `customer_info` VALUES (1,'Jim','8021 Indigo Plateau Ave','','Ashton','California','15187','US');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_info`
--

LOCK TABLES `order_info` WRITE;
/*!40000 ALTER TABLE `order_info` DISABLE KEYS */;
INSERT INTO `order_info` VALUES (1,1,'6K3QE97DOPE7N24Z1','Fox 4','15987','Now','2014-04-19','Canceled',0),(2,1,'6K3QE97DOPE7N24Z1','Undercover','18789','Now','2014-04-19','Delivered',1),(3,1,'EI7LRQ29GFUFPSQCO','Major Discount','15000','Now','2014-04-19','Ready to Process',0);
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
  `scost` varchar(100) DEFAULT NULL,
  `sdate` varchar(100) DEFAULT NULL,
  `stats` int(11) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `cid` (`cid`),
  KEY `vin` (`vin`),
  CONSTRAINT `service_info_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customer_info` (`cid`) ON UPDATE CASCADE,
  CONSTRAINT `service_info_ibfk_2` FOREIGN KEY (`vin`) REFERENCES `car` (`vin`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_info`
--

LOCK TABLES `service_info` WRITE;
/*!40000 ALTER TABLE `service_info` DISABLE KEYS */;
INSERT INTO `service_info` VALUES (1,1,'6K3QE97DOPE7N24Z1','Oil Change','20','Now',0),(2,1,'6K3QE97DOPE7N24Z1','Oil Change\r\nTire Rotation','40','Now',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','f323a35706d7c595d1b171a234e5fc13','48c81ed1a80a8eba25f7174473815db0d4c6cf71c66795d18729c92ee3e935d7','Admin',1),(2,'jimch','341012e15bb2ad0a71814d9944506667','bff7946db7f21ce37a966c4a6e2074753ae4b13a1e7f0d9dabf77c88ffcf5f6b','Sales',0),(3,'loki1','ae81eb6d41da6e3363a022262ff94340','054fa6c84a9242032e4864d7d072c73d49cb3ab122b33d0a718057cd95e5793a','Guest',0);
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

-- Dump completed on 2014-04-19  8:30:39
