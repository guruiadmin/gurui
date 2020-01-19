package routers

import (
	"report/controllers"
	"github.com/astaxie/beego"
)

func init() {
    beego.Router("/", &controllers.MainController{})
	//beego.Router("/api",&controllers.MainController{},"get:GoodsGet")
	beego.Router("/login",&controllers.Basecontroller{}, )
}
