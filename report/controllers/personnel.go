package controllers

import (
	"bytes"
	"encoding/json"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	"io"
	"net/http"
	"report/models"
	"time"
)

type Pbasecontroller struct {
	beego.Controller
}
type Server struct {
	Id   int
	Name string
	Parentid int
}
type Response struct {
	Msg string
	Code int

}

type Serverslice struct {
	Department []Server
	Msg Response
}

func (this* Pbasecontroller) Getpersonnel(){
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
		data := &RESPONSE{
			Code: 500,
			Msg:  "Token conversion failed %v " ,
		}
		this.Data["json"] = data
		this.ServeJSON()
	}else{
		var token string
		token = tokendata["access_token"].(string)
		url := "https://oapi.dingtalk.com/department/list?access_token="+token+""
		client := http.Client{Timeout:15*time.Second}
		resp, err := client.Get(url)
		defer resp.Body.Close()
		if err != nil{
			panic(err)
		}
		var buffer [2048]byte
		result := bytes.NewBuffer(nil)
		for {
			n, err := resp.Body.Read(buffer[0:])
			result.Write(buffer[0:n])
			if err != nil && err == io.EOF{
				break
			}else if err != nil{
				panic(err)
			}
		}
		info := result.String()
		var redata Serverslice
		json.Unmarshal([]byte(info), &redata)
		if redata.Msg.Code != 0{
			data := &RESPONSE{
				Code: 500,
				Msg:  "dingding faild",
			}
			this.Data["json"] = data
			this.ServeJSON()
		}
		for _, v := range redata.Department{
			o := orm.NewOrm()
			var department []models.Department
			num, err := o.Raw("select id from department where id = ?", v.Id ).QueryRows(&department)
			if err != nil{
				data := &RESPONSE{
					Code: 500,
					Msg: err,
				}
				this.Data["json"] = data
				this.ServeJSON()
			}
			if num < 1{
				o := orm.NewOrm()
				_, err := o.Raw("insert into department(id,name,parentid) values(?,?,?)",v.Id, v.Name, v.Parentid).Exec()
				if err != nil {
					data := &RESPONSE{
						Code: 500,
						Msg: err,
					}
					this.Data["json"] = data
					this.ServeJSON()
				}
			}
		}
		data := &RESPONSE{
			Code: 200,
			Msg:  "success",
		}
		this.Data["json"] = data
		this.ServeJSON()
	}
}