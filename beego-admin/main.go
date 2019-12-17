package main

import (
	_ "beego-admin/conf"
	"beego-admin/models"
	_ "beego-admin/models"
	_ "beego-admin/routers"
	"encoding/gob"

	//"encoding/gob"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	_ "github.com/astaxie/beego/session/redis"
)

func init() {
	//创建数据库表
	orm.RunSyncdb("default", false, true)
	//redis session注册
	gob.Register(models.User{})
	gob.Register([]*models.One{})
}

func main() {
	beego.Run()
}
