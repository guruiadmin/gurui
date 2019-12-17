package routers

import (
	"beego-admin/controllers"
	"github.com/astaxie/beego"
)

func init() {

	/*
		菜单管理   平台一级菜单管理
	*/
	beego.Router("/menu/onelist", &controllers.MenuController{}, "get:OneList")
	beego.Router("/menu/onelistadd", &controllers.MenuController{}, "get:OneListAdd")
	beego.Router("/menu/onelistaddto", &controllers.MenuController{}, "post:OneListAddTo")
	beego.Router("/menu/onelistdelete", &controllers.MenuController{}, "post:OneListDelete")
	beego.Router("/menu/onedata", &controllers.MenuController{}, "get:OneData")

	/*
		菜单管理   平台二级菜单管理
	*/
	beego.Router("/menu/twolist", &controllers.MenuController{}, "get:TwoList")
	beego.Router("/menu/twolistadd", &controllers.MenuController{}, "get:TwoListAdd")
	beego.Router("/menu/twolistaddto", &controllers.MenuController{}, "post:TwoListAddTo")
	beego.Router("/menu/twolistdelete", &controllers.MenuController{}, "post:TwoListDelete")
	beego.Router("/menu/twodata", &controllers.MenuController{}, "get:TwoData")

}
