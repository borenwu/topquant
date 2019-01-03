DROP TABLE IF EXISTS `stock_daily_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_daily_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trade_date` varchar(50) DEFAULT NULL,
  `ts_code` varchar(50) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `open` decimal(40,2) DEFAULT 0,
  `high` decimal(40,2) DEFAULT 0,
  `low` decimal(40,2) DEFAULT 0,
  `close` decimal(40,2) DEFAULT 0,
  `pre_close` decimal(40,2) DEFAULT 0,
  `change` decimal(40,2) DEFAULT 0,
  `pct_chg` decimal(40,2) DEFAULT 0,
  `vol` int(40) DEFAULT 0,
  `amount` decimal(40,2) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;


