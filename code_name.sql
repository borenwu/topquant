DROP TABLE IF EXISTS `stock_code_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_code_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ts_code` varchar(45) DEFAULT NULL,
  `code` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `area` varchar(45) DEFAULT NULL,
  `industry` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;