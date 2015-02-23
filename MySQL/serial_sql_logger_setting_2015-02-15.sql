-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           5.6.12-log - MySQL Community Server (GPL)
-- Serveur OS:                   Win64
-- HeidiSQL Version:             9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Export de la structure de la base pour serial_sql_logger_setting
CREATE DATABASE IF NOT EXISTS `serial_sql_logger_setting` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `serial_sql_logger_setting`;


-- Export de la structure de table serial_sql_logger_setting. filter
CREATE TABLE IF NOT EXISTS `filter` (
  `id` smallint(6) DEFAULT NULL,
  `tableArchive` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `dayStart` varchar(50) DEFAULT NULL,
  `dayEnd` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger_setting.filter: ~0 rows (environ)
/*!40000 ALTER TABLE `filter` DISABLE KEYS */;
INSERT INTO `filter` (`id`, `tableArchive`, `category`, `dayStart`, `dayEnd`) VALUES
	(1, 'bacacier07ligne01', '*', '0', '1');
/*!40000 ALTER TABLE `filter` ENABLE KEYS */;


-- Export de la structure de table serial_sql_logger_setting. server
CREATE TABLE IF NOT EXISTS `server` (
  `serverName` varchar(15) DEFAULT NULL,
  `serverIp` varchar(15) DEFAULT NULL,
  `serverUser` varchar(15) DEFAULT NULL,
  `serverPwd` varchar(15) DEFAULT NULL,
  `serverBase` varchar(15) DEFAULT NULL,
  `serverPort` smallint(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger_setting.server: ~0 rows (environ)
/*!40000 ALTER TABLE `server` DISABLE KEYS */;
/*!40000 ALTER TABLE `server` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
