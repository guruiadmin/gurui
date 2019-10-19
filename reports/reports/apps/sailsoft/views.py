'''
/**
* Copyright ©2019-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 合颌科技（北京）有限公司 版权所有
*
*/
'''
from django.db import connections
from django.http import HttpResponse
import json
from django.views import View


class GuRui(View):

    def get(self, request):

        name = request.GET.get('user')
        cursor = connections['default'].cursor()

        # 模糊查询返回用户地址，名字
        try:
            cursor.execute(
                "select name,id from jld_user where name LIKE '%" + name + "%'"
            )
            receive = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "查询的用户名字不存在", "errno": "4001"}),content_type="application/json")
        if not receive:
            return HttpResponse(json.dumps({"errmsg": "没有符合条件的用户名", "errno": "4001"}), content_type="application/json")
        list = []
        for info in receive:
            dict = {
                'name': info[0],
                'useraddr': info[1],
            }
            list.append(dict)
        data = {'data': list, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")