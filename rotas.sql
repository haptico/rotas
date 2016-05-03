/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50709
Source Host           : localhost:3306
Source Database       : rotas

Target Server Type    : MYSQL
Target Server Version : 50709
File Encoding         : 65001

Date: 2016-05-02 17:44:05
*/
CREATE DATABASE rotas;
USE rotas;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `mapa`
-- ----------------------------
DROP TABLE IF EXISTS `mapa`;
CREATE TABLE `mapa` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nome_mapa` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of mapa
-- ----------------------------

-- ----------------------------
-- Table structure for `rota`
-- ----------------------------
DROP TABLE IF EXISTS `rota`;
CREATE TABLE `rota` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nome_rota` varchar(512) NOT NULL,
  `inicio` varchar(255) NOT NULL,
  `fim` varchar(255) NOT NULL,
  `autonomia` int(10) unsigned NOT NULL,
  `autonomia_ultima` int(10) unsigned NOT NULL,
  `distancia` int(10) unsigned NOT NULL,
  `id_mapa` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_mapa_rota_id_mapa` (`id_mapa`),
  CONSTRAINT `fk_mapa_rota_id_mapa` FOREIGN KEY (`id_mapa`) REFERENCES `mapa` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of rota
-- ----------------------------

