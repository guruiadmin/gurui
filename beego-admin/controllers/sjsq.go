package controllers

import (
	"beego-admin/models"
	"encoding/json"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"github.com/satori/go.uuid"
	"strconv"
)

type SjsqController struct {
	BaseController
}

/*
	返回审核公司内容列表展示页面
*/
func (This *SjsqController) SjsqReviewList() {
	This.TplName = "pages/sjsq/sjsqReviewOneDataList.html"
}

/*
	返回公司内容修改页面
*/
func (This *SjsqController) SjsqReviewListUp() {

	id := This.Ctx.Input.Param(":id")

	o := orm.NewOrm()
	var oneData *models.OneData
	var err error
	err = o.Raw("select id, title, status, review, description, data, username, updated from sjsq_one_data where id = ?", id).QueryRow(&oneData)
	if err != nil {
		logs.Error("查询公司内容单条数据出错。")
	}
	This.Data["oneData"] = oneData
	This.TplName = "pages/sjsq/sjsqReviewOneDataListUp.html"
}

/*
	返回公司内容列表展示页面
*/
func (This *SjsqController) SjsqList() {
	This.TplName = "pages/sjsq/sjsqOneDataList.html"
}

/*
	返回公司内容添加页面
*/
func (This *SjsqController) SjsqListAdd() {
	This.TplName = "pages/sjsq/sjsqOneDataListAdd.html"
}

/*
	返回公司内容修改页面
*/
func (This *SjsqController) SjsqListUp() {

	id := This.Ctx.Input.Param(":id")

	o := orm.NewOrm()
	var oneData *models.OneData
	var err error
	err = o.Raw("select id, title, status, review, description, data, username, updated from sjsq_one_data where id = ?", id).QueryRow(&oneData)
	if err != nil {
		logs.Error("查询公司内容单条数据出错。")
	}
	This.Data["oneData"] = oneData
	This.TplName = "pages/sjsq/sjsqOneDataListUp.html"
}

/*
	公司内容修改页面
*/
func (This *SjsqController) SjsqListUpTo() {
	var err error
	var oneData *models.OneData

	err = json.Unmarshal(This.Ctx.Input.RequestBody, &oneData)
	user, ok := This.GetSession("LoginUser").(models.User)
	if !ok {
		logs.Error("转换model.User类型出错了！！！")
	}
	oneData.Username = user.Username

	if err != nil {
		logs.Error(err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	o := orm.NewOrm()
	_, err = o.Raw(
		"update sjsq_one_data set title = ?, description = ?, data = ?, review = ? where id = ?", oneData.Title, oneData.Description, oneData.Data, oneData.Review, oneData.Id).Exec()
	if err != nil {
		logs.Error("修改公司内容出错，错误内容为:", err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	This.JsonEncode(0, "成功！", "", 1)
}

/*
	公司内容批量删除
*/
func (This *SjsqController) SjsqListDelete() {
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
		_, err = o.Raw("delete from sjsq_one_data where id = ?", v).Exec()
		if err != nil {
			o.Rollback()
			logs.Error("删除公司内容错误，错误内容为:", err)
			This.JsonEncode(1, "失败！", "", 0)
		}
	}
	o.Commit()
	This.JsonEncode(0, "成功！", "", 0)
}

/*
	公司内容添加
*/
func (This *SjsqController) SjsqListAddTo() {

	var err error
	var oneData *models.OneData

	err = json.Unmarshal(This.Ctx.Input.RequestBody, &oneData)
	user, ok := This.GetSession("LoginUser").(models.User)
	if !ok {
		logs.Error("转换model.User类型出错了！！！")
	}
	oneData.Username = user.Username

	if err != nil {
		logs.Error(err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	o := orm.NewOrm()
	_, err = o.Insert(oneData)
	if err != nil {
		logs.Error("添加公司内容出错，错误内容为:", err)
		This.JsonEncode(1, "失败！", "", 0)
	}

	This.JsonEncode(0, "成功！", "", 1)
}

/*
	返回公司内容管理数据
*/
func (This *SjsqController) SjsqData() {
	title := This.GetString("title")
	review := This.GetString("review")
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
	var oneDatas []*models.OneData
	var sql string
	var sqlc string
	var count int64

	sql = "select id, title, status, review, description, data, username, updated from sjsq_one_data where 1=1"
	sqlc = "select count(*) from sjsq_one_data where 1=1"

	if title != "" {
		sql += " and title like '%" + title + "%'"
		sqlc += " and title like '%" + title + "%'"
	}

	if review != "" {
		sql += " and review = " + review
		sqlc += " and review = " + review
	}

	sql += " order by id desc limit " + strconv.Itoa((page-1)*limit) + "," + strconv.Itoa(limit)
	_, err = o.Raw(sql).QueryRows(&oneDatas)
	if err != nil {
		logs.Error("查询公司内容数据sql出错，错误内容为：", err)
		This.JsonEncode(1, "失败！", nil, 0)
	}

	err = o.Raw(sqlc).QueryRow(&count)
	if err != nil {
		logs.Error("统计公司内容数据sql出错，错误内容为：", err)
		This.JsonEncode(1, "失败！", nil, 0)
	}

	This.JsonEncode(0, "成功！", oneDatas, count)
}

/*
	图片上传
*/
func (This *SjsqController) AddPhoto() {
	file, head, err := This.GetFile("file")
	if err != nil {
		This.Ctx.WriteString("获取文件失败")
		return
	}
	defer file.Close()

	u := uuid.Must(uuid.NewV4())

	filename := head.Filename
	url := "static/img/" + u.String() + filename
	err = This.SaveToFile("file", url)
	if err != nil {
		logs.Error("上传文件出错，错误内容为：", err)
		This.JsonEncodePhoto(1, "上传失败！", nil)
	}
	This.JsonEncodePhoto(0, "成功！", map[string]string{"src": "/" + url})
}
