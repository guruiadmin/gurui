package controllers

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"quickstart/models"
	"time"
)

type LoggerController struct {
	beego.Controller
}


type RESPONSEJOSN struct {
	Code string
	Msg  string
	Data []map[string]string
}


type JSONS11 struct {
	//必须的大写开头
	Code string
	Msg  string
	Num int64
	User []models.Goods
}

func Select(ids  string) (string, string, string){
	//sqlText := fmt.Sprintf("select foreign_key , name, market_price,brief from goods where foreign_key = '%s'", ids)
	//sqlText1 := fmt.Sprintf("select foreign_key, name from manager where  foreign_key= '%s'", ids)
	sqlText := fmt.Sprintf("SELECT `purchase_order`.`manager_id`, COUNT(`purchase_order`.`order_number`) AS `count`, SUM(`purchase_order`.`actual_price`) AS `money` FROM `purchase_order` WHERE (`purchase_order`.`pay_time` BETWEEN '2018-12-11 16:00:00' AND '2019-12-12 15:59:59' AND `purchase_order`.`pay_state` = 1 AND `purchase_order`.`order_state` = 1) GROUP BY `purchase_order`.`manager_id` ORDER BY NULL")
	sqlText1 := fmt.Sprintf("SELECT `take_order`.`manager_id`, COUNT(`take_order`.`order_number`) AS `count` FROM `take_order` WHERE (NOT (`take_order`.`order_state` = 1) AND `take_order`.`create_date` BETWEEN '2018-12-11 16:00:00' AND '2019-12-12 15:59:59' AND `take_order`.`order_state` = 0 AND `take_order`.`take_state` IN (1, 3, 2, 0)) GROUP BY `take_order`.`manager_id` ORDER BY NULL")
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
	var maps2 []orm.Params
	result := []map[string]string{}
	data1, data2, data3 := Select(jsoninfo)
	_, err1 := o.Raw(data1).Values(&maps)
	_, err2 := o.Raw(data2).Values(&maps1)
	_, err3 := o.Raw(data3).Values(&maps2)
	date := time.Now().Format("2006-01-02")
	if err1 == nil && err2 == nil && err3 == nil{
		for _, i := range maps2{
			result = append(
				result,
				map[string]string{"id" : i["id"].(string), "name" : i["name"].(string), "mai" : "0", "ti" : "0", "price" : "0", "date" : date},
				)
		for _, i := range result{
			for _, k := range maps{
				if i["id"] == k["manager_id"]{
					i["mai"] = k["count"].(string)
					i["price"] = k["money"].(string)
				}
			}
			for _, k := range maps1{
				if i["id"] == k["manager_id"]{
					i["ti"] = k["count"].(string)
				}
			}
		}
	}
	data := &RESPONSEJOSN{
		"200",
		"获取成功",
		result[0:6],
	}
	c.Data["json"] = data
	}
	c.ServeJSON()
}

func (c *LoggerController) GoodsGet(){
	o := orm.NewOrm()
	var goods []models.Goods
	name := c.GetString("a")
	//_, err := o.Raw("select name,foreign_key,create_time from goods where name like '%"+name+"%'").QueryRows(&goods)
	num, err := o.Raw("select name,foreign_key,create_time,(select short_name from manager where foreign_key = s.foreign_key) as short_name from goods as s where s.name like '%"+name+"%'").QueryRows(&goods)
	if err != nil {
		logs.Error(err)
		c.Ctx.WriteString("1111111111jsoninfo is empty")
		return
	}
	result := &JSONS11{
		"200",
		"获取成功",
		num,
		goods,
	}
	c.Data["json"] = result			//将结构体数组根据tag解析为json
	c.ServeJSON()					//对json进行序列化输出
}




