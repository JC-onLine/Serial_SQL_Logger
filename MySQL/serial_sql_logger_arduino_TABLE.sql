-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le: Sam 20 Septembre 2014 à 00:41
-- Version du serveur: 5.5.38
-- Version de PHP: 5.4.4-14+deb7u12

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données: `serial_sql_logger`
--

-- --------------------------------------------------------

--
-- Structure de la table `bacacier63ligne03`
--

CREATE TABLE IF NOT EXISTS `arduino` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id unique du message',
  `horodatage` datetime NOT NULL COMMENT 'horodatage du message',
  `categorie` text NOT NULL COMMENT 'categorie du message',
  `niv_detail` tinyint(4) NOT NULL COMMENT 'niveau de detail du message log',
  `message` text NOT NULL COMMENT 'message de log',
  PRIMARY KEY (`horodatage`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='BAC63 L03 Profileuse avec Poinconnage' AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
