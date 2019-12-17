package controllers

import (
	"beego-admin/models"
	"encoding/json"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
)

type LoginController struct {
	BaseController
}

/*
	跳转登录页面
*/
func (This *LoginController) Get() {
	_, err := This.CheckLogin()
	if err {
		This.Redirect("/", 302)
		This.StopRun()
	}
	This.TplName = "login.html"
}

/*
	接受登录验证返回参数
*/
type LoginUser struct {
	Username string
	Password string
}

/*
	登录验证
*/
func (This *LoginController) Post() {
	var loginUser LoginUser
	var err error
	err = json.Unmarshal(This.Ctx.Input.RequestBody, &loginUser)
	if err != nil {
		logs.Error(err)
		This.Data["json"] = map[string]string{"code": "1", "msg": "登录失败！！！"}
	}
	o := orm.NewOrm()
	var user models.User
	err = o.Raw("select id, username from menu_user where username = '" + loginUser.Username + "' and password = '" + loginUser.Password + "' and status = 0").QueryRow(&user)
	if err != nil {
		logs.Error(err)
		This.Data["json"] = map[string]string{"code": "1", "msg": "登录失败，用户名或密码错误或此用户已被禁用，请联系管理员！！！"}
		return
	}
	This.SetSession("LoginUser", user)
	This.SessionLeftNav(user.Id)
	This.Data["json"] = map[string]string{"code": "0", "msg": "登录成功！！！"}
	This.ServeJSON()
	This.StopRun()
}

/*
	退出
*/
func (this *LoginController) Quit() {
	this.DestroySession()
	this.Redirect("/login", 302)
	this.StopRun()
}
