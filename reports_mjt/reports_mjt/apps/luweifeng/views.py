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

        #检查查询类型 是否传
        name = request.GET.get('name')
        type = request.GET.get('type')
        useraddr = request.GET.get('useraddr')
        cursor = connections['default'].cursor()
        if type is None:
            return HttpResponse(json.dumps({"errmsg": "type参数未传", "errno": "4001"}), content_type="application/json")

        # 模糊查询返回用户地址，名字
        elif type == '0':
            if not name:
                return HttpResponse(json.dumps({"errmsg": "名字参数未传", "errno": "4001"}),content_type="application/json")
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

        #查询提货记录
        elif type == '1':

            # 模糊查询返回用户地址，名字
            if not useraddr:
                return HttpResponse(json.dumps({"errmsg": "用户地址参数未传", "errno": "4001"}),content_type="application/json")
            try:
                cursor.execute(
                    "select (select name from goods where id = g.goods_id),l.consignee_user_name,l.consignee_phone,l.detail_addr from take_order as o, take_order_logistics as l ,take_order_goods as g  where o.user_addr = '"+useraddr+"' and o.order_number = l.order_num and o.order_number = g.order_number "
                )
                receive = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "查询的用户名字不存在", "errno": "4001"}),content_type="application/json")
            data = []
            for info in receive:
                dict = {
                    '商品名字': info[0],
                    '提货人姓名': info[1],
                    '电话': info[2],
                    '详细地址': info[3],
                }
                data.append(dict)

            data = {'data': data, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")

        #查询个人所有记录
        elif type == '2':
            if not useraddr:
                return HttpResponse(json.dumps({"errmsg": "用户地址未传", "errno": "4001"}), content_type="application/json")
            #根据用户地址查询与之相关联的所有券的地址
            try:
                cursor.execute(
                    "select goodsAddr from relation where userAddr = '"+useraddr+"'"
                )
                goodsaddr = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "根据用户地址查询与之相关联的所有券的地址", "errno": "4001"}), content_type="application/json")
            if not goodsaddr:
                return HttpResponse(json.dumps({"errmsg": "没有和查询人物有关联的券", "errno": "4001"}),content_type="application/json")
            numreceiptslist = 0
            usernamelist = 0
            username = set()
            fromlist = set()
            # 获取 转赠数量
            try:
                cursor.execute(
                    "select sum(amount) from transfer_record where userAddr = '"+useraddr+"'"
                )
                giftgiv = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "转赠数量", "errno": "4001"}), content_type="application/json")
            # 获取 商品地址和提货数量
            try:
                cursor.execute(
                    "select sum(g.goods_amount) from take_order as o,take_order_goods as g where o.user_addr = '"+useraddr+"' and o.order_number = g.order_number"
                )
                takegood = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "商品地址和提货数量", "errno": "4001"}), content_type="application/json")
            for info in goodsaddr:
                #获取 商品地址和领取数量
                try:
                    cursor.execute(
                        "select sum(amount) from reviewrecord_"+info[0][-2::]+" where toAddr = '"+useraddr+"'"
                    )
                    numberreceipts = cursor.fetchall()
                except:
                    return HttpResponse(json.dumps({"errmsg": "商品地址和领取数量", "errno": "4001"}), content_type="application/json")
                if numberreceipts[0][0] is None:
                    pass
                else:
                    numreceiptslist += numberreceipts[0][0]

                # 获取 商品地址和剩余数量
                try:
                    cursor.execute(
                        "select sum(amount) from userbalance_"+info[0][-2::]+" where userAddress = '"+useraddr+"'"
                    )
                    fromuser = cursor.fetchall()
                except:
                    return HttpResponse(json.dumps({"errmsg": "商品地址和剩余数量", "errno": "4001"}), content_type="application/json")
                if fromuser[0][0] is None:
                    pass
                else:
                    usernamelist += fromuser[0][0]
                # 用户从哪里领取的
                try:
                    cursor.execute(
                        "select (select name from jld_user where id = fromAddr) from reviewrecord_"+info[0][-2::]+" where toAddr = '"+useraddr+"'"
                    )
                    userdata = cursor.fetchall()
                except:
                    return HttpResponse(json.dumps({"errmsg": "用户从哪里领取的", "errno": "4001"}),content_type="application/json")
                if userdata is None:
                    pass
                else:
                    for infodata in userdata:
                        if infodata[0]:
                            username.add(infodata[0])

                # 用户领取商品名字
                try:
                    cursor.execute(
                        "select (select name from goods where id = goodsAddr) from reviewrecord_" + info[0][-2::] + " where toAddr = '" + useraddr + "'"
                    )
                    userdata = cursor.fetchall()
                except:
                    return HttpResponse(json.dumps({"errmsg": "用户领取商品名字", "errno": "4001"}),content_type="application/json")
                if userdata[0][0] is None:
                    pass
                else:
                    for infogoods in userdata:
                        fromlist.add(infogoods[0])
            dict = {
                '用户领取卡劵数量': to_string(numreceiptslist),
                '用户转赠次数': to_string(giftgiv[0][0]),
                '用户余额数量': to_string(usernamelist),
                '用户提货数量': to_string(takegood[0][0]),
                '用户从哪里领取的': set_default(username),
                '用户领取商品名字': set_default(fromlist),
            }
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")

        # 查询券是转赠给谁
        elif type == '3':
            if useraddr is None:
                return HttpResponse(json.dumps({"errmsg": "type参数未传", "errno": "4001"}), content_type="application/json")
            fromlist = set()
            # 根据用户地址查询与之相关联的所有券的地址
            try:
                cursor.execute(
                    "select goodsAddr from relation where userAddr = '" + useraddr + "'"
                )
                goodsaddr = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "根据用户地址查询与之相关联的所有券的地址", "errno": "4001"}), content_type="application/json")
            if not goodsaddr:
                return HttpResponse(json.dumps({"errmsg": "没有和查询人物有关联的券", "errno": "4001"}),content_type="application/json")
            for info in goodsaddr:
                # 用户转增谁领取了
                try:
                    cursor.execute(
                        "select (select name from jld_user where id = toAddr) from reviewrecord_" + info[0][-2::] + " where fromAddr = '" + useraddr + "'"
                    )
                    fromaddr = cursor.fetchall()
                except:
                    return HttpResponse(json.dumps({"errmsg": "用户转增谁领取了", "errno": "4001"}),content_type="application/json")
                if not fromaddr:
                    pass
                else:
                    for name in fromaddr:
                        if name[0] is None:
                            pass
                        else:
                            fromlist.add(name[0])

            data = {"领券人名字": set_default(fromlist)}
            data = {'data': data, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"errmsg": "type参数错误", "errno": "4001"}), content_type="application/json")

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


'''
select * from jld_user where id = '0xf79eb7e9cf2aa4b90d8feb35079c2c4df35a32b2'
select * from jld_user where wx_nick_name = '跟我来'

select * from take_order, take_order_goods where take_order.order_number = '17225608751196' and take_order.order_number = take_order_goods.order_number
select (select name from jld_user where id = fromAddr) from reviewrecord_82 where toAddr = '0xcc03cdd44aadd8dbafa2e3f3d03718905216fa75'
select goodsAddr from relation where userAddr = '0x174f94ac054149ec49a64b250c70108647eec739'

select * from reviewrecord_7f where toAddr = '0x174f94ac054149ec49a64b250c70108647eec739'
'''