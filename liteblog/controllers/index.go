package controllers

import "github.com/astaxie/beego"

type IndexController struct {
	beego.Controller
}

//@router / [get]
func (this *IndexController) Index(){
	this.TplName = "index.html"
}

//@router /message [get]
func (this *IndexController) IndexMessage(){
	this.TplName = "message.html"
}


//@router /about [get]
func (this *IndexController) IndexAbout(){
	this.TplName = "about.html"
}
