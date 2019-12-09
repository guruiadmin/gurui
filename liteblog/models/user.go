package models

import "github.com/jinzhu/gorm"

//用户表
type User struct {
	gorm.Model
	Name   string `gorm:"unique_index"`
	Email  string `gorm:"unique_index"`
	Pwd string
	Avatar string
	Role int `gorm:"default:0"`
}

