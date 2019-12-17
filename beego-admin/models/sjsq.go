package models

import (
	"github.com/astaxie/beego/orm"
	"time"
)

/*
	一级数据 （公司内容管理员提交数据）
*/
type OneData struct {
	Id     int64  `orm:"auto; pk"`
	Title  string `orm:"size(25); description(标题)"`
	Status int    `orm:"description(审核是否通过，默认为0开启,为1禁用)"`
	Review int    `orm:"description(审核是否通过，默认为0待审核,为1未通过，为2通过)"`
	//	Url         string    `orm:"description(链接)"`
	Description string    `orm:"type(text); description(介绍)"`
	Data        string    `orm:"type(text); description(内容)"`
	Username    string    `orm:"size(25); description(最后一次修改人)"`
	Updated     time.Time `orm:"auto_now; type(datetime); description(最后一次修改时间)"`
}

func init() {
	orm.RegisterModelWithPrefix("sjsq_", new(OneData))
}
