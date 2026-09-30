-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 30, 2026 at 07:36 AM
-- Server version: 8.4.11-11
-- PHP Version: 8.1.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `news-admin`
--
CREATE DATABASE IF NOT EXISTS `news-admin` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `news-admin`;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` bigint UNSIGNED NOT NULL,
  `username` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` text COLLATE utf8mb4_unicode_ci,
  `email` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `forgot_unique_code` text COLLATE utf8mb4_unicode_ci,
  `forgot_at` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`, `email`, `forgot_unique_code`, `forgot_at`, `image`, `status`, `created_at`, `updated_at`) VALUES
(1, 'admin', '$2y$10$CPDdykyxNCj1iuImIarDRun21v9nyXfAwifhWXLo7KMQHzFs.gbsW', 'admin@gmail.com', '', '', 'panel/user.jpg', 1, '2026-09-28 06:04:56', '2026-09-28 06:04:56');

-- --------------------------------------------------------

--
-- Table structure for table `alerts`
--

CREATE TABLE `alerts` (
  `id` bigint UNSIGNED NOT NULL,
  `alert_type` enum('stock','commodity','forex','Crypto','IPO') COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `symbol` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `exchange` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ipo_price` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `current_price` decimal(15,4) DEFAULT NULL,
  `currency` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `percent_change` decimal(8,4) DEFAULT NULL,
  `direction` enum('up','down','unchanged') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `last_updated_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `episode_bookmarks`
--

CREATE TABLE `episode_bookmarks` (
  `id` bigint UNSIGNED NOT NULL,
  `episode_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `followed_at` timestamp NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `episode_play_history`
--

CREATE TABLE `episode_play_history` (
  `id` bigint UNSIGNED NOT NULL,
  `episode_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `listened_seconds` int NOT NULL,
  `completed` tinyint(1) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint UNSIGNED NOT NULL,
  `uuid` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `connection` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `queue` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `payload` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `exception` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `featured_section_rss_feeds`
--

CREATE TABLE `featured_section_rss_feeds` (
  `id` bigint UNSIGNED NOT NULL,
  `featured_section_id` bigint UNSIGNED NOT NULL,
  `rss_feed_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `feed_items`
--

CREATE TABLE `feed_items` (
  `id` bigint UNSIGNED NOT NULL,
  `rss_source_id` bigint UNSIGNED NOT NULL,
  `guid` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `image_url` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `author` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `published_at` timestamp NULL DEFAULT NULL,
  `fetched_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` bigint UNSIGNED NOT NULL,
  `queue` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payload` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `attempts` tinyint UNSIGNED NOT NULL,
  `reserved_at` int UNSIGNED DEFAULT NULL,
  `available_at` int UNSIGNED NOT NULL,
  `created_at` int UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int UNSIGNED NOT NULL,
  `migration` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `batch` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '2014_10_12_100000_create_password_reset_tokens_table', 1),
(2, '2014_10_12_100000_create_password_resets_table', 1),
(3, '2019_08_19_000000_create_failed_jobs_table', 1),
(4, '2019_12_14_000001_create_personal_access_tokens_table', 1),
(5, '2023_11_27_064401_create_all_tables', 1),
(6, '2024_04_10_104520_create_admin_table', 1),
(7, '2024_04_10_104525_create_tbl_users_table', 1),
(8, '2024_04_10_104530_create_tbl_languages_table', 1),
(9, '2024_04_10_105710_create_tbl_category_table', 1),
(10, '2024_04_10_110701_create_tbl_subcategory_table', 1),
(11, '2024_04_10_114540_create_tbl_tag_table', 1),
(12, '2024_04_10_115137_create_tbl_news_table', 1),
(13, '2024_04_10_115178_create_tbl_news_image_table', 1),
(14, '2024_04_10_120536_create_tbl_breaking_news_table', 1),
(15, '2024_04_10_122518_create_tbl_live_streaming_table', 1),
(16, '2024_04_12_091014_create_tbl_settings_table', 1),
(17, '2024_04_12_091153_create_tbl_bookmark_table', 1),
(18, '2024_04_12_091423_create_tbl_news_like_table', 1),
(19, '2024_04_12_091725_create_tbl_news_view_table', 1),
(20, '2024_04_12_092110_create_tbl_breaking_news_view_table', 1),
(21, '2024_04_12_092330_create_tbl_comment_table', 1),
(22, '2024_04_12_093239_create_tbl_comment_flag_table', 1),
(23, '2024_04_12_095441_create_tbl_comment_like_table', 1),
(24, '2024_04_12_100023_create_tbl_comment_notification_table', 1),
(25, '2024_04_12_100436_create_tbl_survey_question_table', 1),
(26, '2024_04_12_100901_create_tbl_survey_option_table', 1),
(27, '2024_04_12_102723_create_tbl_survey_result_table', 1),
(28, '2024_04_12_103031_create_tbl_location_table', 1),
(29, '2024_04_12_103211_create_tbl_notifications_table', 1),
(30, '2024_04_13_052620_create_tbl_token_table', 1),
(31, '2024_04_13_052717_create_tbl_users_category_table', 1),
(32, '2024_04_13_053529_create_tbl_pages_table', 1),
(33, '2024_04_13_054156_create_tbl_featured_sections_table', 1),
(34, '2024_04_13_055248_create_tbl_ad_spaces_table', 1),
(35, '2024_04_13_055535_create_tbl_web_settings_table', 1),
(36, '2024_04_13_055705_create_tbl_web_seo_pages_table', 1),
(37, '2024_07_15_161407_create_tbl_social_media_table', 1),
(38, '2024_11_09_150136_create_tbl_rss_table', 1),
(39, '2025_01_23_100907_version_3_2_0', 1),
(40, '2025_04_07_051450_version_3_2_1', 1),
(41, '2025_05_06_102624_version_3_2_2', 1),
(42, '2025_05_06_102624_version_3_2_3', 1),
(43, '2025_08_18_183935_version_3_2_4', 1),
(44, '2025_09_03_124942_update_tbl_news_table', 1),
(45, '2025_11_08_155756_version_3_2_5', 1),
(46, '2025_12_19_095852_version_3_2_6_table', 1),
(47, '2026_01_13_164209_create_jobs_table', 1),
(48, '2026_02_18_172444_version_3_2_7_table', 1),
(49, '2026_03_20_122142_version_3_2_8_table', 1),
(50, '2026_04_08_100000_create_service_health_logs_table', 1),
(51, '2026_05_07_111223_version_3_2_9_table', 1),
(52, '2026_07_10_100157_version_4_0_0_table', 1);

-- --------------------------------------------------------

--
-- Table structure for table `model_has_permissions`
--

CREATE TABLE `model_has_permissions` (
  `permission_id` bigint UNSIGNED NOT NULL,
  `model_type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `model_has_roles`
--

CREATE TABLE `model_has_roles` (
  `role_id` bigint UNSIGNED NOT NULL,
  `model_type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `model_has_roles`
--

INSERT INTO `model_has_roles` (`role_id`, `model_type`, `model_id`) VALUES
(1, 'App\\Models\\Admin', 1);

-- --------------------------------------------------------

--
-- Table structure for table `notification_preferences`
--

CREATE TABLE `notification_preferences` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `notification_type_id` bigint UNSIGNED NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notification_types`
--

CREATE TABLE `notification_types` (
  `id` bigint UNSIGNED NOT NULL,
  `key` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `notification_types`
--

INSERT INTO `notification_types` (`id`, `key`, `label`, `created_at`, `updated_at`) VALUES
(1, 'news', 'News', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(2, 'podcasts', 'Podcasts', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(3, 'alerts', 'Alerts', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(4, 'comments', 'Comments', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(5, 'announcements', 'Announcements', '2026-09-28 05:31:11', '2026-09-28 05:31:11');

-- --------------------------------------------------------

--
-- Table structure for table `password_resets`
--

CREATE TABLE `password_resets` (
  `email` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `guard_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `permissions`
--

INSERT INTO `permissions` (`id`, `name`, `guard_name`, `created_at`, `updated_at`) VALUES
(1, 'category-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(2, 'category-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(3, 'category-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(4, 'category-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(5, 'category-order-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(6, 'sub-category-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(7, 'sub-category-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(8, 'sub-category-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(9, 'sub-category-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(10, 'sub-category-order-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(11, 'tag-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(12, 'tag-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(13, 'tag-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(14, 'tag-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(15, 'news-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(16, 'news-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(17, 'news-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(18, 'news-edit-description', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(19, 'news-clone', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(20, 'news-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(21, 'news-bulk-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(22, 'breaking-news-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(23, 'breaking-news-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(24, 'breaking-news-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(25, 'breaking-news-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(26, 'breaking-news-bulk-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(27, 'live-streaming-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(28, 'live-streaming-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(29, 'live-streaming-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(30, 'live-streaming-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(31, 'rss-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(32, 'rss-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(33, 'rss-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(34, 'rss-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(35, 'rss-bulk-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(36, 'featured-section-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(37, 'featured-section-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(38, 'featured-section-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(39, 'featured-section-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(40, 'featured-section-order-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(41, 'ad-space-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(42, 'ad-space-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(43, 'ad-space-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(44, 'ad-space-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(45, 'user-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(46, 'user-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(47, 'comment-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(48, 'comment-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(49, 'comment-bulk-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(50, 'comment-flag-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(51, 'comment-flag-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(52, 'notification-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(53, 'notification-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(54, 'notification-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(55, 'survey-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(56, 'survey-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(57, 'survey-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(58, 'survey-view', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(59, 'survey-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(60, 'survey-bulk-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(61, 'location-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(62, 'location-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(63, 'location-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(64, 'location-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(65, 'page-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(66, 'page-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(67, 'page-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(68, 'page-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(69, 'staff-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(70, 'staff-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(71, 'staff-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(72, 'staff-change-password', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(73, 'staff-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(74, 'role-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(75, 'role-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(76, 'role-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(77, 'role-view', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(78, 'role-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(79, 'general-settings', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(80, 'panel-settings', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(81, 'web-settings', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(82, 'app-settings', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(83, 'language-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(84, 'language-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(85, 'language-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(86, 'language-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(87, 'seo-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(88, 'seo-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(89, 'seo-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(90, 'seo-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(91, 'firebase-configuration', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(92, 'social-media-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(93, 'social-media-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(94, 'social-media-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(95, 'social-media-delete', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(96, 'system-update', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(97, 'author-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(98, 'author-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(99, 'enews-list', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(100, 'enews-create', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(101, 'enews-edit', 'admin', '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(102, 'enews-delete', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(103, 'newsbuzz-list', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(104, 'newsbuzz-create', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(105, 'newsbuzz-edit', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(106, 'newsbuzz-delete', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(107, 'newsbuzz-bulk-delete', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(108, 'podcast-list', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(109, 'podcast-create', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(110, 'podcast-edit', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(111, 'podcast-delete', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(112, 'podcast-bulk-delete', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(113, 'alerts-list', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(114, 'alerts-create', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(115, 'alerts-edit', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12'),
(116, 'alerts-delete', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12');

-- --------------------------------------------------------

--
-- Table structure for table `personal_access_tokens`
--

CREATE TABLE `personal_access_tokens` (
  `id` bigint UNSIGNED NOT NULL,
  `tokenable_type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tokenable_id` bigint UNSIGNED NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `abilities` text COLLATE utf8mb4_unicode_ci,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `podcasts`
--

CREATE TABLE `podcasts` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `title` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `draft` tinyint(1) NOT NULL DEFAULT '0',
  `status` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '1',
  `published_at` timestamp NULL DEFAULT NULL,
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `podcast_episodes`
--

CREATE TABLE `podcast_episodes` (
  `id` bigint UNSIGNED NOT NULL,
  `podcast_id` bigint UNSIGNED NOT NULL,
  `episode_no` int NOT NULL,
  `title` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `audio_url` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration_seconds` int NOT NULL,
  `draft` tinyint(1) NOT NULL DEFAULT '0',
  `published_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `podcast_follows`
--

CREATE TABLE `podcast_follows` (
  `id` bigint UNSIGNED NOT NULL,
  `podcast_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `followed_at` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `guard_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `guard_name`, `created_at`, `updated_at`) VALUES
(1, 'Admin', 'admin', '2026-09-28 05:31:12', '2026-09-28 05:31:12');

-- --------------------------------------------------------

--
-- Table structure for table `role_has_permissions`
--

CREATE TABLE `role_has_permissions` (
  `permission_id` bigint UNSIGNED NOT NULL,
  `role_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `role_has_permissions`
--

INSERT INTO `role_has_permissions` (`permission_id`, `role_id`) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(10, 1),
(11, 1),
(12, 1),
(13, 1),
(14, 1),
(15, 1),
(16, 1),
(17, 1),
(18, 1),
(19, 1),
(20, 1),
(21, 1),
(22, 1),
(23, 1),
(24, 1),
(25, 1),
(26, 1),
(27, 1),
(28, 1),
(29, 1),
(30, 1),
(31, 1),
(32, 1),
(33, 1),
(34, 1),
(35, 1),
(36, 1),
(37, 1),
(38, 1),
(39, 1),
(40, 1),
(41, 1),
(42, 1),
(43, 1),
(44, 1),
(45, 1),
(46, 1),
(47, 1),
(48, 1),
(49, 1),
(50, 1),
(51, 1),
(52, 1),
(53, 1),
(54, 1),
(55, 1),
(56, 1),
(57, 1),
(58, 1),
(59, 1),
(60, 1),
(61, 1),
(62, 1),
(63, 1),
(64, 1),
(65, 1),
(66, 1),
(67, 1),
(68, 1),
(69, 1),
(70, 1),
(71, 1),
(72, 1),
(73, 1),
(74, 1),
(75, 1),
(76, 1),
(77, 1),
(78, 1),
(79, 1),
(80, 1),
(81, 1),
(82, 1),
(83, 1),
(84, 1),
(85, 1),
(86, 1),
(87, 1),
(88, 1),
(89, 1),
(90, 1),
(91, 1),
(92, 1),
(93, 1),
(94, 1),
(95, 1),
(96, 1),
(97, 1),
(98, 1),
(99, 1),
(100, 1),
(101, 1),
(102, 1),
(103, 1),
(104, 1),
(105, 1),
(106, 1),
(107, 1),
(108, 1),
(109, 1),
(110, 1),
(111, 1),
(112, 1),
(113, 1),
(114, 1),
(115, 1),
(116, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_ad_spaces`
--

CREATE TABLE `tbl_ad_spaces` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `ad_featured_section_id` int NOT NULL,
  `ad_image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `web_ad_image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ad_url` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '0-deactive, 1-active',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `page` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'page or screen names',
  `platform` enum('app','web') COLLATE utf8mb4_unicode_ci DEFAULT 'web',
  `placement` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ad_type` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT 'external_link',
  `duration_days` int UNSIGNED NOT NULL DEFAULT '1',
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_authors`
--

CREATE TABLE `tbl_authors` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `bio` text COLLATE utf8mb4_unicode_ci,
  `telegram_link` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `linkedin_link` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `facebook_link` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `whatsapp_link` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('pending','approved','rejected') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending',
  `auto_approve` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_bookmark`
--

CREATE TABLE `tbl_bookmark` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` int NOT NULL,
  `news_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_breaking_news`
--

CREATE TABLE `tbl_breaking_news` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content_value` text COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `summarized_description` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_breaking_news_view`
--

CREATE TABLE `tbl_breaking_news_view` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` int DEFAULT NULL,
  `breaking_news_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_category`
--

CREATE TABLE `tbl_category` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `category_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `row_order` int NOT NULL DEFAULT '0',
  `image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_comment`
--

CREATE TABLE `tbl_comment` (
  `id` bigint UNSIGNED NOT NULL,
  `parent_id` int NOT NULL DEFAULT '0',
  `user_id` int NOT NULL,
  `news_id` int NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '0-unapproved, 1-approved',
  `date` datetime NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_comment_flag`
--

CREATE TABLE `tbl_comment_flag` (
  `id` bigint UNSIGNED NOT NULL,
  `comment_id` int NOT NULL,
  `user_id` int NOT NULL,
  `news_id` int NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` tinyint NOT NULL COMMENT '0-deactive, 1-active',
  `date` datetime NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_comment_like`
--

CREATE TABLE `tbl_comment_like` (
  `id` bigint UNSIGNED NOT NULL,
  `comment_id` int NOT NULL,
  `user_id` int NOT NULL,
  `status` tinyint NOT NULL COMMENT '1-like, 2-dislike',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_comment_notification`
--

CREATE TABLE `tbl_comment_notification` (
  `id` bigint UNSIGNED NOT NULL,
  `master_id` int NOT NULL,
  `user_id` int NOT NULL,
  `sender_id` int NOT NULL,
  `type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_e_news`
--

CREATE TABLE `tbl_e_news` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` bigint UNSIGNED NOT NULL,
  `title` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `thumbnail` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `attachment` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date DEFAULT NULL,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '1-active, 0-deactive',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_featured_sections`
--

CREATE TABLE `tbl_featured_sections` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `title` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `slug` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `short_description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `news_type` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_ids` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'comma separated user_ids of authors',
  `videos_type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `filter_type` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category_ids` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subcategory_ids` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `news_ids` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `style_app` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `style_web` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `row_order` int NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '0-deactive, 1-active',
  `is_based_on_user_choice` tinyint NOT NULL COMMENT '0-filter_section, 1-news from users category',
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `og_image` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_languages`
--

CREATE TABLE `tbl_languages` (
  `id` bigint UNSIGNED NOT NULL,
  `language` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '1-active, 0-deactive',
  `isRTL` tinyint NOT NULL DEFAULT '0' COMMENT '1-yes, 0-no',
  `image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `display_name` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `app_file` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `web_file` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `panel_file` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_languages`
--

INSERT INTO `tbl_languages` (`id`, `language`, `code`, `status`, `isRTL`, `image`, `display_name`, `created_at`, `updated_at`, `app_file`, `web_file`, `panel_file`) VALUES
(1, 'English (US)', 'en', 1, 0, 'flags/en.webp', 'English (US)', '2026-09-28 05:31:11', '2026-09-28 05:31:11', 'en_app.json', 'en_web.json', 'en.json');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_live_streaming`
--

CREATE TABLE `tbl_live_streaming` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `url` text COLLATE utf8mb4_unicode_ci,
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_location`
--

CREATE TABLE `tbl_location` (
  `id` bigint UNSIGNED NOT NULL,
  `location_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `longitude` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_news`
--

CREATE TABLE `tbl_news` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `category_id` int NOT NULL,
  `subcategory_id` int NOT NULL DEFAULT '0',
  `tag_id` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `location_id` int NOT NULL DEFAULT '0',
  `title` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `published_date` date DEFAULT NULL,
  `content_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_value` text COLLATE utf8mb4_unicode_ci,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `summarized_description` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int NOT NULL,
  `admin_id` int NOT NULL,
  `show_till` date DEFAULT NULL,
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '1-active, 0-deactive',
  `is_draft` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0-no, 1-yes',
  `is_clone` int NOT NULL DEFAULT '0',
  `is_comment` tinyint(1) NOT NULL DEFAULT '1' COMMENT '0 - Comments disabled, 1 - Comments enabled',
  `counter` int NOT NULL DEFAULT '0',
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `is_short_news` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0-no, 1-yes'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_news_image`
--

CREATE TABLE `tbl_news_image` (
  `id` bigint UNSIGNED NOT NULL,
  `news_id` int NOT NULL,
  `other_image` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_news_like`
--

CREATE TABLE `tbl_news_like` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` int NOT NULL,
  `news_id` int NOT NULL,
  `status` tinyint NOT NULL COMMENT '1-like, 2-dislike, 0-none',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_news_view`
--

CREATE TABLE `tbl_news_view` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` int DEFAULT NULL,
  `news_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_notifications`
--

CREATE TABLE `tbl_notifications` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL DEFAULT '0',
  `category_id` int NOT NULL DEFAULT '0',
  `subcategory_id` int NOT NULL DEFAULT '0',
  `news_id` int NOT NULL,
  `location_id` int NOT NULL DEFAULT '0',
  `title` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_unicode_ci,
  `type` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category_preference` tinyint(1) NOT NULL DEFAULT '0',
  `date_sent` datetime NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_pages`
--

CREATE TABLE `tbl_pages` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `title` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `page_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `page_content` mediumtext COLLATE utf8mb4_unicode_ci,
  `page_icon` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `og_image` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keywords` text COLLATE utf8mb4_unicode_ci,
  `is_custom` tinyint NOT NULL DEFAULT '1' COMMENT '0-default, 1-custom',
  `is_termspolicy` tinyint NOT NULL DEFAULT '0',
  `is_privacypolicy` tinyint NOT NULL DEFAULT '0',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '0-deactive, 1-active',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_pages`
--

INSERT INTO `tbl_pages` (`id`, `language_id`, `title`, `page_type`, `slug`, `page_content`, `page_icon`, `og_image`, `schema_markup`, `meta_title`, `meta_description`, `meta_keywords`, `is_custom`, `is_termspolicy`, `is_privacypolicy`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'Privacy Policy', 'privacy-policy', 'privacy-policy', '<p style=\"text-align: left;\">NEWS APP &amp; CONTENT POLICY</p>', '', '', '', '', 'Privacy Policy', 'Policy', 0, 0, 1, 1, '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(2, 1, 'Terms & Conditions', 'terms-condition', 'terms-condition', '<p style=\"text-align: left;\"><strong>1. Terms Conditions</strong></p>', '', '', '', '', 'Terms & Conditions', 'Terms', 0, 1, 0, 1, '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(3, 1, 'Contact Us', 'contact-us', 'contact-us', '<p style=\"text-align: center;\"><strong>How can we help you?</strong></p>', '', '', '', '', 'Contact Us', 'Contact', 0, 0, 0, 1, '2026-09-28 05:31:11', '2026-09-28 05:31:11'),
(4, 1, 'About Us', 'about-us', 'about-us', '<p><strong>About Us:</strong></p>', '', '', '', '', 'About Us', 'About', 0, 0, 0, 1, '2026-09-28 05:31:11', '2026-09-28 05:31:11');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_rss`
--

CREATE TABLE `tbl_rss` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `category_id` int NOT NULL,
  `subcategory_id` int NOT NULL DEFAULT '0',
  `tag_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `feed_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `feed_url` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '1-active, 0-deactive',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `last_fetched_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_settings`
--

CREATE TABLE `tbl_settings` (
  `id` bigint UNSIGNED NOT NULL,
  `type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_settings`
--

INSERT INTO `tbl_settings` (`id`, `type`, `message`, `created_at`, `updated_at`) VALUES
(1, 'rss_feed_mode', '1', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(2, 'mobile_login_mode', '0', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(3, 'country_code', 'IN', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(4, 'shareapp_text', 'You can find our app from below url', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(5, 'appstore_app_id', '', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(6, 'association_file', '', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(7, 'assetlinks_file', '', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(8, 'views_auth_mode', '1', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(9, 'video_type_preference', 'normal_style', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(10, 'auth_short_video_views', '0', '2026-09-28 05:31:10', '2026-09-28 05:31:10'),
(11, 'news_buzz_mode', '1', '2026-09-28 05:31:10', '2026-09-28 05:31:10'),
(12, 'podcast_mode', '1', '2026-09-28 05:31:10', '2026-09-28 05:31:10'),
(13, 'ad_after_page_clicks', '1', '2026-09-28 05:31:10', '2026-09-28 05:31:10'),
(14, 'youtube_api_key', '', '2026-09-28 05:31:10', '2026-09-28 05:31:10'),
(15, 'finnhub_api_key', '', '2026-09-28 05:31:10', '2026-09-28 05:31:10'),
(16, 'twelvedata_api_key', '', '2026-09-28 05:31:10', '2026-09-28 05:31:10'),
(17, 'app_version', '4.1.0', NULL, NULL),
(18, 'default_language', '1', NULL, NULL),
(19, 'system_timezone', 'Asia/Kolkata', NULL, NULL),
(20, 'app_name', 'News', NULL, NULL),
(21, 'primary_color', '#E00000', NULL, NULL),
(22, 'secondary_color', '#ba2028', NULL, NULL),
(23, 'auto_delete_expire_news_mode', '0', NULL, NULL),
(24, 'app_logo_full', 'panel/logo.png', NULL, NULL),
(25, 'app_logo', 'panel/favicon.png', NULL, NULL),
(26, 'smtp_host', 'smtp.googlemail.com', NULL, NULL),
(27, 'smtp_user', 'SMTP User', NULL, NULL),
(28, 'smtp_password', 'SMTP Password', NULL, NULL),
(29, 'smtp_port', '465', NULL, NULL),
(30, 'smtp_crypto', 'tls', NULL, NULL),
(31, 'from_name', 'News', NULL, NULL),
(32, 'category_mode', '1', NULL, NULL),
(33, 'subcategory_mode', '1', NULL, NULL),
(34, 'breaking_news_mode', '1', NULL, NULL),
(35, 'live_streaming_mode', '1', NULL, NULL),
(36, 'comments_mode', '1', NULL, NULL),
(37, 'weather_mode', '0', NULL, NULL),
(38, 'location_news_mode', '0', NULL, NULL),
(39, 'nearest_location_measure', '1000', NULL, NULL),
(40, 'maintenance_mode', '0', NULL, NULL),
(41, 'in_app_ads_mode', '0', NULL, NULL),
(42, 'ads_type', '1', NULL, NULL),
(43, 'google_rewarded_video_id', 'google Rewarded Video Id', NULL, NULL),
(44, 'google_interstitial_id', 'google Interstitial Id', NULL, NULL),
(45, 'google_banner_id', 'google Banner Id', NULL, NULL),
(46, 'google_native_unit_id', 'google Native Unit Id', NULL, NULL),
(47, 'unity_rewarded_video_id', '1', NULL, NULL),
(48, 'unity_interstitial_id', '1', NULL, NULL),
(49, 'unity_banner_id', '1', NULL, NULL),
(50, 'android_game_id', '1', NULL, NULL),
(51, 'ios_in_app_ads_mode', '0', NULL, NULL),
(52, 'ios_ads_type', '1', NULL, NULL),
(53, 'ios_google_rewarded_video_id', 'google Rewarded Video Id', NULL, NULL),
(54, 'ios_google_interstitial_id', 'google Interstitial Id', NULL, NULL),
(55, 'ios_google_banner_id', 'google Banner Id', NULL, NULL),
(56, 'ios_google_native_unit_id', 'google Native Unit Id', NULL, NULL),
(57, 'ios_unity_rewarded_video_id', '1', NULL, NULL),
(58, 'ios_unity_interstitial_id', '1', NULL, NULL),
(59, 'ios_unity_banner_id', '1', NULL, NULL),
(60, 'ios_game_id', '1', NULL, NULL),
(61, 'force_update_app_mode', '0', NULL, NULL),
(62, 'android_app_version', '1.0.0', NULL, NULL),
(63, 'ios_app_version', '1.0.0', NULL, NULL),
(64, 'google_gemini_api_key', '', NULL, NULL),
(65, 'google_app_open_unit_id', 'google App Open Unit Id', NULL, NULL),
(66, 'ios_google_app_open_unit_id', 'google App Open Unit Id', NULL, NULL),
(67, 'e_news_mode', '1', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_social_media`
--

CREATE TABLE `tbl_social_media` (
  `id` bigint UNSIGNED NOT NULL,
  `image` char(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `link` char(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `row_order` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_subcategory`
--

CREATE TABLE `tbl_subcategory` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `category_id` int NOT NULL,
  `subcategory_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `row_order` int NOT NULL DEFAULT '0',
  `image` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_survey_option`
--

CREATE TABLE `tbl_survey_option` (
  `id` bigint UNSIGNED NOT NULL,
  `question_id` int NOT NULL,
  `options` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `counter` int NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_survey_question`
--

CREATE TABLE `tbl_survey_question` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `question` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_survey_result`
--

CREATE TABLE `tbl_survey_result` (
  `id` bigint UNSIGNED NOT NULL,
  `question_id` int NOT NULL,
  `option_id` int NOT NULL,
  `user_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_tag`
--

CREATE TABLE `tbl_tag` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int NOT NULL,
  `tag_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `meta_title` text COLLATE utf8mb4_unicode_ci,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `og_image` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_token`
--

CREATE TABLE `tbl_token` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `token` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `language_id` int DEFAULT NULL,
  `latitude` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `longitude` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_users`
--

CREATE TABLE `tbl_users` (
  `id` bigint UNSIGNED NOT NULL,
  `firebase_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profile` text COLLATE utf8mb4_unicode_ci,
  `fcm_id` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '1-active, 0-deactive',
  `date` datetime NOT NULL,
  `is_author` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0-no, 1-yes',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_users_category`
--

CREATE TABLE `tbl_users_category` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` int NOT NULL,
  `category_id` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_user_roles`
--

CREATE TABLE `tbl_user_roles` (
  `id` bigint UNSIGNED NOT NULL,
  `role` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_web_seo_pages`
--

CREATE TABLE `tbl_web_seo_pages` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` int DEFAULT NULL,
  `page_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `og_image` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `meta_title` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `meta_description` text COLLATE utf8mb4_unicode_ci,
  `meta_keyword` text COLLATE utf8mb4_unicode_ci,
  `schema_markup` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_web_settings`
--

CREATE TABLE `tbl_web_settings` (
  `id` bigint UNSIGNED NOT NULL,
  `type` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_web_settings`
--

INSERT INTO `tbl_web_settings` (`id`, `type`, `message`, `created_at`, `updated_at`) VALUES
(1, 'web_name', 'News', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(2, 'light_body_color', '#f5f5f5', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(3, 'light_hover_color', '#122342', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(4, 'light_primary_color', '#ee2934', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(5, 'light_secondary_color', '#1a2e51', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(6, 'light_text_primary_color', '#0f1f40', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(7, 'light_text_secondary_color', '#65686d', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(8, 'light_header_logo', 'logos/header-logo.svg', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(9, 'light_footer_logo', 'logos/footer-logo.svg', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(10, 'light_placeholder_image', 'logos/placeholder.png', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(11, 'dark_body_color', '#0a1935', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(12, 'dark_hover_color', '#15346d', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(13, 'dark_primary_color', '#ce2b2b', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(14, 'dark_secondary_color', '#122342', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(15, 'dark_text_primary_color', '#ffffff', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(16, 'dark_text_secondary_color', '#98a2b3', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(17, 'dark_header_logo', 'logos/header-logo-dark.svg', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(18, 'dark_footer_logo', 'logos/footer-logo-dark.svg', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(19, 'dark_placeholder_image', 'logos/placeholder-dark.png', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(20, 'favicon_icon', 'logos/favicon-icon.png', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(21, 'web_footer_description', 'News Web website is an online platform that provides news and information about various topics, including current events, entertainment, politics, sports, technology, and more.', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(22, 'google_adsense', '', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(23, 'android_app_link', '', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(24, 'ios_app_link', '', '2026-09-28 05:31:09', '2026-09-28 05:31:09'),
(25, 'accept_cookie', '0', '2026-09-28 05:31:09', '2026-09-28 05:31:09');

-- --------------------------------------------------------

--
-- Table structure for table `video_shorts`
--

CREATE TABLE `video_shorts` (
  `id` bigint UNSIGNED NOT NULL,
  `language_id` bigint UNSIGNED DEFAULT NULL,
  `category_id` bigint UNSIGNED DEFAULT NULL,
  `title` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `video_type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'video_upload',
  `video_url` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `published_date` timestamp NULL DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `views_count` bigint UNSIGNED NOT NULL DEFAULT '0',
  `shares_count` bigint UNSIGNED NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `video_shorts_comments`
--

CREATE TABLE `video_shorts_comments` (
  `id` bigint UNSIGNED NOT NULL,
  `video_shorts_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `comment` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `video_shorts_likes`
--

CREATE TABLE `video_shorts_likes` (
  `id` bigint UNSIGNED NOT NULL,
  `video_shorts_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `like` tinyint(1) NOT NULL DEFAULT '0',
  `dislike` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `alerts`
--
ALTER TABLE `alerts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `episode_bookmarks`
--
ALTER TABLE `episode_bookmarks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `episode_bookmarks_episode_id_foreign` (`episode_id`),
  ADD KEY `episode_bookmarks_user_id_foreign` (`user_id`);

--
-- Indexes for table `episode_play_history`
--
ALTER TABLE `episode_play_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `episode_play_history_episode_id_foreign` (`episode_id`),
  ADD KEY `episode_play_history_user_id_foreign` (`user_id`);

--
-- Indexes for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indexes for table `featured_section_rss_feeds`
--
ALTER TABLE `featured_section_rss_feeds`
  ADD PRIMARY KEY (`id`),
  ADD KEY `featured_section_rss_feeds_featured_section_id_foreign` (`featured_section_id`),
  ADD KEY `featured_section_rss_feeds_rss_feed_id_foreign` (`rss_feed_id`);

--
-- Indexes for table `feed_items`
--
ALTER TABLE `feed_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `feed_items_guid_rss_source_unique` (`guid`,`rss_source_id`),
  ADD KEY `feed_items_rss_source_id_published_at_index` (`rss_source_id`,`published_at`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobs_queue_index` (`queue`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `model_has_permissions`
--
ALTER TABLE `model_has_permissions`
  ADD PRIMARY KEY (`permission_id`,`model_id`,`model_type`),
  ADD KEY `model_has_permissions_model_id_model_type_index` (`model_id`,`model_type`);

--
-- Indexes for table `model_has_roles`
--
ALTER TABLE `model_has_roles`
  ADD PRIMARY KEY (`role_id`,`model_id`,`model_type`),
  ADD KEY `model_has_roles_model_id_model_type_index` (`model_id`,`model_type`);

--
-- Indexes for table `notification_preferences`
--
ALTER TABLE `notification_preferences`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `notification_preferences_user_id_notification_type_id_unique` (`user_id`,`notification_type_id`),
  ADD KEY `notification_preferences_notification_type_id_foreign` (`notification_type_id`);

--
-- Indexes for table `notification_types`
--
ALTER TABLE `notification_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `notification_types_key_unique` (`key`);

--
-- Indexes for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD KEY `password_resets_email_index` (`email`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `permissions_name_guard_name_unique` (`name`,`guard_name`);

--
-- Indexes for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `personal_access_tokens_token_unique` (`token`),
  ADD KEY `personal_access_tokens_tokenable_type_tokenable_id_index` (`tokenable_type`,`tokenable_id`);

--
-- Indexes for table `podcasts`
--
ALTER TABLE `podcasts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `podcasts_slug_unique` (`slug`),
  ADD KEY `podcasts_user_id_foreign` (`user_id`);

--
-- Indexes for table `podcast_episodes`
--
ALTER TABLE `podcast_episodes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `podcast_episodes_slug_unique` (`slug`),
  ADD KEY `podcast_episodes_podcast_id_foreign` (`podcast_id`);

--
-- Indexes for table `podcast_follows`
--
ALTER TABLE `podcast_follows`
  ADD PRIMARY KEY (`id`),
  ADD KEY `podcast_follows_podcast_id_foreign` (`podcast_id`),
  ADD KEY `podcast_follows_user_id_foreign` (`user_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `roles_name_guard_name_unique` (`name`,`guard_name`);

--
-- Indexes for table `role_has_permissions`
--
ALTER TABLE `role_has_permissions`
  ADD PRIMARY KEY (`permission_id`,`role_id`),
  ADD KEY `role_has_permissions_role_id_foreign` (`role_id`);

--
-- Indexes for table `tbl_ad_spaces`
--
ALTER TABLE `tbl_ad_spaces`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`);

--
-- Indexes for table `tbl_authors`
--
ALTER TABLE `tbl_authors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tbl_authors_user_id_foreign` (`user_id`);

--
-- Indexes for table `tbl_bookmark`
--
ALTER TABLE `tbl_bookmark`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `news_id` (`news_id`);

--
-- Indexes for table `tbl_breaking_news`
--
ALTER TABLE `tbl_breaking_news`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`),
  ADD KEY `slug` (`slug`);

--
-- Indexes for table `tbl_breaking_news_view`
--
ALTER TABLE `tbl_breaking_news_view`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `breaking_news_id` (`breaking_news_id`);

--
-- Indexes for table `tbl_category`
--
ALTER TABLE `tbl_category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`),
  ADD KEY `slug` (`slug`),
  ADD KEY `row_order` (`row_order`);

--
-- Indexes for table `tbl_comment`
--
ALTER TABLE `tbl_comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `news_id` (`news_id`);

--
-- Indexes for table `tbl_comment_flag`
--
ALTER TABLE `tbl_comment_flag`
  ADD PRIMARY KEY (`id`),
  ADD KEY `comment_id` (`comment_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `news_id` (`news_id`);

--
-- Indexes for table `tbl_comment_like`
--
ALTER TABLE `tbl_comment_like`
  ADD PRIMARY KEY (`id`),
  ADD KEY `comment_id` (`comment_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `status` (`status`);

--
-- Indexes for table `tbl_comment_notification`
--
ALTER TABLE `tbl_comment_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `master_id` (`master_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `sender_id` (`sender_id`);

--
-- Indexes for table `tbl_e_news`
--
ALTER TABLE `tbl_e_news`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tbl_e_news_language_id_foreign` (`language_id`),
  ADD KEY `slug` (`slug`);

--
-- Indexes for table `tbl_featured_sections`
--
ALTER TABLE `tbl_featured_sections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`);

--
-- Indexes for table `tbl_languages`
--
ALTER TABLE `tbl_languages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `code` (`code`);

--
-- Indexes for table `tbl_live_streaming`
--
ALTER TABLE `tbl_live_streaming`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`);

--
-- Indexes for table `tbl_location`
--
ALTER TABLE `tbl_location`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_news`
--
ALTER TABLE `tbl_news`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `subcategory_id` (`subcategory_id`),
  ADD KEY `location_id` (`location_id`),
  ADD KEY `slug` (`slug`),
  ADD KEY `published_date` (`published_date`),
  ADD KEY `status` (`status`);

--
-- Indexes for table `tbl_news_image`
--
ALTER TABLE `tbl_news_image`
  ADD PRIMARY KEY (`id`),
  ADD KEY `news_id` (`news_id`);

--
-- Indexes for table `tbl_news_like`
--
ALTER TABLE `tbl_news_like`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `news_id` (`news_id`),
  ADD KEY `status` (`status`);

--
-- Indexes for table `tbl_news_view`
--
ALTER TABLE `tbl_news_view`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `news_id` (`news_id`);

--
-- Indexes for table `tbl_notifications`
--
ALTER TABLE `tbl_notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `subcategory_id` (`subcategory_id`),
  ADD KEY `location_id` (`location_id`);

--
-- Indexes for table `tbl_pages`
--
ALTER TABLE `tbl_pages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`);

--
-- Indexes for table `tbl_rss`
--
ALTER TABLE `tbl_rss`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `subcategory_id` (`subcategory_id`),
  ADD KEY `status` (`status`);

--
-- Indexes for table `tbl_settings`
--
ALTER TABLE `tbl_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_social_media`
--
ALTER TABLE `tbl_social_media`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_subcategory`
--
ALTER TABLE `tbl_subcategory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `slug` (`slug`),
  ADD KEY `row_order` (`row_order`);

--
-- Indexes for table `tbl_survey_option`
--
ALTER TABLE `tbl_survey_option`
  ADD PRIMARY KEY (`id`),
  ADD KEY `question_id` (`question_id`);

--
-- Indexes for table `tbl_survey_question`
--
ALTER TABLE `tbl_survey_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`);

--
-- Indexes for table `tbl_survey_result`
--
ALTER TABLE `tbl_survey_result`
  ADD PRIMARY KEY (`id`),
  ADD KEY `question_id` (`question_id`),
  ADD KEY `option_id` (`option_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tbl_tag`
--
ALTER TABLE `tbl_tag`
  ADD PRIMARY KEY (`id`),
  ADD KEY `language_id` (`language_id`),
  ADD KEY `slug` (`slug`);

--
-- Indexes for table `tbl_token`
--
ALTER TABLE `tbl_token`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tbl_token_user_id_index` (`user_id`);

--
-- Indexes for table `tbl_users`
--
ALTER TABLE `tbl_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tbl_users_slug_unique` (`slug`);

--
-- Indexes for table `tbl_users_category`
--
ALTER TABLE `tbl_users_category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tbl_user_roles`
--
ALTER TABLE `tbl_user_roles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_web_seo_pages`
--
ALTER TABLE `tbl_web_seo_pages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `page_type` (`page_type`);

--
-- Indexes for table `tbl_web_settings`
--
ALTER TABLE `tbl_web_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `video_shorts`
--
ALTER TABLE `video_shorts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `video_shorts_slug_unique` (`slug`),
  ADD KEY `video_shorts_language_id_foreign` (`language_id`),
  ADD KEY `video_shorts_category_id_foreign` (`category_id`);

--
-- Indexes for table `video_shorts_comments`
--
ALTER TABLE `video_shorts_comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `video_shorts_comments_video_shorts_id_foreign` (`video_shorts_id`),
  ADD KEY `video_shorts_comments_user_id_foreign` (`user_id`);

--
-- Indexes for table `video_shorts_likes`
--
ALTER TABLE `video_shorts_likes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `video_shorts_likes_video_shorts_id_user_id_unique` (`video_shorts_id`,`user_id`),
  ADD KEY `video_shorts_likes_user_id_foreign` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `alerts`
--
ALTER TABLE `alerts`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `episode_bookmarks`
--
ALTER TABLE `episode_bookmarks`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `episode_play_history`
--
ALTER TABLE `episode_play_history`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `featured_section_rss_feeds`
--
ALTER TABLE `featured_section_rss_feeds`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `feed_items`
--
ALTER TABLE `feed_items`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `notification_preferences`
--
ALTER TABLE `notification_preferences`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notification_types`
--
ALTER TABLE `notification_types`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=117;

--
-- AUTO_INCREMENT for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `podcasts`
--
ALTER TABLE `podcasts`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `podcast_episodes`
--
ALTER TABLE `podcast_episodes`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `podcast_follows`
--
ALTER TABLE `podcast_follows`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tbl_ad_spaces`
--
ALTER TABLE `tbl_ad_spaces`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_authors`
--
ALTER TABLE `tbl_authors`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_bookmark`
--
ALTER TABLE `tbl_bookmark`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_breaking_news`
--
ALTER TABLE `tbl_breaking_news`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_breaking_news_view`
--
ALTER TABLE `tbl_breaking_news_view`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_category`
--
ALTER TABLE `tbl_category`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_comment`
--
ALTER TABLE `tbl_comment`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_comment_flag`
--
ALTER TABLE `tbl_comment_flag`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_comment_like`
--
ALTER TABLE `tbl_comment_like`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_comment_notification`
--
ALTER TABLE `tbl_comment_notification`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_e_news`
--
ALTER TABLE `tbl_e_news`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_featured_sections`
--
ALTER TABLE `tbl_featured_sections`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_languages`
--
ALTER TABLE `tbl_languages`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tbl_live_streaming`
--
ALTER TABLE `tbl_live_streaming`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_location`
--
ALTER TABLE `tbl_location`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_news`
--
ALTER TABLE `tbl_news`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_news_image`
--
ALTER TABLE `tbl_news_image`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_news_like`
--
ALTER TABLE `tbl_news_like`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_news_view`
--
ALTER TABLE `tbl_news_view`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_notifications`
--
ALTER TABLE `tbl_notifications`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_pages`
--
ALTER TABLE `tbl_pages`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tbl_rss`
--
ALTER TABLE `tbl_rss`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_settings`
--
ALTER TABLE `tbl_settings`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT for table `tbl_social_media`
--
ALTER TABLE `tbl_social_media`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_subcategory`
--
ALTER TABLE `tbl_subcategory`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_survey_option`
--
ALTER TABLE `tbl_survey_option`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_survey_question`
--
ALTER TABLE `tbl_survey_question`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_survey_result`
--
ALTER TABLE `tbl_survey_result`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_tag`
--
ALTER TABLE `tbl_tag`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_token`
--
ALTER TABLE `tbl_token`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_users`
--
ALTER TABLE `tbl_users`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_users_category`
--
ALTER TABLE `tbl_users_category`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_user_roles`
--
ALTER TABLE `tbl_user_roles`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_web_seo_pages`
--
ALTER TABLE `tbl_web_seo_pages`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_web_settings`
--
ALTER TABLE `tbl_web_settings`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `video_shorts`
--
ALTER TABLE `video_shorts`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `video_shorts_comments`
--
ALTER TABLE `video_shorts_comments`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `video_shorts_likes`
--
ALTER TABLE `video_shorts_likes`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `episode_bookmarks`
--
ALTER TABLE `episode_bookmarks`
  ADD CONSTRAINT `episode_bookmarks_episode_id_foreign` FOREIGN KEY (`episode_id`) REFERENCES `podcast_episodes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `episode_bookmarks_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `episode_play_history`
--
ALTER TABLE `episode_play_history`
  ADD CONSTRAINT `episode_play_history_episode_id_foreign` FOREIGN KEY (`episode_id`) REFERENCES `podcast_episodes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `episode_play_history_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `featured_section_rss_feeds`
--
ALTER TABLE `featured_section_rss_feeds`
  ADD CONSTRAINT `featured_section_rss_feeds_featured_section_id_foreign` FOREIGN KEY (`featured_section_id`) REFERENCES `tbl_featured_sections` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `featured_section_rss_feeds_rss_feed_id_foreign` FOREIGN KEY (`rss_feed_id`) REFERENCES `tbl_rss` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `feed_items`
--
ALTER TABLE `feed_items`
  ADD CONSTRAINT `feed_items_rss_source_id_foreign` FOREIGN KEY (`rss_source_id`) REFERENCES `tbl_rss` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `model_has_permissions`
--
ALTER TABLE `model_has_permissions`
  ADD CONSTRAINT `model_has_permissions_permission_id_foreign` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `model_has_roles`
--
ALTER TABLE `model_has_roles`
  ADD CONSTRAINT `model_has_roles_role_id_foreign` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `notification_preferences`
--
ALTER TABLE `notification_preferences`
  ADD CONSTRAINT `notification_preferences_notification_type_id_foreign` FOREIGN KEY (`notification_type_id`) REFERENCES `notification_types` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notification_preferences_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `podcasts`
--
ALTER TABLE `podcasts`
  ADD CONSTRAINT `podcasts_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `podcast_episodes`
--
ALTER TABLE `podcast_episodes`
  ADD CONSTRAINT `podcast_episodes_podcast_id_foreign` FOREIGN KEY (`podcast_id`) REFERENCES `podcasts` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `podcast_follows`
--
ALTER TABLE `podcast_follows`
  ADD CONSTRAINT `podcast_follows_podcast_id_foreign` FOREIGN KEY (`podcast_id`) REFERENCES `podcasts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `podcast_follows_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `role_has_permissions`
--
ALTER TABLE `role_has_permissions`
  ADD CONSTRAINT `role_has_permissions_permission_id_foreign` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `role_has_permissions_role_id_foreign` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `tbl_authors`
--
ALTER TABLE `tbl_authors`
  ADD CONSTRAINT `tbl_authors_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `tbl_e_news`
--
ALTER TABLE `tbl_e_news`
  ADD CONSTRAINT `tbl_e_news_language_id_foreign` FOREIGN KEY (`language_id`) REFERENCES `tbl_languages` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `tbl_token`
--
ALTER TABLE `tbl_token`
  ADD CONSTRAINT `tbl_token_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `video_shorts`
--
ALTER TABLE `video_shorts`
  ADD CONSTRAINT `video_shorts_category_id_foreign` FOREIGN KEY (`category_id`) REFERENCES `tbl_category` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `video_shorts_language_id_foreign` FOREIGN KEY (`language_id`) REFERENCES `tbl_languages` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `video_shorts_comments`
--
ALTER TABLE `video_shorts_comments`
  ADD CONSTRAINT `video_shorts_comments_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `video_shorts_comments_video_shorts_id_foreign` FOREIGN KEY (`video_shorts_id`) REFERENCES `video_shorts` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `video_shorts_likes`
--
ALTER TABLE `video_shorts_likes`
  ADD CONSTRAINT `video_shorts_likes_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `video_shorts_likes_video_shorts_id_foreign` FOREIGN KEY (`video_shorts_id`) REFERENCES `video_shorts` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
