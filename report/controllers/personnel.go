package controllers

import (
	"bytes"
	"encoding/json"
	"fmt"
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
type EmployeeDetails struct {
	Errcode int `json:"errcode"`
	HasMore bool `json:"hasMore"`
	Errmsg string `json:"errmsg"`
	Userlist []struct {
		Unionid string `json:"unionid"`
		OpenID string `json:"openId"`
		Remark string `json:"remark"`
		Userid string `json:"userid"`
		IsBoss bool `json:"isBoss"`
		Tel string `json:"tel"`
		Department []int `json:"department"`
		WorkPlace string `json:"workPlace"`
		Email string `json:"email"`
		Order int64 `json:"order"`
		IsLeader bool `json:"isLeader"`
		Mobile string `json:"mobile"`
		Active bool `json:"active"`
		IsAdmin bool `json:"isAdmin"`
		Avatar string `json:"avatar"`
		IsHide bool `json:"isHide"`
		Name string `json:"name"`
		StateCode string `json:"stateCode"`
		Position string `json:"position"`
	}
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
	var buffer [2048]byte
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

func (this* Pbasecontroller)  Getdetails() {
	url := "https://oapi.dingtalk.com/gettoken?appkey=dingkarppuxvlty75z95&appsecret=1pwB8WmjeVeRZfpXEFSdu8zpevysoTOCI_mRxTgl1TCbFy8Hv9rYaY4aNu9utTkM"
	client := http.Client{Timeout: 15 * time.Second}
	resp, error := client.Get(url)
	defer resp.Body.Close()
	if error != nil {
		panic(error)
	}
	var buffer [2048]byte
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
			Msg:  "Token conversion failed %v ",
		}
		this.Data["json"] = data
		this.ServeJSON()
	}
	o := orm.NewOrm()
	var details []orm.Params
	sql := fmt.Sprintf("select id from department")
	_, err1 := o.Raw(sql).Values(&details)
	if err1 != nil {
		data := &RESPONSE{
			Code: 500,
			Msg:  "查詢department id 出錯",
		}
		this.Data["json"] = data
		this.ServeJSON()
	} else {
		for _, i := range details {
			var token string
			token = tokendata["access_token"].(string)
			durl := "https://oapi.dingtalk.com/user/listbypage?access_token=" + token + "&department_id=" + i["id"].(string) + "&offset=0&size=100"
			dclient := http.Client{Timeout: 15 * time.Second}
			dresp, derr := dclient.Get(durl)
			defer dresp.Body.Close()
			if derr != nil {
				panic(derr)
			}
			var dbuffer [2048]byte
			dresult := bytes.NewBuffer(nil)
			for {
				n, err := dresp.Body.Read(dbuffer[0:])
				dresult.Write(dbuffer[0:n])
				if err != nil && err == io.EOF {
					break
				} else if err != nil {
					panic(err)
				}
			}
			dinfo := dresult.String()
			fmt.Println(dinfo)
			var details EmployeeDetails
			json.Unmarshal([]byte(dinfo), &details)
			if details.Errmsg != "ok" {
				data := &RESPONSE{
					Code: 500,
					Msg:  "details faild",
				}
				this.Data["json"] = data
				this.ServeJSON()
			}
			for _, v := range details.Userlist {
				fmt.Println(details.Userlist)
				o := orm.NewOrm()
				var details []models.Employee_details
				num, err := o.Raw("select userid from department where userid = ?", v.Userid).QueryRows(&details)
				if err != nil {
					data := &RESPONSE{
						Code: 500,
						Msg:  err,
					}
					this.Data["json"] = data
					this.ServeJSON()
				}
				if num < 1 {
					fmt.Println(fmt.Printf("insert into employee_details(userid,unionid,order,mobile,tel,workPlace,remark,isAdmin,isBoss,isLeader,name) "+
						"values(?,?,?,?,?,?,?,?,?,?,?)", v.Userid, v.Unionid, v.Order, v.Mobile, v.Tel, v.WorkPlace, v.Remark, v.IsAdmin, v.IsBoss, v.IsLeader, v.Name))
					o := orm.NewOrm()
					_, err := o.Raw("insert into employee_details(unionid,openid,remark,userid,isadmin,isboss,IsHide,isleader,tel,department,workPlace,email,`order`," +
						"mobile,active,avatar,name,statecode,position) "+"values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", v.Unionid, v.OpenID, v.Remark, v.Userid, v.IsAdmin,
						v.IsBoss, v.IsHide, v.IsLeader, v.Tel, v.Department, v.WorkPlace,v.Email,v.Order,v.Mobile,v.Active,v.Avatar,v.Name,v.StateCode,v.Position).Exec()
					if err != nil {
						data := &RESPONSE{
							Code: 500,
							Msg:  err,
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
}