package controllers

type IndexController struct {
	BaseControllers
}

//@router / [get]
func (this *IndexController) Index(){
	this.TplName = "index.html"
}

//@router /message [get]
func (this *IndexController) IndexMessage(){
	this.Abort("404")
	this.TplName = "message.html"
}


//@router /about [get]
func (this *IndexController) IndexAbout(){
	this.TplName = "about.html"
}

//@router /user [get]
func (this *IndexController) GetUser(){
	this.TplName = "user.html"
}

