package main

import (
	"encoding/json"
	"fmt"
)

type Server struct {
	ServerName string
	ServerIP   string
}
type Serverslice struct {
	Servers []Server
}

func main() {
	var s Serverslice

	// 模拟传输的Json数据
	str :=`{
				"servers":[
					{
						"serverName":"医生",
						"serverIP":"154921895"
					}
					]
				}`
	//str := `{
    //           "servers": [
    //               {
    //                   "serverName": "Shanghai_VPN",
    //                   "serverIP": "127.0.0.1"
    //               }
    //           ]
    //       }`
	// 解析字符串为Json
	json.Unmarshal([]byte(str), &s)
	fmt.Println(s.Servers)
	// 遍历Json
	for key, val := range s.Servers {

		// 打印索引和其他数据
		println("Key：", key, "\tName：", val.ServerName, "\tIP：", val.ServerIP)
	}
}