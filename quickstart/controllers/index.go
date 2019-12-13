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


func Select(ids  string) (string, string, string){
	//sqlText := fmt.Sprintf("select foreign_key , name, market_price,brief from goods where foreign_key = '%s'", ids)
	//sqlText1 := fmt.Sprintf("select foreign_key, name from manager where  foreign_key= '%s'", ids)
	sqlText := fmt.Sprintf("SELECT `purchase_order`.`manager_id`, COUNT(`purchase_order`.`order_number`) AS `count`, SUM(`purchase_order`.`actual_price`) AS `money` FROM `purchase_order` WHERE (`purchase_order`.`pay_time` BETWEEN '2019-12-11 16:00:00' AND '2019-12-12 15:59:59' AND `purchase_order`.`pay_state` = 1 AND `purchase_order`.`order_state` = 1) GROUP BY `purchase_order`.`manager_id` ORDER BY NULL")
	sqlText1 := fmt.Sprintf("SELECT `take_order`.`manager_id`, COUNT(`take_order`.`order_number`) AS `count` FROM `take_order` WHERE (NOT (`take_order`.`order_state` = 1) AND `take_order`.`create_date` BETWEEN '2019-12-11 16:00:00' AND '2019-12-12 15:59:59' AND `take_order`.`order_state` = 0 AND `take_order`.`take_state` IN (1, 3, 2, 0)) GROUP BY `take_order`.`manager_id` ORDER BY NULL")
	sqlText2 := fmt.Sprintf("select id, name from manager where name is not null")
	return sqlText, sqlText1,sqlText2
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
	data1, data2, data3 := Select(jsoninfo)
	_, err1 := o.Raw(data1).Values(&maps)
	_, err2 := o.Raw(data2).Values(&maps1)
	_, err3 := o.Raw(data3).Values(&maps1)
	fmt.Println(err3)
	if err1 == nil && err2 == nil{
		for _, i := range maps{
			for _, k := range maps1{
				if i["foreign_key"] == k["foreign_key"]{
					i["manage"] = k["name"]
				}
			}
		}
		data := &RESPONSEJOSN{
			"200",
			"获取成功",
			maps,
		}
		c.Data["json"] = data
	}
	c.ServeJSON()
}



