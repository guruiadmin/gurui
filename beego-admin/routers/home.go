package routers

import (
	"beego-admin/controllers"
	"github.com/astaxie/beego"
)

func init() {
	beego.Router("/", &controllers.HomeController{}, "get:Home")
	beego.Router("/welcome", &controllers.HomeController{}, "get:Welcome")
}
