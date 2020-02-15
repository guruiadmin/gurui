package main

import (
	"encoding/json"
	"fmt"
	"github.com/astaxie/beego/orm"
	"report/models"
)

//import (
//	"fmt"
//)
//
//func fib(n int) int{
//	if n == 1{
//		return 1
//	}
//	if n == 2{
//		return 2
//	}else {
//		a := 1
//		b := 2
//		c := 0
//		for i := 3; i < n +1; i ++{
//			c = a + b
//			a = b
//			b = c
//		}
//		return c
//	}
//}
//
//func fib1(n int) int{
//	if n == 1 {
//		return 1
//	}
//	if n == 2 {
//		return 2
//	}else {
//		return fib(n - 1) + fib(n - 2)
//	}
//}
//
//func fib2(arry []int) int{
//	var slic = make([]int, len(arry))
//		slic[0] = arry[0]
//		if arry[0] < arry[1]{
//			slic[1] = arry[1]
//		}	else {
//			slic[1] = arry[0]
//		}
//		for i := 2; i < len(arry); i ++{
//			a := slic[i-2] + arry[i]
//			b := slic[i-1]
//			if a < b{
//				slic[i] = b
//			}else {
//				slic[i] = a
//			}
//		}
//		return slic[len(arry) - 1]
//}
//




func main(){
	type Server struct {
		Id   int
		Name string
		Parentid int
	}
	type Response struct {
		Errmsg string
		Errcode int

	}
	type Serverslice struct {
		Department []Server
		Msg Response
	}
	var s Serverslice
	str := `{"errcode":0,"department":[{"createDeptGroup":false,"name":"医生","id":155165256,"autoAddUser":false,"parentid":154921895},
{"createDeptGroup":true,"name":"实习生","id":170456964,"autoAddUser":true,"parentid":152515727}],"errmsg":"ok"}`
	json.Unmarshal([]byte(str), &s)
	fmt.Println(s.Msg.Errcode != 0)

	for _, v := range s.Department{
		o := orm.NewOrm()
		var department []models.Department
		num, _ := o.Raw("select id from department where id = ?", v.Id ).QueryRows(&department)

		if num < 1{
			fmt.Println("insert into department(id,name,parentid,ext) values(?,?,?,?)",v.Id, v.Name, v.Parentid)
			_, err := o.Raw("insert into department(id,name,parentid,ext) values(?,?,?)",v.Id, v.Name, v.Parentid).Exec()
			fmt.Println(err)
		}
	}
}










