package models

import "time"

type Clinic struct {
	Clinic_id             string     `orm:"size(25); pk" json:"clinic_id"`
	Brand                 string    `orm:"size(25); description(门店品牌)" json:"brand"`
	Is_chain              string    `orm:"size(25); description(是否连锁（0否/1是）)" json:"is_chain"`
	Group_name            string    `orm:"size(255); description(集团名字)" json:"group_name"`
	Name                  string    `orm:"size(255); description(门店名称)" json:"name"`
	Branch_name           string    `orm:"size(255); description(分店名称)" json:"branch_name"`
	Attribution_group     string    `orm:"size(25); description(归属集团)" json:"attribution_group"`
	Attribution_city      string    `orm:"size(25); description(归属城市)" json:"attribution_city"`
	Business_circle       string    `orm:"size(255); description(所属商圈)" json:"business_circle"`
	Fixed_telephone       string    `orm:"size(255); description(门店固定电话)" json:"fixed_telephone"`
	Mobile_admin          string    `orm:"size(255); description(管理员手机号)" json:"mobile_admin"`
	Business_Hours        string    `orm:"size(25); description(营业时间)" json:"business_Hours"`
	Store_address         string    `orm:"size(25); description(门店地址)" json:"store_address"`
	Longitude_latitude    string    `orm:"size(255); description(经纬度)" json:"longitude_latitude"`
	Type_organization     string    `orm:"size(255); description(机构类型)" json:"type_organization"`
	Establishment_time    string    `orm:"size(255); description(经营性质)" json:"establishment_time"`
	Measure_area          string    `orm:"size(25); description(门店面积)" json:"measure_area"`
	Dental_chairs         string    `orm:"size(25); description(牙椅数量)" json:"dental_chairs"`
	Consultation_room     string    `orm:"size(255); description(诊室数量)" json:"consultation_room"`
	Child_consulting_room string    `orm:"size(255); description(儿童诊室数量)" json:"child_consulting_room"`
	Facilities            string    `orm:"size(255); description(门店设施)" json:"facilities"`
	Brand_introduction    string    `orm:"size(255); description(品牌介绍)" json:"brand_introduction"`
	Num_doctor            string    `orm:"size(255); description(医生数量)" json:"num_doctor"`
	Num_nurses            string    `orm:"size(255); description(护士数量)" json:"num_nurses"`
	Create_time           time.Time `orm:"auto_now; type(datetime); description(用户登录时间)" json:"create_time"`
}
