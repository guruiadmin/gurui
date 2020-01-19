package conf

import (
	"github.com/astaxie/beego/logs"
)

func init() {
	//设置日志输出
	logs.SetLogger("console")
	//设置日志输出级别
	logs.SetLevel(logs.LevelInformational)
	//设置是否输出文件名和行号
	logs.EnableFuncCallDepth(true)
	//异步输出日志 le3设置缓冲区大小
	logs.Async(1e3)
	//将日志输出到文件中
	logs.SetLogger(logs.AdapterFile, `{"filename":"dev.log"}`)
}
