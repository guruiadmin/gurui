package controllers

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	"quickstart/common"
)

type LoggerController struct {
	beego.Controller
}

type Product struct {
	ID           int64  `json:"id" sql:"id"`
	ProductName  string `json:"ProductName" sql:"productName"`
	ProductNum   int64  `json:"ProductNum" sql:"productNum"`
}

func (c *LoggerController) Get() {
	//这块是模拟mysql获取所有的数据反射到结构体
	o := orm.NewOrm()
	var maps []orm.Params
	num, err := o.Raw("select id, name, market_price from goods where name is not null").Values(&maps)
	fmt.Println(maps)
	if err == nil && num > 0 {
	Alldata := []map[string]string{
		{"id": "1", "productName": "5lmh.com", "productNum": "40"},
		{"id": "2", "productName": "5lmh.com", "productNum": "40"},
	}
	var productArray []*Product
	for _, v := range Alldata {
		Allproduct := &Product{}
		common.DataToStructByTagSql(v, Allproduct)
		productArray = append(productArray, Allproduct)
	}
	for _, vv := range productArray {
		fmt.Println(vv)
	}
		c.ServeJSON()
	}
}


