package main
//
//import (
//	"encoding/json"
//	"fmt"
//)
//
//type AutoGenerated struct {
//	Servers []struct {
//		ServerName string `json:"serverName"`
//		ServerIP string `json:"serverIP"`
//	} `json:"servers"`
//}
//
//func main() {
//	var s AutoGenerated
//	str := `{
//
//               "servers": [
//                   {
//                       "serverName": "Shanghai_VPN",
//                       "serverIP": "127.0.0.1"
//                   }, {
//                       "serverName": "Beijing_VPN",
//                       "serverIP": "127.0.0.2"
//                   }
//               ]
//           }`
//	json.Unmarshal([]byte(str), &s)
//	fmt.Println(str, "\n")
//	fmt.Println(s, "\n")
//	// 遍历Json
//	for key, val := range s.Servers {
//
//		// 打印索引和其他数据
//		println("Key：", key, "\tName：", val.ServerName, "\tIP：", val.ServerIP)
//	}
//}