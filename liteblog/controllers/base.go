package controllers

import (
	"github.com/astaxie/beego"
	"liteblog/models"
)

const SESSION_USER_KEY  = "SESSION_USER_KEY"

type BaseControllers struct {
	beego.Controller
	User models.User
	IsLogin bool
}

func (this *BaseControllers) Prepare() {
	this.Data["Path"] = this.Ctx.Request.RequestURI
	u, ok := this.GetSession(SESSION_USER_KEY).(models.User)
	this.IsLogin = false
	if ok{
		this.User = u
		this.IsLogin = true
		this.Data["User"] = this.User
	}
}

func (this *BaseControllers) Abort500(err error) {
	this.Data["error"] = err
	this.Abort("500")
}

