package models

import (
	"github.com/astaxie/beego/orm"
	_ "github.com/go-sql-driver/mysql"
)

func init(){
	// 设置数据库基本信息
	orm.RegisterDataBase("default", "mysql", "root:mingjingtai123@tcp(47.94.102.108:3306)/dev?charset=utf8")

}



