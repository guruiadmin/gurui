package controllers

import (
	"beego-admin/models"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
)

type HomeController struct {
	BaseController
}

/*
	返回主页
*/
func (This *HomeController) Home() {
	user, err := This.CheckLogin()
	if err {
		This.Data["user"] = user
		This.Data["ones"] = This.GetSession("LeftNavResult")
		This.TplName = "index.html"
		return
	}
	This.Redirect("/login", 302)
	This.StopRun()
}

/*
	返回我的桌面页面
*/
func (This *HomeController) Welcome() {

	user, ok := This.GetSession("LoginUser").(models.User)
	if !ok {
		logs.Error("转换model.User类型出错了！！！")
	}

	o := orm.NewOrm()
	var err error
	var roles []*models.Role
	_, err = o.Raw("select name, description from menu_role where id in(select menu_role_id from menu_user_menu_roles where menu_user_id = ?)", user.Id).QueryRows(&roles)
	if err != nil {
		logs.Error("查询用户角色出错，错误内容为:", err)
	}
	user.Roles = roles
	This.Data["user"] = user
	This.TplName = "pages/welcome.html"
}
