package models

import (
	"github.com/astaxie/beego/orm"
)

/*
	一级菜单表
*/
type One struct {
	Id          int64   `orm:"auto; pk"`
	Title       string  `orm:"size(25); description(一级菜单标题)"`
	Description string  `orm:"type(text); description(菜单对应说明)"`
	Twos        []*Two  `orm:"reverse(many)"`
	Roles       []*Role `orm:"reverse(many)"`
}

/*
	二级菜单表
*/
type Two struct {
	Id          int64  `orm:"auto; pk"`
	Title       string `orm:"size(25); description(二级菜单标题)"`
	Url         string `orm:"size(26); description(二级菜单对应接口)"`
	Description string `orm:"type(text); description(二级菜单对应说明)"`
	One         *One   `orm:"rel(fk)"`
}

func init() {
	orm.RegisterModelWithPrefix("menu_", new(One), new(Two))
}
