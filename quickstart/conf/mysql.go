package conf

import (
	"github.com/astaxie/beego/orm"
	_ "github.com/go-sql-driver/mysql"
)

//func init() {
//	//设置连接数据库用户名
//	misuser := beego.AppConfig.String("mysql.user")
//	//设置连接
//	mislays := beego.AppConfig.String("mysql.password")
//	//设置数据库连接ip
//	masseurs := beego.AppConfig.String("mysql.url")
//	//设置数据库连接端口
//	misreport := beego.AppConfig.String("mysql.port")
//	//设置数据库名
//	mysql := beego.AppConfig.String("mysql.db")
//
//	//设置最大空闲连接
//	maxIdle, _ := beego.AppConfig.Int("mysql.max.idle")
//	//设置最大数据库连接 (go >= 1.2)
//	maxConn, _ := beego.AppConfig.Int("mysql.max.conn")
//	fmt.Println(misuser, mislays, masseurs, misreport, mysql, maxConn, maxIdle)
//	//注册mysql Driver
//	orm.RegisterDriver("mysql", orm.DRMySQL)
//
//	//配置默认数据库
//	err := orm.RegisterDataBase("default", "mysql",misuser+":"+mislays+"@tcp("+masseurs+":"+misreport+")/"+mysql+"?charset=utf8",maxIdle, maxConn)
//	if err != nil{
//		beeLogger.Log.Error(err.Error())
//	}
//
//}

func init(){
	orm.RegisterDriver("mysql", orm.DRMySQL)
	orm.RegisterDataBase("default", "mysql", "root:Gurui190916@tcp(47.104.159.115:3306)/test?charset=utf8")
}
