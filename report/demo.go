package main


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
//func main(){
//	var data = []int{0,4,1,31,99,5,7}
//	f := fib2(data)
//	fmt.Println(f)
//	//start := time.Now()
//	//n := fib(20)
//	//fmt.Println(n)
//	//end := time.Now()
//	//fmt.Println(end.Sub(start))
//	//start1 := time.Now()
//	//n1 := fib1(400000)
//	//fmt.Println(n1)
//	//end1 := time.Now()
//	//fmt.Println(end1.Sub(start1))
//}

//
//import (
//	"encoding/json"
//	"fmt"
//)
//
//func main() {
//	jsonBuf := `
//    {
//        "company": "itcast",
//        "subjects": [
//            "Go",
//            "C++",
//            "Python",
//            "Test"
//        ],
//        "isok": true,
//        "price": 666.666
//    }
//    `
//	//创建一个map
//	m := make(map[string]interface{}, 4)
//	err := json.Unmarshal([]byte(jsonBuf), &m)
//	if err != nil {
//		fmt.Println("err=", err)
//		return
//	}
//	fmt.Println("m=", m)     //m= map[company:itcast subjects:[Go C++ Python Test] isok:true price:666.666]
//	fmt.Printf("m=%+v\n", m) //m=map[isok:true price:666.666 company:itcast subjects:[Go C++ Python Test]]
//
//	var s string
//	s = m["company"].(string)
//	fmt.Println("s= ", s) //s=  itcast
//
//	var s1 bool
//	s1 = m["isok"].(bool)
//	fmt.Println("s1= ", s1) //s1=  true
//
//	var s2 float64
//	s2 = m["price"].(float64)
//	fmt.Println("s2= ", s2) //s2=  666.666
//
//	var str string
//	//类型断言
//	for key, value := range m {
//		// fmt.Printf("%v===>%v\n", key, value)
//		switch data := value.(type) {
//		case string:
//			str = data
//			fmt.Printf("map[%s]的值类型为string，内容为%s\n", key, str)
//		case bool:
//			fmt.Printf("map[%s]的值类型为bool，内容为%v\n", key, data)
//		case float64:
//			fmt.Printf("map[%s]的值类型为float64，内容为%v\n", key, data)
//		case []string:
//			fmt.Printf("map[%s]的值类型为[]stiring1，内容为%v\n", key, data)
//		case []interface{}:
//			fmt.Printf("map[%s]的值类型为[]stiring2，内容为%v\n", key, data)
//		}
//		/*
//		   map[company]的值类型为string，内容为itcast
//		   map[subjects]的值类型为[]stiring2，内容为[Go C++ Python Test]
//		   map[isok]的值类型为bool，内容为true
//		   map[price]的值类型为float64，内容为666.666
//		*/
//	}
//}



