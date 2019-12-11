package controllers

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
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
	o := orm.NewOrm()
	var maps []orm.Params
	num, err := o.Raw("select id, name, market_price from goods where name is not null").Values(&maps)
	if err == nil && num > 0 {
		for key, value := range maps{
			fmt.Println(key, value["name"])
			data := &JSONS{
				"100",
				"获取成功",
				[]string{"maple","18"},
				LIKE{"蛋糕","电影","音乐"}}
			c.Data["json"] = data
			c.ServeJSON()
		}
	}
}
