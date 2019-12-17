package models

import (
	"github.com/astaxie/beego/orm"
	"time"
)

/*
	用户表
*/
type User struct {
	Id        int64     `orm:"auto; pk"`
	Username  string    `orm:"size(25); description(用户登录名)"`
	Password  string    `orm:"size(25); description(用户登录密码)"`
	Status    int       `orm:"description(用户状态，是否启用，默认为0启用，为1不启用)"`
	Loginip   string    `orm:"size(25); description(用户登录ip)"`
	Logintime time.Time `orm:"auto_now; type(datetime); description(用户登录时间)"`
	Roles     []*Role   `orm:"rel(m2m)"`
}

/*
	角色表
*/
type Role struct {
	Id          int64   `orm:"auto; pk"`
	Name        string  `orm:"size(25); description(角色名)"`
	Status      int     `orm:"description(角色状态，是否启用，默认为0启用，为1不启用)"`
	Description string  `orm:"type(text); description(角色说明)"`
	Users       []*User `orm:"reverse(many)"`
	Ones        []*One  `orm:"rel(m2m)"`
}

func init() {
	orm.RegisterModelWithPrefix("menu_", new(User), new(Role))
}
