package routers

import (
	"report/controllers"
	"github.com/astaxie/beego"
)

func init() {
    beego.Router("/", &controllers.MainController{})
	//beego.Router("/api",&controllers.MainController{},"get:GoodsGet")
	beego.Router("/login",&controllers.Basecontroller{}, )
	beego.Router("/business",&controllers.Bbasecontroller{}, )
	beego.Router("/personnel",&controllers.Pbasecontroller{}, "get:Getpersonnel" )
	beego.Router("/details",&controllers.Pbasecontroller{}, "get:Getdetails" )
}
