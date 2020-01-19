package quickservice

import "github.com/astaxie/beego/orm"

//得到数据库中用户名为adminname密码为password的后台用户的数量
func getCount(adminname string, password string) int {
	o := orm.NewOrm()
	var count int
	o.Raw("select count(*) from jld_user where name=? and sex=?", adminname, password).QueryRow(&count)

	return count
}

//验证后台用户登录
func ValidateAdminLogin(adminname string, password string) bool {
	count := getCount(adminname, password)
	if count > 0 {
		return true
	} else {
		return false
	}
}
