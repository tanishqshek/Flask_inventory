-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Sep 10, 2020 at 08:10 AM
-- Server version: 10.1.13-MariaDB
-- PHP Version: 5.6.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE `locations` (
  `id` int(10) NOT NULL,
  `name` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`id`, `name`) VALUES
(1, 'Vidya'),
(2, 'Delhi'),
(3, 'Mumbai'),
(12, 'Chennai'),
(13, 'Bangalore'),
(14, 'Hyderabad'),
(15, 'Kolkata');

-- --------------------------------------------------------

--
-- Table structure for table `movements`
--

CREATE TABLE `movements` (
  `movement_id` int(10) NOT NULL,
  `prod_id` int(11) DEFAULT NULL,
  `prod_name` varchar(40) NOT NULL,
  `to_location_id` int(11) DEFAULT NULL,
  `to_location_name` varchar(40) NOT NULL,
  `from_location_id` int(11) DEFAULT NULL,
  `from_location_name` varchar(40) NOT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `movements`
--

INSERT INTO `movements` (`movement_id`, `prod_id`, `prod_name`, `to_location_id`, `to_location_name`, `from_location_id`, `from_location_name`, `quantity`) VALUES
(19, 19, 'Apple iPhone', 2, 'Delhi', 3, 'Mumbai', 5),
(20, 20, 'Samsung Galaxy', 3, 'Mumbai', 12, 'Chennai', 3),
(21, 22, 'Philips Hairdryer', 14, 'Hyderabad', 13, 'Bangalore', 8),
(22, 23, 'LG Tv', 1, 'Vidya', 15, 'Kolkata', 7);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(10) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`) VALUES
(19, 'Apple iPhone'),
(20, 'Samsung Galaxy'),
(21, 'Oneplus Nord'),
(22, 'Philips Hairdryer'),
(23, 'LG Tv');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `locations`
--
ALTER TABLE `locations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `movements`
--
ALTER TABLE `movements`
  ADD PRIMARY KEY (`movement_id`),
  ADD KEY `prod_id` (`prod_id`),
  ADD KEY `to_location_id` (`to_location_id`),
  ADD KEY `from_location_id` (`from_location_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `locations`
--
ALTER TABLE `locations`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `movements`
--
ALTER TABLE `movements`
  MODIFY `movement_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `movements`
--
ALTER TABLE `movements`
  ADD CONSTRAINT `movements_ibfk_1` FOREIGN KEY (`prod_id`) REFERENCES `products` (`id`),
  ADD CONSTRAINT `movements_ibfk_2` FOREIGN KEY (`to_location_id`) REFERENCES `locations` (`id`),
  ADD CONSTRAINT `movements_ibfk_3` FOREIGN KEY (`from_location_id`) REFERENCES `locations` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
