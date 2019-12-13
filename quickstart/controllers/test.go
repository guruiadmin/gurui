package controllers

import (
	"database/sql"
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	"quickstart/common"
)

type LoggerController1 struct {
	beego.Controller
}

type Product1 struct {
	ID           int64  `json:"id" sql:"id"`
	ProductName  string `json:"ProductName" sql:"productName"`
	ProductNum   int64  `json:"ProductNum" sql:"productNum"`
}

func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}

func (c *LoggerController) Test() {
	//这块是模拟mysql获取所有的数据反射到结构体
	db, err := sql.Open( "mysql", "root:mingjingtai123@tcp(47.94.102.108:3306)/dev?charset=utf8")
	db.SetMaxOpenConns(2000)
	db.SetMaxIdleConns(1000)
	db.Ping()
	rows, err := db.Query("select  market_price from goods where name is not null limit 5")
	checkErr(err)
	fmt.Println(&rows)
	ows, err := db.Query("select name from goods where name is not null limit 5")
	fmt.Println(ows)
	o := orm.NewOrm()
	var maps []orm.Params
	num, err := o.Raw("select id, name, market_price from goods where name is not null limit 5").Values(&maps)
	fmt.Println(8)
	if err == nil && num > 0 {
		Alldata := []map[string]string{
			{"id": "1", "productName": "5lmh.com", "productNum": "40"},
			{"id": "2", "productName": "5lmh.com", "productNum": "40"},
		}
		var productArray []*Product1
		for _, v := range Alldata {
			Allproduct := &Product1{}
			common.DataToStructByTagSql(v, Allproduct)
			productArray = append(productArray, Allproduct)
		}
		for _, vv := range productArray {
			fmt.Println(vv)
		}
		c.ServeJSON()
	}
}