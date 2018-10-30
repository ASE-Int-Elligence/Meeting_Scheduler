create database IF NOT EXISTS `ase_project_db`;
USE `ase_project_db`;

CREATE TABLE IF NOT EXISTS `user_credentials` (
    `username` varchar(50) DEFAULT NULL,
    `nameFirst` varchar(50) DEFAULT NULL,
    `nameLast` varchar(50) DEFAULT NULL,
    `password` varchar(50) DEFAULT NULL,
    `email` varchar(150) DEFAULT NULL,
    `DOB` date DEFAULT NULL
);

