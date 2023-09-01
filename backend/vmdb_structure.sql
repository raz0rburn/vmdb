-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Сен 01 2023 г., 18:00
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
-- База данных: `vmdb_structure`
--

-- --------------------------------------------------------

--
-- Структура таблицы `clusterinfo`
--

CREATE TABLE `clusterinfo` (
  `id` bigint(20) NOT NULL,
  `datetime` datetime NOT NULL,
  `cluster_name` varchar(127) NOT NULL,
  `total_cpu` int(11) NOT NULL,
  `total_memory` float NOT NULL,
  `num_cpu_cores` int(11) NOT NULL,
  `num_cpu_threads` int(11) NOT NULL,
  `num_hosts` int(11) NOT NULL,
  `num_eff_hosts` int(11) NOT NULL,
  `current_failover_level` int(11) NOT NULL,
  `num_vmotions` int(11) NOT NULL,
  `usage_total_cpu` int(11) NOT NULL,
  `usage_total_mem` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `dshostinfo`
--

CREATE TABLE `dshostinfo` (
  `id` bigint(20) NOT NULL,
  `datetime` datetime NOT NULL,
  `ds_name` varchar(511) NOT NULL,
  `esxihost_name` varchar(511) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `dsinfo`
--

CREATE TABLE `dsinfo` (
  `id` bigint(20) NOT NULL,
  `datetime` datetime NOT NULL,
  `ds_name` varchar(255) NOT NULL,
  `UUID` varchar(255) NOT NULL,
  `vmfs_version` varchar(255) NOT NULL,
  `is_local_vmfs` tinyint(1) NOT NULL,
  `SSD` tinyint(1) NOT NULL,
  `URL` varchar(1023) NOT NULL,
  `capacity` float NOT NULL,
  `uncommitted` float NOT NULL,
  `provisioned` float NOT NULL,
  `free_space` float NOT NULL,
  `hosts_quantity` int(11) NOT NULL,
  `vm_quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `hostinfo`
--

CREATE TABLE `hostinfo` (
  `id` bigint(20) NOT NULL,
  `datetime` datetime NOT NULL,
  `host_name` varchar(127) NOT NULL,
  `cluster_name` varchar(127) NOT NULL,
  `num_cpu_packages` smallint(4) NOT NULL,
  `num_cpu_cores` mediumint(9) NOT NULL,
  `num_cpu_threads` mediumint(9) NOT NULL,
  `cpu_mhz` mediumint(9) NOT NULL,
  `memory_size` float NOT NULL,
  `bios_date` varchar(127) NOT NULL,
  `bios_vendor` varchar(63) NOT NULL,
  `cpu_vendor` varchar(63) NOT NULL,
  `cpu_desc` varchar(127) NOT NULL,
  `srv_vendor` varchar(63) NOT NULL,
  `srv_model` varchar(127) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Структура таблицы `snapinfo`
--

CREATE TABLE `snapinfo` (
  `id` bigint(20) NOT NULL,
  `datetime` datetime NOT NULL,
  `dc_name` varchar(255) NOT NULL,
  `vm_name` varchar(255) NOT NULL,
  `snap_description` varchar(511) NOT NULL,
  `snap_name` varchar(1023) NOT NULL,
  `snap_size` float NOT NULL,
  `snap_count` int(11) NOT NULL,
  `snap_createtime` datetime NOT NULL,
  `snap_state` varchar(31) NOT NULL,
  `iteration` bigint(20) NOT NULL
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
  `cores_per_socket` tinyint(4) NOT NULL,
  `sockets` tinyint(4) NOT NULL,
  `memory_overhead` int(11) NOT NULL,
  `max_cpu_usage` int(11) NOT NULL,
  `max_memory_usage` int(11) NOT NULL,
  `ostype` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `connection_state` varchar(255) NOT NULL,
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
-- Индексы таблицы `clusterinfo`
--
ALTER TABLE `clusterinfo`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `dshostinfo`
--
ALTER TABLE `dshostinfo`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `dsinfo`
--
ALTER TABLE `dsinfo`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `hostinfo`
--
ALTER TABLE `hostinfo`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `nicinfo`
--
ALTER TABLE `nicinfo`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `snapinfo`
--
ALTER TABLE `snapinfo`
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
-- AUTO_INCREMENT для таблицы `clusterinfo`
--
ALTER TABLE `clusterinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT для таблицы `dshostinfo`
--
ALTER TABLE `dshostinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41851;

--
-- AUTO_INCREMENT для таблицы `dsinfo`
--
ALTER TABLE `dsinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3349;

--
-- AUTO_INCREMENT для таблицы `hostinfo`
--
ALTER TABLE `hostinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=157;

--
-- AUTO_INCREMENT для таблицы `nicinfo`
--
ALTER TABLE `nicinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83416;

--
-- AUTO_INCREMENT для таблицы `snapinfo`
--
ALTER TABLE `snapinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=148;

--
-- AUTO_INCREMENT для таблицы `vminfo`
--
ALTER TABLE `vminfo`
  MODIFY `id` bigint(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92669;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
