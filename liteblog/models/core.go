package models

import (
	"github.com/jinzhu/gorm"
	"os"
	_"github.com/jinzhu/gorm/dialects/sqlite"
)

var (
	db *gorm.DB
)

func init(){
	var err error
	if err = os.MkdirAll("data", 0777);err!=nil{
		panic("failed database"+err.Error())
	}
	db, err = gorm.Open("sqlite3", "data/data.db")
	if err != nil{
		panic("failed to connect database,")
	}
	db.AutoMigrate(&User{})
	var count int
	if err := db.Model(&User{}).Count(&count).Error; err==nil && count==0{
		db.Create(&User{Name: "admin",
			//邮箱
			Email: "admin@qq.com",
			//密码
			Pwd: "123123",
			//头像地址
			Avatar: "/static/images/info-img.png",
			//是否认证 例： lyblog 作者
			Role: 0,
		})
	}
}
