package main

import (
	_"quickstart/conf"
	_ "quickstart/routers"
	"github.com/astaxie/beego"
	_ "github.com/astaxie/beego/session/redis"
)

func main() {
	beego.Run()
}

