package main

import (
	"github.com/astaxie/beego/plugins/cors"
	_"quickstart/conf"
	_ "quickstart/routers"
	"github.com/astaxie/beego"
	_ "github.com/astaxie/beego/session/redis"
)

func main() {

	beego.InsertFilter("*", beego.BeforeRouter, cors.Allow(&cors.Options{
		AllowAllOrigins:  true,
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "Content-Type"},
		AllowCredentials: true,
	}))

	beego.Run()
}

