package controllers

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
)

type LoggerController struct {
	beego.Controller
}

type RESPONSEJOSN struct {
	Code string
	Msg  string
	Data []orm.Params
}


func Select(ids  string) (string, string){
	sqlText := fmt.Sprintf("select foreign_key , name, market_price,brief from goods where foreign_key = '%s'", ids)
	sqlText1 := fmt.Sprintf("select foreign_key, name from manager where  foreign_key= '%s'", ids)
	return sqlText, sqlText1
}

func (c *LoggerController) Get() {
	jsoninfo := c.GetString("a")
	if jsoninfo == "" {
		c.Ctx.WriteString("jsoninfo is empty")
		return
	}
	o := orm.NewOrm()
	var maps []orm.Params
	var maps1 []orm.Params
	data1, data2 := Select(jsoninfo)
	_, err1 := o.Raw(data1).Values(&maps)
	_, err2 := o.Raw(data2).Values(&maps1)
	for _, i := range maps{
		for _, k := range maps1{
			if i["foreign_key"] == k["foreign_key"]{
				i["manage"] = k["name"]
			}
		}
	}
	fmt.Println(maps1)
	if err1 == nil && err2 == nil{
		data := &RESPONSEJOSN{
			"200",
			"获取成功",
			maps,
		}
		c.Data["json"] = data
	}
	c.ServeJSON()
}



