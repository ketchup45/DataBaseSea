/*
 Navicat Premium Data Transfer

 Source Server         : web_db_test
 Source Server Type    : MySQL
 Source Server Version : 80036
 Source Host           : localhost:3306
 Source Schema         : seaice_test

 Target Server Type    : MySQL
 Target Server Version : 80036
 File Encoding         : 65001

 Date: 16/06/2024 13:45:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for detector
-- ----------------------------
DROP TABLE IF EXISTS `detector`;
CREATE TABLE `detector`  (
  `detector_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `detector_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `detector_model` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `user_id` int UNSIGNED NOT NULL,
  PRIMARY KEY (`detector_id`) USING BTREE,
  UNIQUE INDEX `unq_detectorname`(`detector_name` ASC) USING BTREE,
  INDEX `fk_userid`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_userid` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of detector
-- ----------------------------
INSERT INTO `detector` VALUES (1, 'dect1', 'sate1', 2);
INSERT INTO `detector` VALUES (2, 'dect2', 'sate2', 2);

-- ----------------------------
-- Table structure for ice
-- ----------------------------
DROP TABLE IF EXISTS `ice`;
CREATE TABLE `ice`  (
  `ice_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `ice_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ice_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `ice_size` double UNSIGNED NULL DEFAULT NULL,
  `record_id` int UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`ice_id`) USING BTREE,
  UNIQUE INDEX `unq_icename`(`ice_name` ASC) USING BTREE,
  INDEX `fk_recordid`(`record_id` ASC) USING BTREE,
  CONSTRAINT `fk_recordid` FOREIGN KEY (`record_id`) REFERENCES `record` (`record_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ice
-- ----------------------------
INSERT INTO `ice` VALUES (1, 'testice', '尖顶冰山', 123.4, NULL);
INSERT INTO `ice` VALUES (2, 'newice', '尖顶冰山', 345.22, 24);

-- ----------------------------
-- Table structure for record
-- ----------------------------
DROP TABLE IF EXISTS `record`;
CREATE TABLE `record`  (
  `record_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `ice_id` int UNSIGNED NOT NULL,
  `detector_id` int UNSIGNED NOT NULL,
  `latitude` double NOT NULL,
  `longtitude` double NOT NULL,
  `record_time` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`record_id`) USING BTREE,
  INDEX `fk_detectorid`(`detector_id` ASC) USING BTREE,
  INDEX `fk_iceid`(`ice_id` ASC) USING BTREE,
  CONSTRAINT `fk_detectorid` FOREIGN KEY (`detector_id`) REFERENCES `detector` (`detector_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_iceid` FOREIGN KEY (`ice_id`) REFERENCES `ice` (`ice_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of record
-- ----------------------------
INSERT INTO `record` VALUES (1, 1, 1, 74.34, 73.53, '2024-01-15 21:35:07');
INSERT INTO `record` VALUES (2, 1, 1, 77.91, 102.38, '2024-02-15 21:31:26');
INSERT INTO `record` VALUES (3, 1, 1, 74.96, 123.12, '2024-03-15 21:31:40');
INSERT INTO `record` VALUES (4, 1, 1, 72.51, 134.37, '2024-04-15 21:31:30');
INSERT INTO `record` VALUES (5, 1, 1, 71.74, 155.46, '2024-05-15 21:31:28');
INSERT INTO `record` VALUES (6, 1, 1, 71.19, 174.1, '2024-06-15 21:31:26');
INSERT INTO `record` VALUES (24, 2, 2, 20, 34, '2024-06-16 13:16:23');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` int UNSIGNED NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `unq_username`(`user_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'user0', '123456', 0);
INSERT INTO `user` VALUES (2, 'user1', '112233', 1);
INSERT INTO `user` VALUES (3, 'admin', '123456', 2);
INSERT INTO `user` VALUES (9, 'user3', '112233', 1);
INSERT INTO `user` VALUES (10, 'user4', '112233', 1);

SET FOREIGN_KEY_CHECKS = 1;
