/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50562
Source Host           : 127.0.0.1:3306
Source Database       : sjsq

Target Server Type    : MYSQL
Target Server Version : 50562
File Encoding         : 65001

Date: 2019-06-07 08:43:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for menu_one
-- ----------------------------
DROP TABLE IF EXISTS `menu_one`;
CREATE TABLE `menu_one` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(25) NOT NULL DEFAULT '',
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of menu_one
-- ----------------------------
INSERT INTO `menu_one` VALUES ('1', '菜单管理', '菜单管理');
INSERT INTO `menu_one` VALUES ('2', '用户管理', '用户管理');
INSERT INTO `menu_one` VALUES ('3', '审核管理', '审核管理');
INSERT INTO `menu_one` VALUES ('16', '公司内容管理', '公司内容管理员，填充公司官网内容');

-- ----------------------------
-- Table structure for menu_role
-- ----------------------------
DROP TABLE IF EXISTS `menu_role`;
CREATE TABLE `menu_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL DEFAULT '' COMMENT '角色名',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '角色状态，是否启用，默认为0启用，为1不启用',
  `description` longtext NOT NULL COMMENT '角色说明',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of menu_role
-- ----------------------------
INSERT INTO `menu_role` VALUES ('1', '超级管理员', '0', '平台管理员');
INSERT INTO `menu_role` VALUES ('2', '审核管理员', '0', '审核数据是否可用');
INSERT INTO `menu_role` VALUES ('6', '公司内容管理员', '0', '公司内容管理员');

-- ----------------------------
-- Table structure for menu_role_menu_ones
-- ----------------------------
DROP TABLE IF EXISTS `menu_role_menu_ones`;
CREATE TABLE `menu_role_menu_ones` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `menu_role_id` bigint(20) NOT NULL,
  `menu_one_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of menu_role_menu_ones
-- ----------------------------
INSERT INTO `menu_role_menu_ones` VALUES ('1', '1', '1');
INSERT INTO `menu_role_menu_ones` VALUES ('2', '1', '2');
INSERT INTO `menu_role_menu_ones` VALUES ('3', '1', '3');
INSERT INTO `menu_role_menu_ones` VALUES ('13', '2', '3');
INSERT INTO `menu_role_menu_ones` VALUES ('14', '2', '13');
INSERT INTO `menu_role_menu_ones` VALUES ('18', '1', '16');
INSERT INTO `menu_role_menu_ones` VALUES ('19', '6', '16');

-- ----------------------------
-- Table structure for menu_two
-- ----------------------------
DROP TABLE IF EXISTS `menu_two`;
CREATE TABLE `menu_two` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(25) NOT NULL DEFAULT '',
  `url` varchar(26) NOT NULL DEFAULT '',
  `description` longtext NOT NULL,
  `one_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of menu_two
-- ----------------------------
INSERT INTO `menu_two` VALUES ('1', '平台一级菜单', '/menu/onelist', '平台一级菜单', '1');
INSERT INTO `menu_two` VALUES ('2', '平台二级菜单', '/menu/twolist', '平台二级菜单', '1');
INSERT INTO `menu_two` VALUES ('3', '平台用户管理', '/user/userlist', '用户管理', '2');
INSERT INTO `menu_two` VALUES ('8', '平台角色管理', '/user/rolelist', '角色管理', '2');
INSERT INTO `menu_two` VALUES ('11', '公司内容', '/sjsq/sjsqlist', '公司内容', '16');
INSERT INTO `menu_two` VALUES ('12', '公司内容审核', '/sjsq/reviewlist', '公司内容审核', '3');

-- ----------------------------
-- Table structure for menu_user
-- ----------------------------
DROP TABLE IF EXISTS `menu_user`;
CREATE TABLE `menu_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(25) NOT NULL DEFAULT '' COMMENT '用户登录名',
  `password` varchar(25) NOT NULL DEFAULT '' COMMENT '用户登录密码',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '用户状态，是否启用，默认为0启用，为1不启用',
  `loginip` varchar(25) NOT NULL DEFAULT '' COMMENT '用户登录ip',
  `logintime` datetime NOT NULL COMMENT '用户登录时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of menu_user
-- ----------------------------
INSERT INTO `menu_user` VALUES ('1', 'admin', '123456', '0', '127.0.0.1', '2019-06-02 12:51:56');
INSERT INTO `menu_user` VALUES ('7', 'user', '123456', '0', '', '2019-06-07 00:37:38');
INSERT INTO `menu_user` VALUES ('9', 'data', '123456', '0', '', '2019-06-07 00:40:47');

-- ----------------------------
-- Table structure for menu_user_menu_roles
-- ----------------------------
DROP TABLE IF EXISTS `menu_user_menu_roles`;
CREATE TABLE `menu_user_menu_roles` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `menu_user_id` bigint(20) NOT NULL,
  `menu_role_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of menu_user_menu_roles
-- ----------------------------
INSERT INTO `menu_user_menu_roles` VALUES ('1', '1', '1');
INSERT INTO `menu_user_menu_roles` VALUES ('7', '7', '2');
INSERT INTO `menu_user_menu_roles` VALUES ('9', '9', '6');

-- ----------------------------
-- Table structure for sjsq_one_data
-- ----------------------------
DROP TABLE IF EXISTS `sjsq_one_data`;
CREATE TABLE `sjsq_one_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(25) NOT NULL DEFAULT '' COMMENT '标题',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '审核是否通过，默认为0开启,为1禁用',
  `review` int(11) NOT NULL DEFAULT '0' COMMENT '审核是否通过，默认为0待审核,为1未通过，为2通过',
  `description` longtext NOT NULL COMMENT '介绍',
  `data` longtext NOT NULL COMMENT '内容',
  `username` varchar(25) NOT NULL DEFAULT '' COMMENT '最后一次修改人',
  `updated` datetime NOT NULL COMMENT '最后一次修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sjsq_one_data
-- ----------------------------
INSERT INTO `sjsq_one_data` VALUES ('1', '12412', '0', '2', '21412', '12412<img src=\"/static/img/438ad532-0cb2-49cf-977e-16d645f9bf6fth.jpg\" alt=\"undefined\">', 'admin', '2019-06-06 06:01:35');
INSERT INTO `sjsq_one_data` VALUES ('2', 'test', '0', '0', 'test', '<p style=\"text-align: center;\"><b>test<img src=\"/static/img/91656854-7484-4ac9-af7e-d64dd79dc327th.jpg\" alt=\"undefined\"></b></p>', 'admin', '2019-06-07 00:39:38');
INSERT INTO `sjsq_one_data` VALUES ('3', 'test2', '0', '1', 'test2', '<p>test2</p>', 'data', '2019-06-07 00:41:36');
