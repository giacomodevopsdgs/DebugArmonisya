-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Creato il: Mag 06, 2021 alle 16:58
-- Versione del server: 10.3.27-MariaDB-0+deb10u1-log
-- Versione PHP: 7.3.27-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `api`
--

--
-- Dump dei dati per la tabella `privilege`
--

INSERT INTO `privilege` (`id`, `privilege`, `description`) VALUES
(1, 'asset_get', NULL),
(2, 'asset_patch', NULL),
(3, 'asset_delete', NULL),
(4, 'assets_get', NULL),
(5, 'assets_post', NULL),
(6, 'permission_identityGroups_get', NULL),
(7, 'permission_identityGroups_post', NULL),
(8, 'permission_roles_get', NULL),
(9, 'permission_identityGroup_patch', NULL),
(10, 'permission_identityGroup_delete', NULL),

(11, 'cyberark_safes_get', NULL),
(12, 'cyberark_safes_post', NULL),
(13, 'cyberark_safe_get', NULL),
(14, 'cyberark_safe_patch', NULL),
(15, 'cyberark_safe_delete', NULL),

(16, 'cyberark_accounts_get', NULL),
(17, 'cyberark_accounts_post', NULL),
(18, 'cyberark_account_get', NULL),
(19, 'cyberark_account_patch', NULL),
(20, 'cyberark_account_delete', NULL),

(21, 'cyberark_labs_post', NULL),
(22, 'usecase_bpers_post', NULL),

(23, 'conjur_resources_get', NULL),
(24, 'conjur_resource_get', NULL),
(25, 'conjur_resources_post', NULL),
(26, 'conjur_resource_put', NULL),

(27, 'kubernetes_resources_get', NULL);

--
-- Dump dei dati per la tabella `role`
--

INSERT INTO `role` (`id`, `role`, `description`) VALUES
(1, 'admin', 'admin'),
(2, 'staff', 'read / write, excluding assets'),
(3, 'readonly', 'readonly');

--
-- Dump dei dati per la tabella `role_privilege`
--

INSERT INTO `role_privilege` (`id_role`, `id_privilege`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(1, 23),
(1, 24),
(1, 25),
(1, 26),
(1, 27),

(2, 1),
(2, 4),
(2, 11),
(2, 12),
(2, 13),
(2, 14),
(2, 15),
(2, 16),
(2, 17),
(2, 18),
(2, 19),
(2, 20),
(2, 21),
(2, 22),
(2, 23),
(2, 24),
(2, 25),
(2, 26),
(2, 27),

(3, 1),
(3, 4),
(3, 11),
(3, 13),
(3, 16),
(3, 18),
(3, 23),
(3, 24),
(3, 27);


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
