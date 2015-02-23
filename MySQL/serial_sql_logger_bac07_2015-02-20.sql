-- --------------------------------------------------------
-- Hôte:                         192.168.1.150
-- Version du serveur:           5.5.38-0+wheezy1 - (Debian)
-- Serveur OS:                   debian-linux-gnu
-- HeidiSQL Version:             9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Export de la structure de la base pour serial_sql_logger_data
CREATE DATABASE IF NOT EXISTS `serial_sql_logger_data` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `serial_sql_logger_data`;


-- Export de la structure de table serial_sql_logger_data. bacacier07ligne01
CREATE TABLE IF NOT EXISTS `bacacier07ligne01` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id unique du message',
  `horodatage` datetime NOT NULL COMMENT 'horodatage du message',
  `categorie` text NOT NULL COMMENT 'categorie du message',
  `niv_detail` tinyint(4) NOT NULL COMMENT 'niveau de detail du message log',
  `message` varchar(100) NOT NULL COMMENT 'message de log',
  `marker` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=855 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='Log des cartes Arduino';

-- Export de données de la table serial_sql_logger_data.bacacier07ligne01: ~827 rows (environ)
/*!40000 ALTER TABLE `bacacier07ligne01` DISABLE KEYS */;
/*!40000 ALTER TABLE `bacacier07ligne01` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
