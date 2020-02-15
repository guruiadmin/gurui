package controllers

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"io"
	"net/http"
	"report/models"
	"time"
)

type Basecontroller struct {
	beego.Controller
}



type JSONS1 struct {
	//必须的大写开头
	Code string      `json:"code"`
	Msg  string		 `json:"msg"`
	Num int64        `json:"num"`
	User []models.Goods   `json:"data"`
}


func (c *Basecontroller) Dazu(){
	name := c.GetString("a")
	if name == "" {
		c.Ctx.WriteString("jsoninfo is empty")
		return
	}
	switch name {
	case "1":
		o := orm.NewOrm()
		var goods []models.Goods
		//_, err := o.Raw("select name,foreign_key,create_time from goods where name like '%"+name+"%'").QueryRows(&goods)
		num, err := o.Raw("select name,foreign_key,create_time,(select short_name from manager where foreign_key = s.foreign_key) as short_name from goods as s where s.name like '%"+name+"%'").QueryRows(&goods)
		if err != nil {
			logs.Error(err)
			c.Ctx.WriteString("1111111111jsoninfo is empty")
			return
		}
		result := &JSONS1{
			"200",
			"获取成功",
			num,
			goods,
		}
		c.Data["json"] = result			//将结构体数组根据tag解析为json
		c.ServeJSON()					//对json进行序列化输出
	case "2":
		o := orm.NewOrm()
		var goods []models.Goods
		//_, err := o.Raw("select name,foreign_key,create_time from goods where name like '%"+name+"%'").QueryRows(&goods)
		num, err := o.Raw("select name,(select short_name from manager where foreign_key = s.foreign_key) as short_name from goods as s where s.name like '%"+name+"%'").QueryRows(&goods)
		if err != nil {
			logs.Error(err)
			c.Ctx.WriteString("1111111111jsoninfo is empty")
			return
		}
		result := &JSONS1{
			"200",
			"获取成功",
			num,
			goods,
		}
		c.Data["json"] = result			//将结构体数组根据tag解析为json
		c.ServeJSON()
	default:
		c.Ctx.WriteString("jsoninfo is emphhhhhhty")
	}
}


type Code struct {
	Msg  string
}

type JSONS2 struct {
	//必须的大写开头
	Code string      `json:"code"`
	Msg  string		 `json:"msg"`
	Data   interface{}  `json:"data"`
}

type RESPONSE struct {
	Code interface{}      `json:"code"`
	Msg  interface{}		 `json:"msg"`
}

func (this *Basecontroller) Post() {
	url := "https://oapi.dingtalk.com/gettoken?appkey=dingkarppuxvlty75z95&appsecret=1pwB8WmjeVeRZfpXEFSdu8zpevysoTOCI_mRxTgl1TCbFy8Hv9rYaY4aNu9utTkM"
	client := http.Client{Timeout: 15 * time.Second}
	resp, error := client.Get(url)
	defer resp.Body.Close()
	if error != nil {
		panic(error)
	}
	var buffer [512]byte
	result := bytes.NewBuffer(nil)
	for {
		n, err := resp.Body.Read(buffer[0:])
		result.Write(buffer[0:n])
		if err != nil && err == io.EOF {
			break
		} else if err != nil {
			panic(err)
		}
	}
	access_token := result.String()
	tokendata := make(map[string]interface{})
	err := json.Unmarshal([]byte(access_token), &tokendata)
	if err != nil {
		fmt.Println("token转换 err=", err)
		return
	}
	Msg := this.GetString("Msg", "none")
	if Msg == "none" {
		http.Error(this.Ctx.ResponseWriter, "missing parameters", http.StatusBadRequest)
		return
	}
		var token string
		token = tokendata["access_token"].(string)
		user_url := "https://oapi.dingtalk.com/user/getuserinfo?access_token=" + token + "&code=" + Msg + ""
		user_client := http.Client{Timeout: 15 * time.Second}
		toenresp, tokenerr := user_client.Get(user_url)
		defer toenresp.Body.Close()
		if tokenerr != nil {
			panic(tokenerr)
		}
		var user_buffer [2048]byte
		user_result := bytes.NewBuffer(nil)
		for {
			n, err := toenresp.Body.Read(user_buffer[0:])
			user_result.Write(user_buffer[0:n])
			if err != nil && err == io.EOF {
				break
			} else if err != nil {
				panic(err)
			}
		}
		userid := user_result.String()
		userdata := make(map[string]interface{})
		usererr := json.Unmarshal([]byte(userid), &userdata)
		if usererr != nil{
			http.Error(this.Ctx.ResponseWriter, "token转换 err=", http.StatusBadGateway)
			return
		}
		//if userdata["errcode"] != 200{
		//	resultjson := &RESPONSE{
		//		userdata["errcode"],
		//		userdata["errmsg"],
		//	}
		//	this.Data["json"] = resultjson			//将结构体数组根据tag解析为json
		//	this.ServeJSON()
		//}
		if userdata["is_sys"] == "true"{
			userdata["is_sys"] = "1"
		}else {
			userdata["is_sys"] = "0"
		}
		o := orm.NewOrm()
		var staff []models.Staff
		num, err := o.Raw("select id from staff where userid = ?", userdata["userid"] ).QueryRows(&staff)
		if err != nil {
			logs.Error(err)
			http.Error(this.Ctx.ResponseWriter, "查询用户信息出错", http.StatusBadGateway)
			return
		}
		if userdata["name"] != nil && num < 1{
			o := orm.NewOrm()
			_, err := o.Raw("insert into staff(is_sys,name,deviceId,userid,sys_level,create_time) values(?,?,?,?,?,?)", userdata["is_sys"], userdata["name"], userdata["deviceId"],userdata["userid"],userdata["sys_level"], time.Now()).Exec()
			if err != nil {
				http.Error(this.Ctx.ResponseWriter, "存入用户信息 err=", http.StatusBadGateway)
				return
			}
		}

	var mapppp = make(map[string]interface{})
	mapppp["is_sys"]=userdata["is_sys"]
	mapppp["name"]=userdata["name"]
	mapppp["deviceId"]=userdata["deviceId"]
	mapppp["userid"]=userdata["userid"]
	mapppp["sys_level"]=userdata["sys_level"]

	resultjson := &JSONS2{
		"200",
		"success",
		mapppp,
	}
	this.Data["json"] = resultjson			//将结构体数组根据tag解析为json
	this.ServeJSON()
}
