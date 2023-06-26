-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Июн 26 2023 г., 13:41
-- Версия сервера: 10.3.36-MariaDB-0+deb10u2+b1
-- Версия PHP: 7.3.31-1~deb10u1+ci202204271757+astra3+b1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `vmdb`
--

-- --------------------------------------------------------

--
-- Структура таблицы `nicinfo`
--

CREATE TABLE `nicinfo` (
  `id` bigint(20) NOT NULL,
  `datetime` datetime NOT NULL,
  `datacenter` varchar(255) NOT NULL,
  `cluster` varchar(255) NOT NULL,
  `host` varchar(255) NOT NULL,
  `vmname` varchar(255) NOT NULL,
  `mac` varchar(255) NOT NULL,
  `connected` tinyint(1) NOT NULL,
  `netlabel` varchar(255) NOT NULL,
  `prefix` tinyint(4) NOT NULL,
  `ipv4` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `vminfo`
--

CREATE TABLE `vminfo` (
  `id` bigint(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `datacenter` varchar(255) NOT NULL,
  `cluster` varchar(255) NOT NULL,
  `host` varchar(255) NOT NULL,
  `vmname` varchar(255) NOT NULL,
  `folder` varchar(255) NOT NULL,
  `ip_primary` int(10) UNSIGNED NOT NULL,
  `provisioned_space` float NOT NULL,
  `guest_disk_usage` float NOT NULL,
  `usage_storage` float NOT NULL,
  `path` varchar(512) NOT NULL,
  `mem` float NOT NULL,
  `cpu` int(11) NOT NULL,
  `ostype` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `annotation` varchar(1024) NOT NULL,
  `vmwtools` varchar(255) NOT NULL,
  `boottime` varchar(255) NOT NULL,
  `guestos_id` varchar(255) NOT NULL,
  `template` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `nicinfo`
--
ALTER TABLE `nicinfo`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `vminfo`
--
ALTER TABLE `vminfo`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `nicinfo`
--
ALTER TABLE `nicinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `vminfo`
--
ALTER TABLE `vminfo`
  MODIFY `id` bigint(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
