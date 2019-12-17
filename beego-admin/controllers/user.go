package controllers

import (
	"beego-admin/models"
	"encoding/json"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"strconv"
)

type UserController struct {
	BaseController
}

/*
	返回平台用户管理列表展示页面
*/
func (This *UserController) RoleList() {
	This.TplName = "pages/user/roleList.html"
}

/*
	返回平台角色管理添加页面
*/
func (This *UserController) RoleListAdd() {

	o := orm.NewOrm()
	var err error
	var ones []*models.One

	_, err = o.Raw(
		"select id, title from menu_one").QueryRows(&ones)
	if err != nil {
		logs.Error("查询菜单出错，错误内容为:", err)
	}
	This.Data["ones"] = ones

	This.TplName = "pages/user/roleListAdd.html"
}

/*
	平台角色批量删除
*/
func (This *UserController) RoleListDelete() {

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
		_, err = o.Raw("delete from menu_role where id = ?", v).Exec()
		if err != nil {
			o.Rollback()
			logs.Error("删除角色错误，错误内容为:", err)
			This.JsonEncode(1, "失败！", "", 0)
		}
		_, err = o.Raw("delete from menu_role_menu_ones where menu_role_id = ?", v).Exec()
		if err != nil {
			o.Rollback()
			logs.Error("删除用户菜单出错，错误内容为:", err)
			This.JsonEncode(1, "失败！", "", 0)
		}
	}
	o.Commit()
	This.JsonEncode(0, "成功！", "", 0)
}

/*
	平台角色管理添加
*/
func (This *UserController) RoleListAddTo() {

	var err error
	var role *models.Role

	err = json.Unmarshal(This.Ctx.Input.RequestBody, &role)
	if err != nil {
		logs.Error(err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	o := orm.NewOrm()
	_, err = o.Insert(role)
	if err != nil {
		o.Rollback()
		logs.Error("添加，错误内容为:", err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	for _, x := range role.Ones {
		o.Raw("insert into menu_role_menu_ones(menu_role_id, menu_one_id) value(?,?)", role.Id, x.Id).Exec()
	}

	This.JsonEncode(0, "成功！", "", 1)
}

/*
	返回平台角色管理数据
*/
func (This *UserController) RoleData() {

	name := This.GetString("name")
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
	var roles []*models.Role
	var ones []*models.One
	var sql string
	var sqlc string
	var count int64

	sql = "select id, name, status, description from menu_role where 1=1"
	sqlc = "select count(*) from menu_role where 1=1"

	if name != "" {
		sql += " and name like '%" + name + "%'"
		sqlc += " and name like '%" + name + "%'"
	}
	sql += " order by id desc limit " + strconv.Itoa((page-1)*limit) + "," + strconv.Itoa(limit)
	_, err = o.Raw(sql).QueryRows(&roles)
	if err != nil {
		logs.Error("查询平台角色数据sql出错，错误内容为：", err)
	}

	for i, v := range roles {
		_, err = o.Raw(
			"select title from menu_one where id in(select menu_one_id from menu_role_menu_ones where menu_role_id = ?)", v.Id).QueryRows(&ones)
		if err != nil {
			logs.Error("查询角色数据sql出错，错误内容为：", err)
		}
		roles[i].Ones = ones
		ones = nil
	}

	err = o.Raw(sqlc).QueryRow(&count)
	if err != nil {
		logs.Error("统计平台角色数据sql出错，错误内容为：", err)
	}

	This.JsonEncode(0, "成功！", roles, count)
}

/*
	返回平台用户管理列表展示页面
*/
func (This *UserController) UserList() {
	This.TplName = "pages/user/userList.html"
}

/*
	返回平台用户管理添加页面
*/
func (This *UserController) UserListAdd() {

	o := orm.NewOrm()
	var err error
	var roles []*models.Role

	_, err = o.Raw(
		"select id, name from menu_role").QueryRows(&roles)
	if err != nil {
		logs.Error("查询角色出错，错误内容为:", err)
	}
	This.Data["roles"] = roles
	This.TplName = "pages/user/userListAdd.html"
}

/*
	平台用户批量删除
*/
func (This *UserController) UserListDelete() {

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
		_, err = o.Raw("delete from menu_user where id = ?", v).Exec()
		if err != nil {
			o.Rollback()
			logs.Error("添加，错误内容为:", err)
			This.JsonEncode(1, "失败！", "", 0)
		}
		_, err = o.Raw("delete from menu_user_menu_roles where menu_user_id = ?", v).Exec()
		if err != nil {
			o.Rollback()
			logs.Error("删除用户权限出错，错误内容为:", err)
			This.JsonEncode(1, "失败！", "", 0)
		}
	}
	o.Commit()
	This.JsonEncode(0, "成功！", "", 0)
}

/*
	平台用户管理添加
*/
func (This *UserController) UserListAddTo() {

	var err error
	var user *models.User

	err = json.Unmarshal(This.Ctx.Input.RequestBody, &user)
	if err != nil {
		logs.Error(err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	o := orm.NewOrm()
	_, err = o.Insert(user)
	if err != nil {
		o.Rollback()
		logs.Error("添加，错误内容为:", err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	for _, x := range user.Roles {
		o.Raw("insert into menu_user_menu_roles(menu_user_id, menu_role_id) value(?,?)", user.Id, x.Id).Exec()
	}

	This.JsonEncode(0, "成功！", "", 1)
}

/*
	返回平台用户管理数据
*/
func (This *UserController) UserData() {

	username := This.GetString("username")
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
	var users []*models.User
	var roles []*models.Role
	var sql string
	var sqlc string
	var count int64

	sql = "select id, username, password, status from menu_user where 1=1"
	sqlc = "select count(*) from menu_user where 1=1"

	if username != "" {
		sql += " and username like '%" + username + "%'"
		sqlc += " and username like '%" + username + "%'"
	}
	sql += " order by id desc limit " + strconv.Itoa((page-1)*limit) + "," + strconv.Itoa(limit)
	_, err = o.Raw(sql).QueryRows(&users)
	if err != nil {
		logs.Error("查询平台用户数据sql出错，错误内容为：", err)
	}

	for i, v := range users {
		_, err = o.Raw(
			"select name from menu_role where id in(select menu_role_id from menu_user_menu_roles where menu_user_id = ?)", v.Id).QueryRows(&roles)
		if err != nil {
			logs.Error("查询角色数据sql出错，错误内容为：", err)
		}
		users[i].Roles = roles
		roles = nil
	}

	err = o.Raw(sqlc).QueryRow(&count)
	if err != nil {
		logs.Error("统计平台用户数据sql出错，错误内容为：", err)
	}

	This.JsonEncode(0, "成功！", users, count)
}
