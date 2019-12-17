package models

import (
	"time"
)

/*
	用户表
*/
type Goods struct {
	Id        int64     `orm:"auto; pk"`
	Name  string    `orm:"size(25); description(商品名字)"`
	Brief  string    `orm:"size(25); description(商品介绍)"`
	Market_price  string    `orm:"size(255); description(商品名字)"`
	Foreign_key   string    `orm:"size(255); description(商家关联)"`
	Greate_time time.Time `orm:"auto_now; type(datetime); description(用户登录时间)"`
}