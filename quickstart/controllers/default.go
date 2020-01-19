package controllers

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	"quickstart/quickservice"
)

type MainController struct {
	beego.Controller
}


func (c * MainController) AbcGet() {
	c.TplName = "index.tpl"
	//1.有ORM对象
	o := orm.NewOrm()
	var maps []orm.Params
	num, err := o.Raw("select * from goods").Values(&maps)
	if err == nil && num > 0 {
		fmt.Println(maps[1]["name"]) // slene
	}
}

type LIKE struct {
	Name string
	Price string
	Id string
}


type JSONS struct {
	//必须的大写开头
	Code string
	Msg  string
	User []string `json:"user_info"`//key重命名,最外面是反引号
	Like LIKE
}

func (c *MainController) Get() {
	username := c.GetString("user")
	password := c.GetString("pw")
	fmt.Println(username, password)
	if quickservice.ValidateAdminLogin(username, password) {

		c.SetSession("Adminname", username)
		c.Ctx.WriteString("jsoninfo")
	} else {
		c.Ctx.WriteString("jsoninfo is empty")
		//c.TplName = "admin/login.html"
	}
}
