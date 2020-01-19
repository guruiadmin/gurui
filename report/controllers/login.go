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
	Code string
	Msg  string
	User []string `json:"user_info"`//key重命名,最外面是反引号
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
	Msg := this.GetString("Msg")
	if Msg == "" {
		this.Ctx.WriteString("jsoninfo is empty")
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
		if usererr != nil {
			fmt.Println("token转换 err=", usererr)
			return
		}
		if userdata["is_sys"] == "true"{
			userdata["is_sys"] = "1"
		}else {
			userdata["is_sys"] = "0"
		}
		//num, err := e.Raw("select id from staff where userid = ?", userdata["userid"] ).Exec()
		//if err != nil {
		//	fmt.Println("AddUser err=", err)
		//}
		o := orm.NewOrm()
		var staff []models.Staff
		num, err := o.Raw("select id from staff where userid = ?", userdata["userid"] ).QueryRows(&staff)
		if err != nil {
			logs.Error(err)
			this.Ctx.WriteString("1111111111jsoninfo is empty")
			return
		}
		fmt.Println(userdata["name"], num)
		if userdata["name"] != nil && num < 1{
			o := orm.NewOrm()
			_, err = o.Raw("insert into staff(is_sys,name,deviceId,userid,sys_level,create_time) values(?,?,?,?,?,?)", userdata["is_sys"], userdata["name"], userdata["deviceId"],userdata["userid"],userdata["sys_level"], time.Now()).Exec()
			if err != nil {
				fmt.Println("AddUser err=", err)
			}
		}
		data := &JSONS2{"100", "获取成功",
			[]string{"maple","18"}}
		this.Data["json"] = data
		this.ServeJSON()
}
