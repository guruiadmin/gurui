package controllers

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"net/http"
	"report/models"
	"time"
)

type Bbasecontroller struct {
	beego.Controller
}

func (this *Bbasecontroller) Post() {
	Brand := this.GetString("brand", "none")
	if Brand == "none" {
		resultjson := &RESPONSE{
			"400",
			"miss parameter",
		}
		this.Data["json"] = resultjson
		this.ServeJSON()
	}
	o := orm.NewOrm()
	var clinic []models.Clinic
	num, err := o.Raw("select name from clinic where name = ?", Brand ).QueryRows(&clinic)
	if err != nil {
		logs.Error(err)
		http.Error(this.Ctx.ResponseWriter, "查询用户信息出错", http.StatusBadGateway)
		return
	}
	if num < 1{
		_, err1 := o.Raw("insert into clinic(clinic_id,create_time) values(?,?)",Brand, time.Now()).Exec()
		if err1 != nil {
			fmt.Println("Addbrand err=", err)
			return
		}
		http.Error(this.Ctx.ResponseWriter, "success", http.StatusOK)
	}else{
		resultjson := &RESPONSE{
			"200",
			"success",
		}
		this.Data["json"] = resultjson
		this.ServeJSON()
	}
}
