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

-- Export de la structure de la base pour serial_sql_logger_data
CREATE DATABASE IF NOT EXISTS `serial_sql_logger_data` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `serial_sql_logger_data`;


-- Export de la structure de table serial_sql_logger_data. arduino
CREATE TABLE IF NOT EXISTS `arduino` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id unique du message',
  `horodatage` datetime NOT NULL COMMENT 'horodatage du message',
  `categorie` text NOT NULL COMMENT 'categorie du message',
  `niv_detail` tinyint(4) NOT NULL COMMENT 'niveau de detail du message log',
  `message` varchar(100) NOT NULL COMMENT 'message de log',
  `marker` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8 COMMENT='Log des cartes Arduino';

-- Export de données de la table serial_sql_logger_data.arduino: ~71 rows (environ)
/*!40000 ALTER TABLE `arduino` DISABLE KEYS */;
INSERT INTO `arduino` (`id`, `horodatage`, `categorie`, `niv_detail`, `message`, `marker`) VALUES
	(10, '2015-04-08 23:50:39', 'robot 1', 1, 'Arduino DUE boot=ok', b'0'),
	(11, '2014-09-21 10:00:00', 'robot1', 1, 'Serial init ok', b'0'),
	(12, '2014-09-21 10:00:01', 'robot1', 1, 'connect ok', b'0'),
	(23, '2014-09-22 10:00:20', 'robot2', 1, 'USB ready', b'0'),
	(24, '2015-02-25 17:56:00', 'robot2', 1, 'message depuis raspberry', b'1'),
	(25, '2015-04-06 20:57:22', 'robot2', 1, 'SQL ok', b'0'),
	(26, '2015-04-07 18:00:00', 'Jeudi', 1, '=============== BP DEPART CYCLE ===================', b'0'),
/*!40000 ALTER TABLE `arduino` ENABLE KEYS */;



-- Export de la structure de la base pour serial_sql_logger_setting
CREATE DATABASE IF NOT EXISTS `serial_sql_logger_setting` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `serial_sql_logger_setting`;


-- Export de la structure de table serial_sql_logger_setting. filter
CREATE TABLE IF NOT EXISTS `filter` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `tableArchive` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `dayStart` varchar(50) DEFAULT NULL,
  `dayEnd` varchar(50) DEFAULT NULL,
  `currentKeywordProfileName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger_setting.filter: ~0 rows (environ)
/*!40000 ALTER TABLE `filter` DISABLE KEYS */;
INSERT INTO `filter` (`id`, `tableArchive`, `category`, `dayStart`, `dayEnd`, `currentKeywordProfileName`) VALUES
	(1, 'arduino', 'all', '0', '1', 'Arduino');
/*!40000 ALTER TABLE `filter` ENABLE KEYS */;


-- Export de la structure de table serial_sql_logger_setting. keyword_color
CREATE TABLE IF NOT EXISTS `keyword_color` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywordProfile_id` int(11) NOT NULL,
  `keywordProfileName` varchar(50) DEFAULT NULL,
  `keywordCheck1` varchar(50) DEFAULT NULL,
  `keywordValue1` varchar(50) DEFAULT NULL,
  `keywordColor1` varchar(10) DEFAULT NULL,
  `keywordCheck2` varchar(50) DEFAULT NULL,
  `keywordValue2` varchar(50) DEFAULT NULL,
  `keywordColor2` varchar(10) DEFAULT NULL,
  `keywordCheck3` varchar(50) DEFAULT NULL,
  `keywordValue3` varchar(50) DEFAULT NULL,
  `keywordColor3` varchar(10) DEFAULT NULL,
  `keywordCheck4` varchar(50) DEFAULT NULL,
  `keywordValue4` varchar(50) DEFAULT NULL,
  `keywordColor4` varchar(10) DEFAULT NULL,
  `keywordCheck5` varchar(50) DEFAULT NULL,
  `keywordValue5` varchar(50) DEFAULT NULL,
  `keywordColor5` varchar(10) DEFAULT NULL,
  `keywordCheck6` varchar(50) DEFAULT NULL,
  `keywordValue6` varchar(50) DEFAULT NULL,
  `keywordColor6` varchar(10) DEFAULT NULL,
  `keywordCheck7` varchar(50) DEFAULT NULL,
  `keywordValue7` varchar(50) DEFAULT NULL,
  `keywordColor7` varchar(10) DEFAULT NULL,
  `keywordCheck8` varchar(50) DEFAULT NULL,
  `keywordValue8` varchar(50) DEFAULT NULL,
  `keywordColor8` varchar(10) DEFAULT NULL,
  `keywordCheck9` varchar(50) DEFAULT NULL,
  `keywordValue9` varchar(50) DEFAULT NULL,
  `keywordColor9` varchar(10) DEFAULT NULL,
  `keywordCheck10` varchar(50) DEFAULT NULL,
  `keywordValue10` varchar(50) DEFAULT NULL,
  `keywordColor10` varchar(10) DEFAULT NULL,
  UNIQUE KEY `id` (`id`),
  KEY `keywordProfile_id` (`keywordProfile_id`),
  KEY `keywordProfile_id_2` (`keywordProfile_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger_setting.keyword_color: ~10 rows (environ)
/*!40000 ALTER TABLE `keyword_color` DISABLE KEYS */;
INSERT INTO `keyword_color` (`id`, `keywordProfile_id`, `keywordProfileName`, `keywordCheck1`, `keywordValue1`, `keywordColor1`, `keywordCheck2`, `keywordValue2`, `keywordColor2`, `keywordCheck3`, `keywordValue3`, `keywordColor3`, `keywordCheck4`, `keywordValue4`, `keywordColor4`, `keywordCheck5`, `keywordValue5`, `keywordColor5`, `keywordCheck6`, `keywordValue6`, `keywordColor6`, `keywordCheck7`, `keywordValue7`, `keywordColor7`, `keywordCheck8`, `keywordValue8`, `keywordColor8`, `keywordCheck9`, `keywordValue9`, `keywordColor9`, `keywordCheck10`, `keywordValue10`, `keywordColor10`) VALUES
	(0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(2, 2, 'Bacacier07_', 'checked', 'BP DEPART CYCLE', '#00FF00', 'checked', 'BP ARRET CYCLE', '#FF0000', 'checked', 'Aiguillage codeur', '#00FFFF', 'checked', 'LIGNE FAITE DEPUIS API', '#00AAFF', '', 'DEBUT DEMANDE FDP PAR AUTOMATE', '#00FF00', '', 'Derniere tole enlevee a la main', '#FFFFFF', '', 'LIGNE FAITE DEPUIS API', '#D0D0D0', 'checked', 'DEPOSE', '#909090', '', 'Coupe Forme', '#CCCCCC', '', 'Tole FDP trouve', '#FFFFFF'),
	(3, 3, 'Rasbberry_', 'checked', 'raspberry', '#00FF00', 'checked', 'SQL', '#FF0000', '', 'USB', '#00FFFF', '', '', '#00AAFF', '', '', '#00FF00', '', '', '#FFFFFF', '', '', '#D0D0D0', '', '', '#909090', '', '', '#CCCCCC', 'checked', 'ready', '#FFFFFF'),
	(4, 4, 'Rasbberry_', 'checked', 'Arduino DUE', '#FFFF00', 'checked', 'SQL', '#FF0000', '', '', '#00FFFF', '', '', '#00AAFF', '', '', '#00FF00', '', '', '#FFFFFF', '', '', '#D0D0D0', '', '', '#909090', '', '', '#CCCCCC', 'checked', 'ready', '#FFFFFF'),
	(5, 5, 'Rasbberry_', 'checked', 'UNO', '#00FF00', 'checked', 'SQL', '#FF0000', '', '', '#00FFFF', '', '', '#00AAFF', '', '', '#00FF00', '', '', '#FFFFFF', '', '', '#D0D0D0', '', '', '#909090', '', '', '#CCCCCC', '', 'ready', '#FFFFFF'),
	(8, 21, 'Arduino', 'checked', 'Serial', '#FFFF00', 'checked', 'ok', '#FF0000', 'checked', 'HIGH', '#FFFF00', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'USB', '#FFFFFF'),
	(9, 22, 'Arduino 2', 'checked', 'Serial', '#FFFF00', 'checked', 'ok', '#00FF00', '', 'SQL', '#FFFFFF', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'checked', 'USB', '#FFFFFF'),
	(10, 23, 'Sam', 'checked', 'HIGH', '#FFFF00', 'checked', 'ok', '#00FF00', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
	(11, 24, 'nebjix', 'checked', 'compteur', '#00FF00', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
	(13, 26, 'Arduino DUE2', 'checked', 'Serial', '#FFFF00', 'checked', 'ok', '#FF0000', '', 'HIGH', '#FFFF00', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'USB', '#FFFFFF');
/*!40000 ALTER TABLE `keyword_color` ENABLE KEYS */;


-- Export de la structure de table serial_sql_logger_setting. keyword_color_back
CREATE TABLE IF NOT EXISTS `keyword_color_back` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `keywordCheck` varchar(50) DEFAULT NULL,
  `keywordValue` varchar(50) DEFAULT NULL,
  `keywordColor` varchar(10) DEFAULT NULL,
  `currentProfileId` int(11) DEFAULT NULL,
  `currentProfileName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger_setting.keyword_color_back: ~10 rows (environ)
/*!40000 ALTER TABLE `keyword_color_back` DISABLE KEYS */;
INSERT INTO `keyword_color_back` (`id`, `keywordCheck`, `keywordValue`, `keywordColor`, `currentProfileId`, `currentProfileName`) VALUES
	(1, 'checked', 'BP DEPART CYCLE', '#00FF00', NULL, NULL),
	(2, 'checked', 'BP ARRET CYCLE', '#FF0000', NULL, NULL),
	(3, 'checked', 'Aiguillage codeur', '#00FFFF', NULL, NULL),
	(4, '', 'LIGNE FAITE DEPUIS API', '#00AAFF', NULL, NULL),
	(5, '', 'DEBUT DEMANDE FDP PAR AUTOMATE', '#00FF00', NULL, NULL),
	(6, '', 'Derniere tole enlevee a la main', '#FFFFFF', NULL, NULL),
	(7, '', 'LIGNE FAITE DEPUIS API', '#D0D0D0', NULL, NULL),
	(8, '', 'DEPOSE', '#909090', NULL, NULL),
	(9, '', 'Coupe Forme', '#CCCCCC', NULL, NULL),
	(10, '', 'Tole FDP trouve', '#FFFFFF', NULL, NULL);
/*!40000 ALTER TABLE `keyword_color_back` ENABLE KEYS */;


-- Export de la structure de table serial_sql_logger_setting. keyword_color_list
CREATE TABLE IF NOT EXISTS `keyword_color_list` (
  `id` int(11) DEFAULT NULL,
  `keyword_id` int(11) DEFAULT NULL,
  `keywordcheck` varchar(50) DEFAULT NULL,
  `keywordvalue` varchar(50) DEFAULT NULL,
  `keywordcolor` varchar(50) DEFAULT NULL,
  `profile_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger_setting.keyword_color_list: ~0 rows (environ)
/*!40000 ALTER TABLE `keyword_color_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `keyword_color_list` ENABLE KEYS */;


-- Export de la structure de table serial_sql_logger_setting. keyword_color_profile
CREATE TABLE IF NOT EXISTS `keyword_color_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profilename` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger_setting.keyword_color_profile: ~8 rows (environ)
/*!40000 ALTER TABLE `keyword_color_profile` DISABLE KEYS */;
INSERT INTO `keyword_color_profile` (`id`, `profilename`) VALUES
	(2, 'Bacacier07'),
	(3, 'Raspberry'),
	(4, 'Arduino DUE'),
	(5, 'Arduino UNO'),
	(21, 'Arduino'),
	(22, 'Arduino 2'),
	(23, 'Sam'),
	(24, 'nebjix'),
	(26, 'Arduino DUE2');
/*!40000 ALTER TABLE `keyword_color_profile` ENABLE KEYS */;


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


-- Export de la structure de table serial_sql_logger_setting. size
CREATE TABLE IF NOT EXISTS `size` (
  `id` smallint(6) DEFAULT NULL,
  `unit` tinytext,
  `sizeCol1` smallint(6) DEFAULT NULL,
  `sizeCol2` smallint(6) DEFAULT NULL,
  `sizeCol3` smallint(6) DEFAULT NULL,
  `sizeCol4` smallint(6) DEFAULT NULL,
  `sizeCol5` smallint(6) DEFAULT NULL,
  `sizeCol6` smallint(6) DEFAULT NULL,
  `sizeCol7` smallint(6) DEFAULT NULL,
  `sizeCol8` smallint(6) DEFAULT NULL,
  `sizeCol9` smallint(6) DEFAULT NULL,
  `sizeCol10` smallint(6) DEFAULT NULL,
  `sizeCol11` smallint(6) DEFAULT NULL,
  `sizeCol12` smallint(6) DEFAULT NULL,
  `sizeCol13` smallint(6) DEFAULT NULL,
  `sizeCol14` smallint(6) DEFAULT NULL,
  `sizeCol15` smallint(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger_setting.size: ~0 rows (environ)
/*!40000 ALTER TABLE `size` DISABLE KEYS */;
INSERT INTO `size` (`id`, `unit`, `sizeCol1`, `sizeCol2`, `sizeCol3`, `sizeCol4`, `sizeCol5`, `sizeCol6`, `sizeCol7`, `sizeCol8`, `sizeCol9`, `sizeCol10`, `sizeCol11`, `sizeCol12`, `sizeCol13`, `sizeCol14`, `sizeCol15`) VALUES
	(1, 'px', 30, 150, 100, 60, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
/*!40000 ALTER TABLE `size` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
