package models

type Department struct {
	Id        int64     `orm:"auto; pk" json:"部门id"`
	Name  string    `orm:"size(25); description(部门名称)" json:"name"`
	Parentid  string    `orm:"size(25); description(父部门id，根部门为1)" json:"parentid"`
	Ext  string    `orm:"size(255); description(部门自定义字段)" json:"ext"`
}
