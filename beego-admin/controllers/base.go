package controllers

import (
	"beego-admin/models"
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
)

type BaseController struct {
	beego.Controller
}

/*
	用户左导航栏内容
*/
func (This *BaseController) SessionLeftNav(id int64) {
	o := orm.NewOrm()
	var err error
	var ones []*models.One
	var twos []*models.Two

	_, err = o.Raw(
		"SELECT o.id, o.title FROM menu_one as o WHERE id IN(SELECT menu_one_id FROM menu_role_menu_ones WHERE menu_role_id IN(SELECT menu_role_id FROM menu_user_menu_roles WHERE menu_user_id = ?))", id).QueryRows(&ones)
	if err != nil {
		logs.Error("查询一级菜单出错，错误内容为:", err)
	}

	for key, value := range ones {
		_, err = o.Raw(
			"select title, url from menu_two where one_id = ?", value.Id).QueryRows(&twos)
		if err != nil {
			logs.Error("查询二级菜单出错，错误内容为:", err)
		}
		ones[key].Twos = twos
		twos = nil
	}
	This.SetSession("LeftNavResult", ones)
}

/*
	判断用户是否登录
*/
func (This *BaseController) CheckLogin() (interface{}, bool) {
	userData := This.GetSession("LoginUser")
	fmt.Println(1111, userData)
	if userData == nil {
		return nil, false
	}
	return userData, true
}
