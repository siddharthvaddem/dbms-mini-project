-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 22, 2022 at 07:18 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `petdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `breed`
--

CREATE TABLE `breed` (
  `bid` int(11) NOT NULL,
  `breed_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `pet`
--

CREATE TABLE `pet` (
  `pid` int(11) NOT NULL,
  `pet_name` varchar(50) NOT NULL,
  `bid` int(11) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `age` int(3) NOT NULL,
  `height` int(4) NOT NULL,
  `weight` int(4) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `pet`
--
DELIMITER $$
CREATE TRIGGER `DELETE` BEFORE DELETE ON `pet` FOR EACH ROW INSERT INTO records VALUES(null,OLD.pid,'PET DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `INSERT` AFTER INSERT ON `pet` FOR EACH ROW INSERT INTO records VALUES(null,NEW.pid,'PET INSERTED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `UPDATE` AFTER UPDATE ON `pet` FOR EACH ROW INSERT INTO records VALUES(null,NEW.pid,'PET UPDATED',NOW())
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `records`
--

CREATE TABLE `records` (
  `rid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `vaccination`
--

CREATE TABLE `vaccination` (
  `vid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `vaccine_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE `vendor` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `breed`
--
ALTER TABLE `breed`
  ADD PRIMARY KEY (`bid`);

--
-- Indexes for table `pet`
--
ALTER TABLE `pet`
  ADD PRIMARY KEY (`pid`),
  ADD KEY `FK_BID` (`bid`);

--
-- Indexes for table `records`
--
ALTER TABLE `records`
  ADD PRIMARY KEY (`rid`),
  ADD KEY `FK_PID` (`pid`);

--
-- Indexes for table `vaccination`
--
ALTER TABLE `vaccination`
  ADD PRIMARY KEY (`vid`),
  ADD KEY `FK_PID2` (`pid`);

--
-- Indexes for table `vendor`
--
ALTER TABLE `vendor`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `vendor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `breed`
  MODIFY `bid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `pet`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

-- AUTO_INCREMENT for table `trig`
--
ALTER TABLE `records`
  MODIFY `rid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `vaccination`
  MODIFY `vid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;
--
-- Constraints for table `pet`
--
ALTER TABLE `pet`
  ADD CONSTRAINT `FK_BID` FOREIGN KEY (`bid`) REFERENCES `breed` (`bid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `records`
--
ALTER TABLE `records`
  ADD CONSTRAINT `FK_PID` FOREIGN KEY (`pid`) REFERENCES `pet` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `vaccination`
--
ALTER TABLE `vaccination`
  ADD CONSTRAINT `FK_PID2` FOREIGN KEY (`pid`) REFERENCES `pet` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;


INSERT INTO `breed` ( `breed_name`) VALUES ( 'Shiba Inu');
INSERT INTO `breed` ( `breed_name`) VALUES ( 'Golden Retriever');
INSERT INTO `breed` ( `breed_name`) VALUES ( 'German Shepherd');
INSERT INTO `breed` ( `breed_name`) VALUES ( 'Airedale Terrier');
INSERT INTO `breed` ( `breed_name`) VALUES ( 'Boxer');
INSERT INTO `breed` ( `breed_name`) VALUES ( 'Chihuahua');
INSERT INTO `breed` ( `breed_name`) VALUES ( 'Dachshund');
INSERT INTO `breed` ( `breed_name`) VALUES ( 'Dachshund');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
