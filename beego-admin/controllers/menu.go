package controllers

import (
	"beego-admin/models"
	"encoding/json"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"strconv"
)

type MenuController struct {
	BaseController
}

/*
	返回平台二级菜单列表展示页面
*/
func (This *MenuController) TwoList() {

	o := orm.NewOrm()
	var err error
	var ones []*models.One

	_, err = o.Raw("select id, title from menu_one").QueryRows(&ones)
	if err != nil {
		logs.Error("查询一级菜单错误，错误为", err)
	}

	This.Data["ones"] = ones
	This.TplName = "pages/menu/twoList.html"
}

/*
	返回平台二级菜单添加页面
*/
func (This *MenuController) TwoListAdd() {

	o := orm.NewOrm()
	var err error
	var ones []*models.One

	_, err = o.Raw("select id, title from menu_one").QueryRows(&ones)
	if err != nil {
		logs.Error("查询一级菜单错误，错误为", err)
	}

	This.Data["ones"] = ones
	This.TplName = "pages/menu/twoListAdd.html"
}

/*
	平台二级菜单批量删除
*/
func (This *MenuController) TwoListDelete() {

	var err error
	var ids *Ids

	err = json.Unmarshal(This.Ctx.Input.RequestBody, &ids)
	if err != nil {
		logs.Error(err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	o := orm.NewOrm()
	o.Begin()
	for _, v := range ids.Ids {
		o.Raw("delete from menu_two where id = ?", v).Exec()
	}
	o.Commit()
	This.JsonEncode(0, "成功！", "", 0)
}

/*
	平台二级菜单添加
*/
func (This *MenuController) TwoListAddTo() {

	var err error
	var two *models.Two

	err = json.Unmarshal(This.Ctx.Input.RequestBody, &two)
	if err != nil {
		logs.Error(err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	o := orm.NewOrm()
	_, err = o.Insert(two)
	if err != nil {
		o.Rollback()
		logs.Error("添加，错误内容为:", err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	This.JsonEncode(0, "成功！", "", 1)
}

/*
	返回平台二级菜单数据
*/
func (This *MenuController) TwoData() {

	onec := This.GetString("one")
	page, err1 := This.GetInt("page")
	if err1 != nil {
		This.JsonEncode(1, "失败！", nil, 0)
	}
	limit, err2 := This.GetInt("limit")
	if err2 != nil {
		This.JsonEncode(1, "失败！", nil, 0)
	}

	o := orm.NewOrm()
	var err error
	var twos []*models.Two
	var one *models.One
	var sql string
	var sqlc string
	var count int64

	sql = "select * from menu_two where 1=1"
	sqlc = "select count(*) from menu_two where 1=1"

	if onec != "" {
		sql += " and one_id = " + onec
		sqlc += " and one_id = " + onec
	}
	sql += " order by id desc limit " + strconv.Itoa((page-1)*limit) + "," + strconv.Itoa(limit)
	_, err = o.Raw(sql).QueryRows(&twos)
	if err != nil {
		logs.Error("查询平台二级菜单数据sql出错，错误内容为：", err)
	}

	for i, v := range twos {
		err = o.Raw("select title from menu_one where id = ?", v.One.Id).QueryRow(&one)
		if err != nil {
			logs.Error("查询平台一级菜单数据sql出错，错误内容为：", err)
		}
		twos[i].One = one
		one = nil
	}

	err = o.Raw(sqlc).QueryRow(&count)
	if err != nil {
		logs.Error("统计平台二级菜单数据sql出错，错误内容为：", err)
	}

	This.JsonEncode(0, "成功！", twos, count)
}

/*
	返回平台一级菜单列表展示页面
*/
func (This *MenuController) OneList() {
	This.TplName = "pages/menu/oneList.html"
}

/*
	返回平台一级菜单添加页面
*/
func (This *MenuController) OneListAdd() {

	o := orm.NewOrm()
	var err error
	var roles []*models.Role

	_, err = o.Raw(
		"select id, name from menu_role").QueryRows(&roles)
	if err != nil {
		logs.Error("查询角色出错，错误内容为:", err)
	}
	This.Data["roles"] = roles
	This.TplName = "pages/menu/oneListAdd.html"
}

type MenuOne struct {
	Title string
}

type Ids struct {
	Ids []int
}

/*
	平台一级菜单批量删除
*/
func (This *MenuController) OneListDelete() {

	var err error
	var ids *Ids

	err = json.Unmarshal(This.Ctx.Input.RequestBody, &ids)
	if err != nil {
		logs.Error(err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	o := orm.NewOrm()
	o.Begin()
	for _, v := range ids.Ids {
		o.Raw("delete from menu_two where id = ?", v).Exec()
		o.Raw("delete from menu_one where id = ?", v).Exec()
		o.Raw("delete from menu_role_menu_ones where menu_id = ?", v).Exec()
	}
	o.Commit()
	This.JsonEncode(0, "成功！", "", 0)
}

/*
	平台一级菜单添加
*/
func (This *MenuController) OneListAddTo() {

	var err error
	var one *models.One

	err = json.Unmarshal(This.Ctx.Input.RequestBody, &one)
	if err != nil {
		logs.Error(err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	o := orm.NewOrm()
	o.Begin()
	_, err = o.Insert(one)
	if err != nil {
		o.Rollback()
		logs.Error("添加平台一级菜单，错误内容为:", err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	err = o.Raw("select id from menu_one where title = ?", one.Title).QueryRow(&one)
	if err != nil {
		o.Rollback()
		logs.Error("查询平台一级菜单出错，错误内容为:", err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	for _, x := range one.Roles {
		_, err = o.Raw("insert into menu_role_menu_ones(menu_role_id, menu_one_id) value(?,?)", x.Id, one.Id).Exec()
		if err != nil {
			o.Rollback()
			logs.Error("添加平台一级菜单出错，错误内容为:", err)
			This.JsonEncode(1, "失败！", "", 0)
		}
	}

	o.Commit()
	This.JsonEncode(0, "成功！", "", 1)
}

/*
	返回平台一级菜单数据
*/
func (This *MenuController) OneData() {

	title := This.GetString("title")
	page, err1 := This.GetInt("page")
	if err1 != nil {
		This.JsonEncode(1, "失败！", nil, 0)
	}
	limit, err2 := This.GetInt("limit")
	if err2 != nil {
		This.JsonEncode(1, "失败！", nil, 0)
	}

	o := orm.NewOrm()
	var err error
	var ones []*models.One
	var roles []*models.Role
	var sql string
	var sqlc string
	var count int64

	sql = "select * from menu_one where 1=1"
	sqlc = "select count(*) from menu_one where 1=1"

	if title != "" {
		sql += " and title like '%" + title + "%'"
		sqlc += " and title like '%" + title + "%'"
	}
	sql += " order by id desc limit " + strconv.Itoa((page-1)*limit) + "," + strconv.Itoa(limit)
	_, err = o.Raw(sql).QueryRows(&ones)
	if err != nil {
		logs.Informational("查询平台一级菜单数据sql出错，错误内容为：", err)
	}

	err = o.Raw(sqlc).QueryRow(&count)
	if err != nil {
		logs.Informational("统计平台一级菜单数据sql出错，错误内容为：", err)
	}

	for key, value := range ones {
		_, err = o.Raw(
			"SELECT name FROM menu_role WHERE `status` = 0 AND id IN(SELECT menu_role_id FROM menu_role_menu_ones WHERE menu_one_id = ?)", value.Id).QueryRows(&roles)
		if err != nil {
			logs.Error("查询角色出错，错误内容为:", err)
		}
		ones[key].Roles = roles
	}

	This.JsonEncode(0, "成功！", ones, count)
}

func (This *BaseController) JsonEncode(code int, msg string, data interface{}, count int64) {
	This.Data["json"] = map[string]interface{}{"code": code, "msg": msg, "data": data, "count": count}
	This.ServeJSON()
	This.StopRun()
}

func (This *BaseController) JsonEncodePhoto(code int, msg string, data interface{}) {
	This.Data["json"] = map[string]interface{}{"code": code, "msg": msg, "data": data}
	This.ServeJSON()
	This.StopRun()
}
