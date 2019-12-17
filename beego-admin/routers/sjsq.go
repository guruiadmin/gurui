package routers

import (
	"beego-admin/controllers"
	"github.com/astaxie/beego"
)

func init() {

	/*
		公司内容管理   公司内容
	*/
	beego.Router("/sjsq/sjsqlist", &controllers.SjsqController{}, "get:SjsqList")
	beego.Router("/sjsq/sjsqlistadd", &controllers.SjsqController{}, "get:SjsqListAdd")
	beego.Router("/sjsq/sjsqlistaddto", &controllers.SjsqController{}, "post:SjsqListAddTo")
	beego.Router("/sjsq/sjsqlistup/:id", &controllers.SjsqController{}, "get:SjsqListUp")
	beego.Router("/sjsq/sjsqlistupto", &controllers.SjsqController{}, "post:SjsqListUpTo")
	beego.Router("/sjsq/sjsqlistdelete", &controllers.SjsqController{}, "post:SjsqListDelete")
	beego.Router("/sjsq/sjsqdata", &controllers.SjsqController{}, "get:SjsqData")

	/*
		审核管理	公司内容审核
	*/
	beego.Router("/sjsq/reviewlist", &controllers.SjsqController{}, "get:SjsqReviewList")
	beego.Router("/sjsq/reviewlistup/:id", &controllers.SjsqController{}, "get:SjsqReviewListUp")

	/*
		公司内容编辑	图片上传
	*/
	beego.Router("/file/addphoto", &controllers.SjsqController{}, "post:AddPhoto")

}
