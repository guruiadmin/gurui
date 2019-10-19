'''
/**
* Copyright ©2017-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 北京和信汇通科技开发有限公司 版权所有
*
*/
'''
from django.db import connections
from django.http import HttpResponse
import json
from django.views import View
from django_redis import get_redis_connection

from reports_mjt.utils.data_select import datedict
from reports_mjt.utils.decime import to_string


class OperationalData(View):
    def get(self, request):
        global null
        null = ''
        global false
        false = False
        cursor = connections['default'].cursor()
        redis_conn = get_redis_connection('default')
        # 获取搜索类型
        type = request.GET.get('type')
        token = request.GET.get('token')
        try:
            tokendata = eval(redis_conn.get(token))
        except:
            return HttpResponse(json.dumps({"errmsg": "token已过期", "errno": "4001"}), content_type="application/json")
        foreign_key = tokendata['foreignKey']
        manager_id = tokendata['managerId']
        if not all([type, token]):
            return HttpResponse(json.dumps({"errmsg": "type token参数未传", "errno": "4001"}), content_type="application/json")
        elif type == '0':
            # 商品总数
            try:
                cursor.execute(
                    "select count(id) from goods where foreign_key = '"+foreign_key+"' and name is not null"
                )
                numshopuser = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "商品总数", "errno": "4001"}),content_type="application/json")

            # 今日订单总量
            try:
                cursor.execute(
                    "select count(order_number) from purchase_order where manager_id = '"+manager_id+"' and order_state='1'and create_time bETWEEN '" + datedict['today'][0] + " 00:00:00' and '" + datedict['today'][0] + " 23:59:59' and pay_state ='1'"
                )
                todaybuyorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "今日订单总量", "errno": "4001"}), content_type="application/json")

            # 购买卡券用户
            try:
                cursor.execute(
                    "select count(distinct user_addr) from purchase_order where manager_id = '"+manager_id+"' and order_state='1'and create_time bETWEEN '" + datedict['today'][0] + " 00:00:00' and '" + datedict['today'][0] + " 23:59:59' and pay_state ='1'"
                )
                buycarduser = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "购买卡券用户", "errno": "4001"}), content_type="application/json")
            # 完成提货总量
            try:
                cursor.execute(
                    "select count(order_number) from take_order where manager_id = '"+manager_id+"' and create_date bETWEEN '" + datedict['today'][0] + " 00:00:00' and '" + datedict['today'][0] + " 23:59:59' and take_state = '3'"
                )
                ordertake = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "本周提货订单量", "errno": "4001"}),content_type="application/json")
            goodsidset = set()
            # 卡券转赠总数
            try:
                cursor.execute(
                    "select id,name ,initial_account from goods where foreign_key = '"+foreign_key+"' and name is not null"
                )
                goodsid = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "店铺地址名字", "errno": "4001"}), content_type="application/json")
            total = 0
            for info in goodsid:
                goodsidset.add(info[0][-2::])
                try:
                    cursor.execute(
                        "select sum(amount) from transfer_record where goodsAddr = '"+info[0]+"'"
                    )
                    result = cursor.fetchall()
                    if result[0][0] is not None:
                        total += int(result[0][0])
                except:
                    return HttpResponse(json.dumps({"errmsg": "转赠总数", "errno": "4001"}),  content_type="application/json")
            #领取卡券
            receive = 0
            for info in goodsidset:
                try:
                    cursor.execute(
                        "select sum(amount) from reviewrecord_"+info+" where type = '1' and goodsAddr in (select goodsAddr from goods where foreign_key = '"+foreign_key+"' and name is not null)"
                    )
                    result = cursor.fetchall()
                    if result[0][0] is not None:
                        receive += int(result[0][0])
                except:
                    return HttpResponse(json.dumps({"errmsg": "领取卡券", "errno": "4001"}), content_type="application/json")

            # 卡券剩余
            surplus = 0
            for info in goodsidset:
                try:
                    cursor.execute(
                        "SELECT sum(amount) from userbalance_" +info+ " where userAddress = '" + goodsid[0][2] + "'"
                    )
                    result = cursor.fetchall()
                    if result[0][0] is not None:
                        surplus += int(result[0][0])
                except:
                    return HttpResponse(json.dumps({"errmsg": "卡券剩余", "errno": "4001"}),content_type="application/json")

            dict = {
                'numshopuser': numshopuser[0][0],#商品总数
                'todaybuyorder': todaybuyorder[0][0],#今日订单总量
                'buycarduser': buycarduser[0][0],#购买卡券用户
                'ordertake': ordertake[0][0],#完成提货总量
                'totalnumcardcoupon':total,#卡券转赠总数
                'todaytotalviews':0,#今日总浏览量
                'totacardreceipt':receive,#卡券领取总量
                'totalcardsurplus':surplus,#卡券剩余总量
            }

            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")

        elif type == '1':
            goodsidset = set()
            # 卡券转赠总数
            try:
                cursor.execute(
                    "select id,name ,initial_account from goods where foreign_key = '" + foreign_key + "' and name is not null"
                )
                goodsid = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "店铺地址名字", "errno": "4001"}), content_type="application/json")
            for info in goodsid:
                goodsidset.add(info[0][-2::])
            #购买订单
            try:
                cursor.execute(
                    "select count(order_number) from purchase_order where manager_id = '"+manager_id+"' and order_state='1'and create_time BETWEEN '"+datedict['today'][0]+" 00:00:00' and '"+datedict['today'][0]+" 23:59:59' and pay_state = '1'"
                )
                buyorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "购买订单", "errno": "4001"}), content_type="application/json")
            # 提货订单
            try:
                cursor.execute(
                    "select count(order_number) from take_order where manager_id = '"+manager_id+"' and create_date BETWEEN '"+datedict['today'][0]+" 00:00:00' and '"+datedict['today'][0]+" 23:59:59'"
                )
                takeorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "提货订单", "errno": "4001"}), content_type="application/json")
            # 成交额
            try:
                cursor.execute(
                    "select COALESCE(SUM(actual_price),0) from purchase_order where manager_id = '"+manager_id+"' and order_state='1'and create_time BETWEEN '" + datedict['today'][0] + " 00:00:00' and '" + datedict['today'][0] + " 23:59:59'  and pay_state = '1'"
                )
                turnover = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "今日订单总量今日销售总额", "errno": "4001"}), content_type="application/json")
            # 领取卡券
            receive = 0
            for info in goodsidset:
                try:
                    cursor.execute(
                        "select sum(amount) from reviewrecord_" + info + " where type = '1' and goodsAddr in (select goodsAddr from goods where foreign_key = '" + foreign_key + "' and name is not null)"
                    )
                    result = cursor.fetchall()
                    if result[0][0] is not None:
                        receive += int(result[0][0])
                except:
                    return HttpResponse(json.dumps({"errmsg": "领取卡券", "errno": "4001"}),content_type="application/json")
            dict = {
                'buyorder': to_string(buyorder[0][0]),#购买订单
                'takeorder': takeorder[0][0],#提货订单
                'turnover':to_string(turnover[0][0]),#成交额
                'browsevolume':0,#浏览量
                'godsbowsed':0,#被浏览商品
                'crdreceipt':receive,#卡券领取
                 }
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")




