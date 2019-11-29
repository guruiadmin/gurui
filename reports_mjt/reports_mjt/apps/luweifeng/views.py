'''
/**
* Copyright ©2017-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 北京和信汇通科技开发有限公司 版权所有
*
*/
'''
import xlwt
from django.db import connections
from django.http import HttpResponse
import json
from django.views import View
import csv
from collections import OrderedDict

#根据人物查询
from reports_mjt.utils.decime import to_string


class PersonQuery(View):

    def get(self, request):

        name = 'BOSS'
        cursor = connections['default'].cursor()
        # 模糊查询返回用户地址，名字
        try:
            cursor.execute(
                "select name,id from jld_user where name LIKE '%" + name + "%'"
            )
            receive = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": 444, "errno": 44}))
        if receive:
            list = []
            for info in receive:
                dict = {
                    'name': info[0],
                    'useraddr': info[1],
                }
                list.append(dict)
            data = {'data': list, "errmsg": 44, "errno": 4444}
            return HttpResponse(json.dumps(data))




'''
select * from jld_user where id = '0xf79eb7e9cf2aa4b90d8feb35079c2c4df35a32b2'
select * from jld_user where wx_nick_name = '跟我来'

select * from take_order, take_order_goods where take_order.order_number = '17225608751196' and take_order.order_number = take_order_goods.order_number
select (select name from jld_user where id = fromAddr) from reviewrecord_82 where toAddr = '0xcc03cdd44aadd8dbafa2e3f3d03718905216fa75'
select goodsAddr from relation where userAddr = '0x174f94ac054149ec49a64b250c70108647eec739'

select * from reviewrecord_7f where toAddr = '0x174f94ac054149ec49a64b250c70108647eec739'
'''