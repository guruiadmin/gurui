package models

import "time"

/*
	用户表
*/
type Goods struct {
	Id        int64     `orm:"auto; pk" json:"id"`
	Name  string    `orm:"size(25); description(商品名字)" json:"name"`
	Brief  string    `orm:"size(25); description(商品介绍)" json:"brief"`
	Market_price  string    `orm:"size(255); description(商品名字)" json:"market_price"`
	Foreign_key   string    `orm:"size(255); description(商家关联)" json:"foreign_key"`
	Short_name   string    `orm:"size(255); description(商家关联)" json:"sort_name"`
	Greate_time time.Time `orm:"auto_now; type(datetime); description(用户登录时间)" json:"greate_time"`
}

type Staff struct {
	DeviceId        int64     `orm:"auto; pk" json:"deviceId"`
	Name  string    `orm:"size(25); description(管理员名字)" json:"name"`
	Clinic_id  string    `orm:"size(25); description(诊所id)" json:"clinic_id"`
	Userid  string    `orm:"size(255); description(管理员id)" json:"userid"`
	Is_sys   string    `orm:"size(255); description(是否是管理员)" json:"foreign_key"`
	Sys_level   string    `orm:"size(255); description(级别)" json:"sys_level"`
	Create_time time.Time `orm:"auto_now; type(datetime); description(用户登录时间)" json:"create_time"`
}
