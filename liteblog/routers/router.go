package routers

import (
	"liteblog/controllers"
	"github.com/astaxie/beego"
)

func init() {
	beego.Include(&controllers.IndexController{})
}
