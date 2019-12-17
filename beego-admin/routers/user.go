package routers

import (
	"beego-admin/controllers"
	"github.com/astaxie/beego"
)

func init() {

	/*
		用户管理   平台用户管理
	*/
	beego.Router("/user/userlist", &controllers.UserController{}, "get:UserList")
	beego.Router("/user/userlistadd", &controllers.UserController{}, "get:UserListAdd")
	beego.Router("/user/userlistaddto", &controllers.UserController{}, "post:UserListAddTo")
	beego.Router("/user/userlistdelete", &controllers.UserController{}, "post:UserListDelete")
	beego.Router("/user/userdata", &controllers.UserController{}, "get:UserData")

	/*
		用户管理   平台权限管理
	*/
	beego.Router("/user/rolelist", &controllers.UserController{}, "get:RoleList")
	beego.Router("/user/rolelistadd", &controllers.UserController{}, "get:RoleListAdd")
	beego.Router("/user/rolelistaddto", &controllers.UserController{}, "post:RoleListAddTo")
	beego.Router("/user/rolelistdelete", &controllers.UserController{}, "post:RoleListDelete")
	beego.Router("/user/roledata", &controllers.UserController{}, "get:RoleData")

}
