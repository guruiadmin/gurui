package conf

import (
	"github.com/astaxie/beego/orm"
	_ "github.com/go-sql-driver/mysql"
)

func init(){
	orm.RegisterDriver("mysql", orm.DRMySQL)
	orm.RegisterDataBase("default", "mysql", "root:Gurui190916@tcp(47.104.159.115:3306)/dev?charset=utf8")
}
