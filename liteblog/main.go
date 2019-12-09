package main

import (
	_ "liteblog/routers"
	"github.com/astaxie/beego"
	"strings"
	_"liteblog/models"
)

func main() {
	initSession()
	initTemplate()
	beego.Run()
}

func initSession(){
	beego.BConfig.WebConfig.Session.SessionOn = true
	beego.BConfig.WebConfig.Session.SessionName = "liteblog-key"
	beego.BConfig.WebConfig.Session.SessionProvider = "file"
	beego.BConfig.WebConfig.Session.SessionProviderConfig = "data/session"
}

func initTemplate(){
	beego.AddFuncMap("equrl", func(x, y string) bool {
		s1 := strings.Trim(x, "/")
		y1 := strings.Trim(y, "/")
		return strings.Compare(s1, y1) == 0
	})
}

