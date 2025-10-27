-- MySQL dump 10.13  Distrib 5.7.31, for Win64 (x86_64)
--
-- Host: localhost    Database: repair_management
-- ------------------------------------------------------
-- Server version	5.7.31

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
-- Table structure for table `app01_companyinfo`
--

DROP TABLE IF EXISTS `app01_companyinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_companyinfo` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `Tele` varchar(16) NOT NULL,
  `email` varchar(16) DEFAULT NULL,
  `manager` varchar(16) DEFAULT NULL,
  `gender` smallint(6) DEFAULT NULL,
  `adress` varchar(16) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `token` varchar(64) DEFAULT NULL,
  `openid` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid` (`openid`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_companyinfo`
--

LOCK TABLES `app01_companyinfo` WRITE;
/*!40000 ALTER TABLE `app01_companyinfo` DISABLE KEYS */;
INSERT INTO `app01_companyinfo` VALUES (1,'景耀数控设备有限公司','13823172206','wenjk20@lzu.edu.','文骏坤',1,'甘肃省兰州市榆中县夏官营镇吴谢营','123','ea823c18-01cb-4edb-92d4-dc4c7f0a9269','oJEEC7BNXG_iX58oThSqGA3vtQPA'),(2,'景耀合理竞赛得奖','12586482565','291066643@qq.com','jam',2,'甘肃省兰州市榆中县夏官营镇吴谢营','2568325','7ad5d098-055d-4576-b682-b62522639ca0',NULL),(4,'平安银行','','','',1,'','123456','c74e5487-0707-417c-9aed-288d58e2e4eb',NULL),(39,'WEN JUNKUN WEN','','wenjk923@outlook',NULL,1,NULL,NULL,NULL,NULL),(49,'文骏坤','17727435630','291066643@qq.com','',1,'','',NULL,NULL),(69,'中山英航','15648956852','nan','nan',2,'','nan',NULL,NULL),(80,'海天酱油','256489532','nan','nan',2,'','nan',NULL,NULL);
/*!40000 ALTER TABLE `app01_companyinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_companyinfo_machine`
--

DROP TABLE IF EXISTS `app01_companyinfo_machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_companyinfo_machine` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `companyinfo_id` bigint(20) NOT NULL,
  `machine_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app01_companyinfo_machin_companyinfo_id_machine_i_c76ae2f8_uniq` (`companyinfo_id`,`machine_id`),
  KEY `app01_companyinfo_ma_machine_id_0c4433d0_fk_app01_mac` (`machine_id`),
  CONSTRAINT `app01_companyinfo_ma_companyinfo_id_fe10f74b_fk_app01_com` FOREIGN KEY (`companyinfo_id`) REFERENCES `app01_companyinfo` (`id`),
  CONSTRAINT `app01_companyinfo_ma_machine_id_0c4433d0_fk_app01_mac` FOREIGN KEY (`machine_id`) REFERENCES `app01_machine` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_companyinfo_machine`
--

LOCK TABLES `app01_companyinfo_machine` WRITE;
/*!40000 ALTER TABLE `app01_companyinfo_machine` DISABLE KEYS */;
INSERT INTO `app01_companyinfo_machine` VALUES (3,1,2),(28,1,3),(6,1,4),(30,1,11),(4,2,2),(27,2,12),(33,2,16),(12,4,3),(11,4,4),(16,49,2),(18,49,3),(24,69,10),(51,80,11),(52,80,18),(53,80,19);
/*!40000 ALTER TABLE `app01_companyinfo_machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_machine`
--

DROP TABLE IF EXISTS `app01_machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_machine` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `machine_id` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_machine`
--

LOCK TABLES `app01_machine` WRITE;
/*!40000 ALTER TABLE `app01_machine` DISABLE KEYS */;
INSERT INTO `app01_machine` VALUES (2,'X86','1'),(3,'P90','546'),(4,'O95','256'),(10,'O19','125682563ED'),(11,'PS165','25984EGD'),(12,'JIS586','258964'),(13,'IOS5268','12568'),(14,'LSDI4568','25648'),(16,'I98','2658956234'),(18,'Pg158','25984EGU'),(19,'PS166','25984EGX'),(21,'nan','nan');
/*!40000 ALTER TABLE `app01_machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_managerinfo`
--

DROP TABLE IF EXISTS `app01_managerinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_managerinfo` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `account` varchar(16) NOT NULL,
  `password` varchar(32) NOT NULL,
  `token` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_managerinfo`
--

LOCK TABLES `app01_managerinfo` WRITE;
/*!40000 ALTER TABLE `app01_managerinfo` DISABLE KEYS */;
INSERT INTO `app01_managerinfo` VALUES (1,'文骏坤','123','123','SYvHGQoKZC29rgP3gFuIZPTwlkffduEPy6lPUMbP9tRYBTv0t3PgqVC1b0M2XXxQ');
/*!40000 ALTER TABLE `app01_managerinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_quotation`
--

DROP TABLE IF EXISTS `app01_quotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_quotation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `quotation` json DEFAULT NULL,
  `responsible_manager` varchar(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `repairOrder_id` bigint(20) NOT NULL,
  `file_position` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_quotation_repairOrder_id_11bc93f8_fk_app01_repairorder_id` (`repairOrder_id`),
  CONSTRAINT `app01_quotation_repairOrder_id_11bc93f8_fk_app01_repairorder_id` FOREIGN KEY (`repairOrder_id`) REFERENCES `app01_repairorder` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_quotation`
--

LOCK TABLES `app01_quotation` WRITE;
/*!40000 ALTER TABLE `app01_quotation` DISABLE KEYS */;
INSERT INTO `app01_quotation` VALUES (1,'\"保内无需报价\"','',NULL,46,'http://127.0.0.1:8000/media/quotation/46/202504020958_DC83.pdf'),(2,'\"保内无需报价\"','文骏坤','2025-04-16 04:28:34.340443',47,'http://127.0.0.1:8000/media/quotation/47/202504071323_8CDC.pdf'),(3,'\"保内无需报价\"','文骏坤','2025-04-16 07:46:16.752397',48,'http://127.0.0.1:8000/media/quotation/48/202504071325_5B6E.pdf'),(4,'\"保内无需报价\"','文骏坤','2025-04-16 08:36:59.481524',49,'http://127.0.0.1:8000/media/quotation/49/202504071326_CE24.pdf'),(5,'[{\"id\": 1, \"tag\": \"\", \"name\": \"模具3.1 CKE.01-13/14\", \"rate\": \"18\", \"unit\": \"套\", \"quantity\": \"2\", \"tax_price\": \"613.60\", \"tax_unitprice\": \"260\"}, {\"id\": 2, \"tag\": \"\", \"name\": \"员工派遣费\", \"rate\": \"13\", \"unit\": \"人\", \"quantity\": \"2\", \"tax_price\": \"67.80\", \"tax_unitprice\": \"30\"}]','文骏坤','2025-04-16 09:09:18.721687',50,'http://127.0.0.1:8000/media/quotation/50/202504110951_5A86.pdf'),(6,'\"保内无需报价\"','文骏坤','2025-04-21 08:30:07.252550',53,'http://127.0.0.1:8000/media/quotation/53/202504210828_B512.pdf'),(7,'[{\"id\": 1, \"tag\": \"\", \"name\": \"员工派遣费\", \"rate\": \"13\", \"unit\": \"人\", \"quantity\": \"2\", \"tax_price\": \"67.80\", \"tax_unitprice\": \"30\"}]','文骏坤','2025-04-21 11:39:16.176008',55,'http://127.0.0.1:8000/media/quotation/55/202504210850_5D46.pdf'),(9,'[{\"id\": 1, \"tag\": \"阿斯顿撒旦\", \"name\": \"员工派遣费\", \"rate\": \"13\", \"unit\": \"人\", \"quantity\": \"2\", \"tax_price\": \"67.80\", \"tax_unitprice\": \"30\"}]','文骏坤','2025-04-22 07:20:04.306921',52,'http://127.0.0.1:8000/media/quotation/52/202504161120_D0F9.pdf'),(10,'[{\"id\": 1, \"tag\": \"nan\", \"name\": \"维修员工费\", \"rate\": \"1.3\", \"unit\": \"人\", \"quantity\": \"3\", \"tax_price\": \"840\", \"tax_unitprice\": \"280\"}, {\"id\": 2, \"tag\": \"nan\", \"name\": \"维修员工费\", \"rate\": \"1.3\", \"unit\": \"人\", \"quantity\": \"6\", \"tax_price\": \"1680\", \"tax_unitprice\": \"280\"}, {\"id\": 3, \"tag\": \"nan\", \"name\": \"维修员工费\", \"rate\": \"1.3\", \"unit\": \"人\", \"quantity\": \"5\", \"tax_price\": \"1400\", \"tax_unitprice\": \"280\"}, {\"id\": 4, \"tag\": \"阿斯顿撒旦\", \"name\": \"员工派遣费\", \"rate\": \"13\", \"unit\": \"人\", \"quantity\": \"2\", \"tax_price\": \"67.80\", \"tax_unitprice\": \"30\"}]','文骏坤','2025-04-22 07:42:35.027062',51,'http://127.0.0.1:8000/media/quotation/51/202504161119_7881.pdf');
/*!40000 ALTER TABLE `app01_quotation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_repairadvice`
--

DROP TABLE IF EXISTS `app01_repairadvice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_repairadvice` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(50) NOT NULL,
  `customer_phone` varchar(20) NOT NULL,
  `satisfaction` int(11) DEFAULT NULL,
  `advice` longtext NOT NULL,
  `images` json DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by` varchar(16) NOT NULL,
  `repair_order_id` bigint(20) DEFAULT NULL,
  `reply` longtext,
  `status` int(11) DEFAULT NULL,
  `reply_date` datetime(6) DEFAULT NULL,
  `companyName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_repairadvice_repair_order_id_774f5f6f_fk_app01_rep` (`repair_order_id`),
  CONSTRAINT `app01_repairadvice_repair_order_id_774f5f6f_fk_app01_rep` FOREIGN KEY (`repair_order_id`) REFERENCES `app01_repairorder` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_repairadvice`
--

LOCK TABLES `app01_repairadvice` WRITE;
/*!40000 ALTER TABLE `app01_repairadvice` DISABLE KEYS */;
INSERT INTO `app01_repairadvice` VALUES (10,'景耀数控设备有限公司','13823172206',3,'asdasd','[\"/media/advice_images/2025/04/02/worker/1/2f00a8.png\", \"/media/advice_images/2025/04/02/worker/1/e1a53f.png\", \"/media/advice_images/2025/04/02/worker/1/4f5c1e.png\"]','2025-04-02 03:16:26.071092','景耀数控设备有限公司',NULL,'大师傅似的',2,'2025-04-18 00:00:00.000000',NULL),(11,'景耀数控设备有限公司','13823172206',3,'dasdas','[\"http://127.0.0.1:8000/media/advice_images/2025/04/02/worker/1/93c976.png\", \"http://127.0.0.1:8000/media/advice_images/2025/04/02/worker/1/7d11e8.png\", \"http://127.0.0.1:8000/media/advice_images/2025/04/02/worker/1/f237e7.png\"]','2025-04-02 12:54:29.107154','景耀数控设备有限公司',NULL,NULL,1,NULL,NULL),(12,'景耀数控设备有限公司','13823172206',3,'sdfsdf','[]','2025-04-07 03:20:11.040034','景耀数控设备有限公司',NULL,NULL,1,NULL,NULL),(13,'文骏坤','17727435630',NULL,'大师傅但是','[]','2025-04-07 03:33:33.208302','wen',NULL,NULL,1,NULL,NULL),(15,'景耀数控设备有限公司','13823172206',3,'sdsad','[\"http://127.0.0.1:8000/media/advice_images/2025/04/07/worker/1/dfa1fb.jpg\"]','2025-04-07 10:20:43.956518','景耀数控设备有限公司',46,NULL,1,NULL,NULL),(16,'景耀数控设备有限公司','13823172206',3,'大师傅似的','[\"http://127.0.0.1:8000/media/advice_images/2025/04/07/worker/1/0e1893.jpg\", \"http://127.0.0.1:8000/media/advice_images/2025/04/07/worker/1/8e6877.png\", \"http://127.0.0.1:8000/media/advice_images/2025/04/07/worker/1/32d8c9.mp4\"]','2025-04-07 15:21:00.971127','景耀数控设备有限公司',46,NULL,1,NULL,NULL),(17,'景耀合理竞赛得奖','12586482565',3,'sadas','[\"http://127.0.0.1:8000/media/advice_images/2025/04/11/worker/2/a2de04.png\"]','2025-04-11 09:50:01.015102','景耀合理竞赛得奖',NULL,'你师弟哦分joie文件',2,'2025-04-17 00:00:00.000000',NULL);
/*!40000 ALTER TABLE `app01_repairadvice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_repairorder`
--

DROP TABLE IF EXISTS `app01_repairorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_repairorder` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(32) NOT NULL,
  `customer_phone` varchar(20) NOT NULL,
  `emergency_level` varchar(10) NOT NULL,
  `machine_model` varchar(50) DEFAULT NULL,
  `machine_id` varchar(50) DEFAULT NULL,
  `purchase_date` varchar(16) DEFAULT NULL,
  `repair_date` date DEFAULT NULL,
  `description` longtext,
  `created_at` datetime(6) DEFAULT NULL,
  `company_id` bigint(20) DEFAULT NULL,
  `repair_images` json DEFAULT NULL,
  `order_id` varchar(32) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `worker_id` bigint(20) DEFAULT NULL,
  `dispatch_status` int(11) NOT NULL,
  `quotation_status` int(11) NOT NULL,
  `finished_date` varchar(16) DEFAULT NULL,
  `process_date` varchar(16) DEFAULT NULL,
  `responsible_name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app01_repairorder_order_id_1d109d62_uniq` (`order_id`),
  KEY `app01_repairorder_worker_id_adcc1361_fk_app01_workerinfo_id` (`worker_id`),
  KEY `app01_repairorder_company_id_a739fdbd_fk_app01_companyinfo_id` (`company_id`),
  CONSTRAINT `app01_repairorder_company_id_a739fdbd_fk_app01_companyinfo_id` FOREIGN KEY (`company_id`) REFERENCES `app01_companyinfo` (`id`),
  CONSTRAINT `app01_repairorder_worker_id_adcc1361_fk_app01_workerinfo_id` FOREIGN KEY (`worker_id`) REFERENCES `app01_workerinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_repairorder`
--

LOCK TABLES `app01_repairorder` WRITE;
/*!40000 ALTER TABLE `app01_repairorder` DISABLE KEYS */;
INSERT INTO `app01_repairorder` VALUES (46,'景耀数控设备有限公司','13823172206','low','X86','1235789','2021-09','2021-12-20','sadsda','2025-04-02 09:58:32.324502',1,'[\"http://127.0.0.1:8000/media/repair_images/2025/04/02/1/8e3393.png\", \"http://127.0.0.1:8000/media/repair_images/2025/04/02/1/bc15d9.png\", \"http://127.0.0.1:8000/media/repair_images/2025/04/02/1/0866a7.png\"]','202504020958_DC83',1,5,1,2,'2025-04-07',NULL,NULL),(47,'景耀数控设备有限公司','13823172206','low','X86','1235789',NULL,'2025-04-19','sdfsd','2025-04-07 13:23:45.017412',1,'[]','202504071323_8CDC',3,10,1,2,'2025-04-21','2025-04-21',NULL),(48,'景耀数控设备有限公司','13823172206','low','X86','1235789',NULL,'2021-12-23','sdfsdf','2025-04-07 13:25:26.276337',1,'[]','202504071325_5B6E',1,3,1,2,'2025-04-14',NULL,NULL),(49,'景耀数控设备有限公司','13823172206','low','X86','1235789',NULL,'2025-04-15','asdasd','2025-04-07 13:26:17.479609',1,'[\"http://127.0.0.1:8000/media/repair_images/2025/04/07/1/99457c.jpg\", \"http://127.0.0.1:8000/media/repair_images/2025/04/07/1/77fefb.png\", \"http://127.0.0.1:8000/media/repair_images/2025/04/07/1/d91b9a.png\", \"http://127.0.0.1:8000/media/repair_images/2025/04/07/1/321d67.png\", \"http://127.0.0.1:8000/media/repair_images/2025/04/07/1/978bfe.mp4\"]','202504071326_CE24',1,10,1,2,'2025-04-21','2025-04-21',NULL),(50,'景耀数控设备有限公司','13823172206','low','X86','1235789',NULL,'2025-04-14','分段书','2025-04-11 09:51:58.403996',1,'[]','202504110951_5A86',1,10,1,1,NULL,NULL,'文骏坤'),(51,'平安银行','156892356754','medium','X86','456876786','2021-09','2025-04-11','的撒佛iu就是从i京东i精品','2025-04-16 11:19:50.534486',4,'[\"http://127.0.0.1:8000/media/repair_images/2025/04/16/4/f6fe0c.jpg\", \"http://127.0.0.1:8000/media/repair_images/2025/04/16/4/a305ca.png\", \"http://127.0.0.1:8000/media/repair_images/2025/04/16/4/24ff14.png\"]','202504161119_7881',3,10,1,1,'2025-04-21','2025-04-21',NULL),(52,'平安银行','156467984253','low','X86','1235789',NULL,'2021-12-17','十分士大夫士大夫的撒旦我去问','2025-04-16 11:20:38.262645',4,'[\"http://127.0.0.1:8000/media/repair_images/2025/04/16/4/0f0be0.png\", \"http://127.0.0.1:8000/media/repair_images/2025/04/16/4/7c6c12.png\", \"http://127.0.0.1:8000/media/repair_images/2025/04/16/4/c8835a.png\"]','202504161120_D0F9',0,NULL,0,1,NULL,NULL,NULL),(53,'景耀数控设备有限公司','13823172206','low','X86','1235789','2021-09','2021-12-21','史蒂芬斯得分','2025-04-21 08:28:49.121710',1,'[]','202504210828_B512',0,NULL,0,2,NULL,NULL,'文'),(54,'景耀数控设备有限公司','13823172206','low','X86','1235789','2021-01','2025-04-17','对方的仿佛如同','2025-04-21 08:48:40.602117',1,'[]','202504210848_F5C7',3,10,1,0,'2025-04-21','2025-04-21','大撒反对'),(55,'景耀数控设备有限公司','13823172206','low','X86','1235789',NULL,'2025-04-02','士大夫很乖回复','2025-04-21 08:50:50.308754',1,'[]','202504210850_5D46',3,10,1,1,'2025-04-21','2025-04-21','打发士大夫'),(56,'景耀数控设备有限公司','13823172206','low','X86','1235789',NULL,'2021-04-23','cvmjuykihkfghgf','2025-04-21 08:51:56.737155',1,'[]','202504210851_328B',0,NULL,0,0,NULL,NULL,'puy'),(57,'景耀数控设备有限公司','13823172206','low','X86','1235789',NULL,'2021-01-15','史蒂芬斯得分','2025-04-21 08:59:02.769505',1,'[]','202504210859_751F',0,NULL,0,0,NULL,NULL,'士大夫反对');
/*!40000 ALTER TABLE `app01_repairorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_report`
--

DROP TABLE IF EXISTS `app01_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `report` longtext,
  `finished_images` json DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `repairOrder_id` bigint(20) NOT NULL,
  `confirm_status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_report_repairOrder_id_4a40fe62_fk_app01_repairorder_id` (`repairOrder_id`),
  CONSTRAINT `app01_report_repairOrder_id_4a40fe62_fk_app01_repairorder_id` FOREIGN KEY (`repairOrder_id`) REFERENCES `app01_repairorder` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_report`
--

LOCK TABLES `app01_report` WRITE;
/*!40000 ALTER TABLE `app01_report` DISABLE KEYS */;
INSERT INTO `app01_report` VALUES (4,'sadas','[\"http://127.0.0.1:8000/media/report_images/2025/04/07/202504020958_DC83/62bd21.jpg\", \"http://127.0.0.1:8000/media/report_images/2025/04/07/202504020958_DC83/b67665.mp4\"]','2025-04-07 09:12:19.681071',46,1),(5,'十大阿斯顿','[\"http://127.0.0.1:8000/media/report_images/2025/04/14/202504071325_5B6E/c4bdf9.jpg\"]','2025-04-14 08:38:27.222822',48,0),(6,'我的任务，完成啦！！！','[\"http://127.0.0.1:8000/media/report_images/2025/04/17/202504071323_8CDC/01dec3.jpg\", \"http://127.0.0.1:8000/media/report_images/2025/04/17/202504071323_8CDC/5a11fe.png\", \"http://127.0.0.1:8000/media/report_images/2025/04/17/202504071323_8CDC/2b5fdc.mp4\"]','2025-04-17 07:56:54.252909',47,1),(7,'程序都是真的','[\"http://127.0.0.1:8000/media/report_images/2025/04/21/202504071323_8CDC/9d0012.png\"]','2025-04-21 11:20:05.999837',47,0),(8,'三年非典拉开圣诞节佛i','[\"http://127.0.0.1:8000/media/report_images/2025/04/21/202504161119_7881/f341db.jpg\"]','2025-04-21 11:21:27.872690',51,0),(9,'你算佛教俄克拉','[\"http://127.0.0.1:8000/media/report_images/2025/04/21/202504071326_CE24/ab8f5b.png\"]','2025-04-21 11:31:25.999088',49,1),(10,'迷倒卢卡斯费德勒快女i技术的','[\"http://127.0.0.1:8000/media/report_images/2025/04/21/202504210848_F5C7/60bd46.png\"]','2025-04-21 11:52:50.365131',54,0),(11,'牛啊东方时空距离喀什酱豆腐了','[\"http://127.0.0.1:8000/media/report_images/2025/04/21/202504210850_5D46/c9eafb.jpg\"]','2025-04-21 11:59:05.030729',55,0);
/*!40000 ALTER TABLE `app01_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app01_workerinfo`
--

DROP TABLE IF EXISTS `app01_workerinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app01_workerinfo` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `password` varchar(64) NOT NULL,
  `Tele` varchar(16) DEFAULT NULL,
  `token` varchar(64) DEFAULT NULL,
  `openid` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid` (`openid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app01_workerinfo`
--

LOCK TABLES `app01_workerinfo` WRITE;
/*!40000 ALTER TABLE `app01_workerinfo` DISABLE KEYS */;
INSERT INTO `app01_workerinfo` VALUES (1,'wen','123','123','1564fb3e-a452-4114-ac17-f50dd67a67f4',NULL),(3,'彭于晏','123456','09315292251',NULL,NULL),(5,'彭嘉元','12564','12568423',NULL,NULL),(6,'士大夫','48675','12345543',NULL,NULL),(7,'马工','456','456',NULL,NULL),(8,'李工','789','789',NULL,NULL),(9,'人工','12','12',NULL,NULL),(10,'文骏坤','086422','17727435630','4f8c1880-f1f5-473a-be11-bbdbe95ad743','oJEEC7BNXG_iX58oThSqGA3vtQPA');
/*!40000 ALTER TABLE `app01_workerinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add company info',7,'add_companyinfo'),(26,'Can change company info',7,'change_companyinfo'),(27,'Can delete company info',7,'delete_companyinfo'),(28,'Can view company info',7,'view_companyinfo'),(29,'Can add worker info',8,'add_workerinfo'),(30,'Can change worker info',8,'change_workerinfo'),(31,'Can delete worker info',8,'delete_workerinfo'),(32,'Can view worker info',8,'view_workerinfo'),(33,'Can add machine',9,'add_machine'),(34,'Can change machine',9,'change_machine'),(35,'Can delete machine',9,'delete_machine'),(36,'Can view machine',9,'view_machine'),(37,'Can add repair order',10,'add_repairorder'),(38,'Can change repair order',10,'change_repairorder'),(39,'Can delete repair order',10,'delete_repairorder'),(40,'Can view repair order',10,'view_repairorder'),(41,'Can add repair image',11,'add_repairimage'),(42,'Can change repair image',11,'change_repairimage'),(43,'Can delete repair image',11,'delete_repairimage'),(44,'Can view repair image',11,'view_repairimage'),(45,'Can add repair advice',12,'add_repairadvice'),(46,'Can change repair advice',12,'change_repairadvice'),(47,'Can delete repair advice',12,'delete_repairadvice'),(48,'Can view repair advice',12,'view_repairadvice'),(49,'Can add report',13,'add_report'),(50,'Can change report',13,'change_report'),(51,'Can delete report',13,'delete_report'),(52,'Can view report',13,'view_report'),(53,'Can add quotation',14,'add_quotation'),(54,'Can change quotation',14,'change_quotation'),(55,'Can delete quotation',14,'delete_quotation'),(56,'Can view quotation',14,'view_quotation'),(57,'Can add manager info',15,'add_managerinfo'),(58,'Can change manager info',15,'change_managerinfo'),(59,'Can delete manager info',15,'delete_managerinfo'),(60,'Can view manager info',15,'view_managerinfo');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(7,'app01','companyinfo'),(9,'app01','machine'),(15,'app01','managerinfo'),(14,'app01','quotation'),(12,'app01','repairadvice'),(11,'app01','repairimage'),(10,'app01','repairorder'),(13,'app01','report'),(8,'app01','workerinfo'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-24 20:22:50
