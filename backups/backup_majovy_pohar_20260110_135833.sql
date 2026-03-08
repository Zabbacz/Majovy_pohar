/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: majovy_pohar
-- ------------------------------------------------------
-- Server version	10.11.13-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `kategorie`
--

DROP TABLE IF EXISTS `kategorie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `kategorie` (
  `kategorie_id` int(11) NOT NULL AUTO_INCREMENT,
  `nazev` varchar(64) NOT NULL,
  `rocnik_od` year(4) DEFAULT NULL,
  `rocnik_do` year(4) DEFAULT NULL,
  PRIMARY KEY (`kategorie_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kategorie`
--

LOCK TABLES `kategorie` WRITE;
/*!40000 ALTER TABLE `kategorie` DISABLE KEYS */;
INSERT INTO `kategorie` VALUES
(36,'2095_Minizaci',NULL,NULL),
(37,'2096_Nejmladsi zaci',NULL,NULL),
(38,'2097_Mladsi zaci',NULL,NULL),
(39,'2098_Starsi zaci',NULL,NULL),
(40,'2151_GymTV',NULL,NULL);
/*!40000 ALTER TABLE `kategorie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `naradi`
--

DROP TABLE IF EXISTS `naradi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `naradi` (
  `naradi_id` int(11) NOT NULL AUTO_INCREMENT,
  `naradi` varchar(64) NOT NULL,
  `obrazek` blob DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`naradi_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `naradi`
--

LOCK TABLES `naradi` WRITE;
/*!40000 ALTER TABLE `naradi` DISABLE KEYS */;
INSERT INTO `naradi` VALUES
(1,'prostná',NULL,1),
(2,'kůň',NULL,1),
(3,'kruhy',NULL,1),
(4,'přeskok',NULL,1),
(5,'bradla',NULL,1),
(6,'hrazda',NULL,1),
(7,'kladina',NULL,0);
/*!40000 ALTER TABLE `naradi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oddily`
--

DROP TABLE IF EXISTS `oddily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `oddily` (
  `oddil_id` int(11) NOT NULL AUTO_INCREMENT,
  `nazev` varchar(128) NOT NULL,
  PRIMARY KEY (`oddil_id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oddily`
--

LOCK TABLES `oddily` WRITE;
/*!40000 ALTER TABLE `oddily` DISABLE KEYS */;
INSERT INTO `oddily` VALUES
(57,'Gymnastika Liberec'),
(58,'TJ Sokol Kolín'),
(59,'TJ Spartak MAS Sezimovo Ústí'),
(60,'TJ Doksy'),
(61,'TJ Sokol Dolní Žandov'),
(62,'TJ Lokomotiva Česká Lípa'),
(63,'GK Vítkovice'),
(64,'SK Viktoria Tábor, z.s.');
/*!40000 ALTER TABLE `oddily` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rozhodci`
--

DROP TABLE IF EXISTS `rozhodci`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `rozhodci` (
  `rozhodci_id` int(11) NOT NULL AUTO_INCREMENT,
  `jmeno` varchar(128) NOT NULL,
  `naradi_id` int(11) DEFAULT NULL,
  `rozhodci_typ` char(1) DEFAULT NULL,
  `oddil` varchar(128) DEFAULT NULL,
  `poznamka` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`rozhodci_id`),
  KEY `naradi_id` (`naradi_id`),
  CONSTRAINT `rozhodci_ibfk_1` FOREIGN KEY (`naradi_id`) REFERENCES `naradi` (`naradi_id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rozhodci`
--

LOCK TABLES `rozhodci` WRITE;
/*!40000 ALTER TABLE `rozhodci` DISABLE KEYS */;
INSERT INTO `rozhodci` VALUES
(57,'Drábek Libor',NULL,NULL,'Gymnastika Liberec',''),
(58,'Putík Miloslav',NULL,NULL,'Gymnastika Liberec',''),
(59,'Hejný Jakub',NULL,NULL,'TJ Sokol Kolín','E'),
(60,'Vogl Štěpán',NULL,NULL,'TJ Sokol Kolín','E'),
(61,'Smetana Sebastian',NULL,NULL,'TJ Sokol Kolín','E'),
(62,'Svobodová Michaela',NULL,NULL,'TJ Spartak MAS Sezimovo Ústí',''),
(63,'Vaněčková Michaela',NULL,NULL,'TJ Spartak MAS Sezimovo Ústí','');
/*!40000 ALTER TABLE `rozhodci` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treneri`
--

DROP TABLE IF EXISTS `treneri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `treneri` (
  `trener_id` int(11) NOT NULL AUTO_INCREMENT,
  `jmeno` varchar(128) NOT NULL DEFAULT 'Neuveden',
  PRIMARY KEY (`trener_id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treneri`
--

LOCK TABLES `treneri` WRITE;
/*!40000 ALTER TABLE `treneri` DISABLE KEYS */;
INSERT INTO `treneri` VALUES
(99,'Pietschmann+Sladová'),
(100,'Bareš'),
(101,'Svobodová,Míková'),
(102,'Kašíková'),
(103,'Jakša'),
(104,'Drábek'),
(105,'Vladimír Jakša'),
(106,'Petra Smith'),
(107,'Vaněčková'),
(108,'Sameš'),
(109,'Kučera+Nový'),
(110,'Kašíková,Pištěková'),
(111,'Pastrňáková'),
(112,'Kučera');
/*!40000 ALTER TABLE `treneri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zavodnici`
--

DROP TABLE IF EXISTS `zavodnici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zavodnici` (
  `zavodnik_id` int(11) NOT NULL AUTO_INCREMENT,
  `kategorie_id` int(11) NOT NULL,
  `rocnik` year(4) NOT NULL,
  `oddil_id` int(11) NOT NULL,
  `trener_id` int(11) NOT NULL,
  `druzstvo` smallint(6) NOT NULL,
  `jmeno` varchar(128) NOT NULL,
  `gis_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`zavodnik_id`),
  KEY `kategorie_id` (`kategorie_id`),
  KEY `trener_id` (`trener_id`),
  CONSTRAINT `zavodnici_ibfk_1` FOREIGN KEY (`kategorie_id`) REFERENCES `kategorie` (`kategorie_id`),
  CONSTRAINT `zavodnici_ibfk_2` FOREIGN KEY (`trener_id`) REFERENCES `treneri` (`trener_id`)
) ENGINE=InnoDB AUTO_INCREMENT=457 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zavodnici`
--

LOCK TABLES `zavodnici` WRITE;
/*!40000 ALTER TABLE `zavodnici` DISABLE KEYS */;
INSERT INTO `zavodnici` VALUES
(400,36,2011,57,99,0,'Dreithaler Rudolf',737751),
(401,36,2011,57,99,0,'Kubata Štěpán',357325),
(402,36,2011,57,99,0,'Rákosník Robinson',457443),
(403,36,2011,57,99,0,'Trnovský Jan Jakub',998179),
(404,36,2012,57,99,0,'Klusáček Martin',189310),
(405,36,2013,57,99,0,'Nol Josef',170015),
(406,36,2011,58,100,0,'Podveský Drahoslav',647379),
(407,36,2012,59,101,0,'Chramosta Čeněk',357311),
(408,36,2011,59,102,0,'Zvěřina Mikuláš',657030),
(409,36,2009,57,99,0,'Rákosník Jonatán',NULL),
(410,36,2010,60,103,0,'Šesták Adam',NULL),
(411,37,2009,57,104,0,'Hrobský David',631772),
(412,37,2009,57,104,0,'Řípa Jakub',466449),
(413,37,2009,57,104,0,'Řípa Petr',718611),
(414,37,2009,57,104,0,'Slad Dominik',416373),
(415,37,2010,57,104,0,'Žitňan Štěpán',264901),
(416,37,2010,60,105,0,'Havlík Vojtěch',561913),
(417,37,2010,60,105,0,'Schröder Tom',483613),
(418,37,2010,60,105,0,'Škorpil Jaroslav',839616),
(419,37,2011,61,106,0,'Smith Richard',684134),
(420,37,2010,58,100,0,'Čermák Radek',657923),
(421,37,2009,58,100,0,'Dvořák Prokop',924505),
(422,37,2010,58,100,0,'Javorský Václav',135601),
(423,37,2009,58,100,0,'Mach Ondřej',594364),
(424,37,2010,59,107,0,'Donát Radim',400985),
(425,37,2010,59,107,0,'Mairych Gabriel',340494),
(426,37,2010,59,107,0,'Míka Vilém',295216),
(427,37,2009,59,107,0,'Novotný Kryštof',824485),
(428,37,2010,59,107,0,'Jech Dalibor',277705),
(429,37,2009,62,108,0,'Panáček Filip',NULL),
(430,38,2007,57,109,0,'Holický Vít',790765),
(431,38,2007,60,103,0,'Kubíček Ondřej',861394),
(432,38,2007,60,105,0,'Tichý Martin',392139),
(433,38,2007,59,110,0,'Donát Čeněk',905580),
(434,39,2006,57,109,0,'Jäger Adam',508471),
(435,39,2006,57,109,0,'Křelina Pavel',657070),
(436,39,2005,61,106,0,'Smith Joseph',625559),
(437,39,2006,63,111,0,'Kaczor Jan',NULL),
(438,40,2006,57,112,0,'Hrobská Elen',679549),
(439,40,2007,64,102,0,'Mísařová Adéla',516747),
(440,40,2008,64,102,0,'Vylítová Anežka',627542),
(441,40,2009,61,106,0,'Nociarová Sofie',714809),
(442,40,2010,61,106,0,'Honzlová Marie',0),
(443,40,2010,61,106,0,'Raisová Natálie',867293),
(444,40,2004,61,106,0,'Lukáčová Adriana',0),
(445,40,2007,61,106,0,'Gašparová Růžena',0),
(446,40,2008,61,106,0,'Baňová Kateřina',0),
(447,40,2010,61,106,0,'Baňová Veronika',0),
(448,40,2010,61,106,0,'Rusinová Patricie Alexandra',0),
(449,40,2010,61,106,0,'Švejdová Lucie',0),
(450,40,2009,61,106,0,'Jurásková Julie',0),
(451,40,2008,61,106,0,'Skalická Andrea',0),
(452,40,2011,61,106,0,'Matoušková Markéta',0),
(453,40,2008,63,111,0,'Kostelecká Ella',NULL),
(454,40,2008,63,111,0,'Kaczorová Simona',NULL),
(455,40,2004,63,111,0,'Asenová Etela',NULL),
(456,40,2004,63,111,0,'Kovářová Viktorie',NULL);
/*!40000 ALTER TABLE `zavodnici` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `znamky`
--

DROP TABLE IF EXISTS `znamky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `znamky` (
  `zavodnik_id` int(11) NOT NULL,
  `naradi_id` int(11) NOT NULL,
  `znamka_D` decimal(12,4) NOT NULL,
  `pen` decimal(12,4) NOT NULL,
  `srazky_E` decimal(12,4) NOT NULL,
  `vysledna` decimal(12,4) NOT NULL,
  PRIMARY KEY (`zavodnik_id`,`naradi_id`),
  KEY `naradi_id` (`naradi_id`),
  CONSTRAINT `znamky_ibfk_1` FOREIGN KEY (`zavodnik_id`) REFERENCES `zavodnici` (`zavodnik_id`),
  CONSTRAINT `znamky_ibfk_2` FOREIGN KEY (`naradi_id`) REFERENCES `naradi` (`naradi_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `znamky`
--

LOCK TABLES `znamky` WRITE;
/*!40000 ALTER TABLE `znamky` DISABLE KEYS */;
/*!40000 ALTER TABLE `znamky` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'majovy_pohar'
--

--
-- Dumping routines for database 'majovy_pohar'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-10 13:58:33
