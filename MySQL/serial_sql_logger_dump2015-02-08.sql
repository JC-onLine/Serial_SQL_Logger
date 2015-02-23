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

-- Export de la structure de la base pour serial_sql_logger
CREATE DATABASE IF NOT EXISTS `serial_sql_logger` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `serial_sql_logger`;


-- Export de la structure de table serial_sql_logger. arduino
CREATE TABLE IF NOT EXISTS `arduino` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id unique du message',
  `horodatage` datetime NOT NULL COMMENT 'horodatage du message',
  `categorie` text NOT NULL COMMENT 'categorie du message',
  `niv_detail` tinyint(4) NOT NULL COMMENT 'niveau de detail du message log',
  `message` varchar(100) NOT NULL COMMENT 'message de log',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8 COMMENT='Log des cartes Arduino';

-- Export de données de la table serial_sql_logger.arduino: ~48 rows (environ)
/*!40000 ALTER TABLE `arduino` DISABLE KEYS */;
INSERT INTO `arduino` (`id`, `horodatage`, `categorie`, `niv_detail`, `message`) VALUES
	(22, '2014-09-21 10:00:10', 'robot2', 1, 'Message1'),
	(31, '2014-09-22 10:00:07', 'robot1', 1, 'Message1'),
	(44, '2014-09-22 10:00:20', 'robot1', 1, 'Message1'),
	(45, '2014-09-22 10:00:22', 'robot1', 1, 'Message1'),
	(46, '2014-09-22 10:00:24', 'robot1', 1, 'Message1'),
	(47, '2014-09-22 10:00:26', 'robot2', 1, 'Hello World !'),
	(49, '2014-09-22 10:00:28', 'robot2', 1, 'Hello Cubietruck !'),
	(50, '2014-09-22 10:00:30', 'robot1', 1, 'Hello logger !'),
	(51, '2014-09-22 10:00:30', 'robot1', 1, 'Hello logger !'),
	(52, '2014-09-22 10:00:30', 'robot1', 1, 'Hello logger !'),
	(53, '2014-09-22 10:00:30', 'robot1', 1, 'Hello logger !'),
	(54, '2014-09-22 10:00:30', 'robot1', 1, 'Hello logger !'),
	(55, '2014-09-22 10:00:30', 'robot1', 1, 'Hello logger !'),
	(56, '2014-09-22 10:00:30', 'robot1', 1, 'Hello logger !'),
	(57, '2014-09-24 22:25:00', 'Uno', 1, ''),
	(58, '2014-09-24 22:27:00', 'Uno', 1, 'Bouton Test'),
	(59, '2014-09-24 22:30:00', 'Uno', 1, 'Hello MySQL !!'),
	(60, '2014-09-24 23:54:00', 'Uno', 1, 'Bouton Test'),
	(61, '2014-09-24 23:54:00', 'Uno', 1, 'Bouton Test'),
	(62, '2014-09-28 00:05:00', 'Uno', 1, 'Bouton Test'),
	(63, '2014-10-01 22:53:00', 'Uno', 1, 'Bouton Test'),
	(64, '2014-11-11 22:25:00', 'Uno', 1, 'Bouton Test'),
	(65, '2014-11-11 22:25:00', 'Uno', 1, 'Bouton Test'),
	(66, '2015-02-07 11:08:00', 'Uno', 1, 'Bouton Test'),
	(67, '2015-02-08 11:04:00', 'Uno', 1, 'Test depuis la tablette'),
	(68, '2015-02-08 19:18:00', 'Uno', 1, 'test sans horodatage'),
	(69, '2015-02-08 19:25:00', 'Uno', 1, '2015-02-08 19:25:00|Messa'),
	(70, '2015-02-08 21:45:00', '', 1, 'message simple'),
	(71, '2015-02-08 21:46:00', 'Tablette', 1, 'message simple tablette'),
	(72, '2015-02-08 21:46:00', 'Tablette', 1, 'simple tablette niv 2'),
	(73, '2015-02-08 21:50:00', 'Tablette', 2, 'tablette niv 2'),
	(74, '2015-02-08 22:25:00', 'Tablette', 3, 'horodatage ON niv3'),
	(75, '2015-02-08 22:27:00', 'horo', 3, 'message niv3'),
	(76, '2015-02-08 22:35:00', '4', 0, 'message de log avec horo '),
	(77, '2015-02-08 22:40:00', 'GT3', 5, 'message gt3 niv5'),
	(78, '2015-02-08 22:56:00', '2015-02-08 22:42:00', 2, 'GT3'),
	(79, '2015-02-08 23:04:00', '', 1, 'message simple'),
	(80, '2015-02-08 23:05:00', 'Manuelle', 2, 'message 2'),
	(81, '2015-02-08 23:06:00', 'Manuelle', 2, '2015-02-08 23:00:00'),
	(82, '2015-02-08 23:09:00', '', 1, 'message'),
	(83, '2015-02-08 23:10:00', 'Manuelle', 1, 'message'),
	(84, '2015-02-08 23:12:00', '2015-02-08 23:11:00', 2, 'message'),
	(85, '2015-02-08 23:17:00', 'Tablette', 3, 'message niv3'),
	(86, '2015-02-08 23:26:00', 'Manuelle', 2, 'message'),
	(87, '2015-02-08 23:27:00', 'Tablette', 2, 'message'),
	(88, '2015-02-08 23:28:00', 'Tablette', 4, 'full extraction'),
	(89, '2015-02-08 23:29:00', 'Manuelle', 3, 'sans categorie'),
	(90, '2015-02-08 23:30:00', 'Manuelle', 7, 'juste niv7');
/*!40000 ALTER TABLE `arduino` ENABLE KEYS */;


-- Export de la structure de table serial_sql_logger. bacacier63ligne03
CREATE TABLE IF NOT EXISTS `bacacier63ligne03` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id unique du message',
  `horodatage` datetime NOT NULL COMMENT 'horodatage du message',
  `categorie` text NOT NULL COMMENT 'categorie du message',
  `niv_detail` tinyint(4) NOT NULL COMMENT 'niveau de detail du message log',
  `message` text NOT NULL COMMENT 'message de log',
  PRIMARY KEY (`horodatage`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='BAC63 L03 Profileuse avec Poinconnage';

-- Export de données de la table serial_sql_logger.bacacier63ligne03: ~0 rows (environ)
/*!40000 ALTER TABLE `bacacier63ligne03` DISABLE KEYS */;
/*!40000 ALTER TABLE `bacacier63ligne03` ENABLE KEYS */;


-- Export de la structure de table serial_sql_logger. bacacier63ligne10
CREATE TABLE IF NOT EXISTS `bacacier63ligne10` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id unique du message',
  `horodatage` datetime NOT NULL,
  `categorie` text NOT NULL COMMENT 'categorie du message',
  `niv_detail` tinyint(11) NOT NULL COMMENT 'niveau de detail du message log',
  `message` text NOT NULL,
  PRIMARY KEY (`horodatage`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table serial_sql_logger.bacacier63ligne10: ~0 rows (environ)
/*!40000 ALTER TABLE `bacacier63ligne10` DISABLE KEYS */;
/*!40000 ALTER TABLE `bacacier63ligne10` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
