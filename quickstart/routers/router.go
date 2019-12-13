package routers

import (
	"quickstart/controllers"
	"github.com/astaxie/beego"
)

func init() {
    beego.Router("/", &controllers.MainController{})
	beego.Router("/abc", &controllers.MainController{})
	beego.Router("/hello",&controllers.MainController{},"get:AbcGet")
	beego.Router("/mjt",&controllers.LoggerController{},"get:Get")
	beego.Router("/api",&controllers.LoggerController{},"get:Test")
}







