-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u2
-- http://www.phpmyadmin.net
--
-- Machine: localhost
-- Gegenereerd op: 13 dec 2017 om 09:08
-- Serverversie: 5.5.57-0+deb8u1
-- PHP-versie: 5.6.30-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Databank: `project`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `Personen`
--

CREATE TABLE IF NOT EXISTS `Personen` (
  `id` bigint(12) NOT NULL DEFAULT '0',
  `firstname` varchar(64) NOT NULL,
  `lastname` varchar(64) NOT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `functionTYPE` int(3) DEFAULT NULL,
  `access` int(3) DEFAULT NULL,
  `state` int(3) DEFAULT NULL,
  `aanwezig` int(8) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Gegevens worden geëxporteerd voor tabel `Personen`
--

INSERT INTO `Personen` (`id`, `firstname`, `lastname`, `photo`, `functionTYPE`, `access`, `state`, `aanwezig`) VALUES
(257131264873, 'Clifford', 'Addai Twum', 'persoon3.gif', 1, 1, 1, 0),
(396961831727, 'Riadh', 'Ben Hassine', 'persoon1.gif', 3, 3, 1, 0),
(443466398134, 'Yannick', 'Buelens ', 'persoon2.gif', 2, 2, 0, 0),
(810602281367, 'John', 'Meeus', 'persoon2.gif', 3, 2, 1, 0);

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `Personen`
--
ALTER TABLE `Personen`
 ADD PRIMARY KEY (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
