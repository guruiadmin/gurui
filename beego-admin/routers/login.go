package routers

import (
	"beego-admin/controllers"
	"github.com/astaxie/beego"
)

func init() {
	//登录
	beego.Router("/login", &controllers.LoginController{})
	//退出
	beego.Router("/quit", &controllers.LoginController{}, "get:Quit")
}
