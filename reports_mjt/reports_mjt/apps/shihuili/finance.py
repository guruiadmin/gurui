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
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
import json

from public.models import GoodsOrm, ManageOrm
from public.serializers import ManageSerializers
from reports_mjt.utils.decime import to_string
from reports_mjt.utils.ormdate import OrmFunctionObject

ormfunc = OrmFunctionObject()


class FinanceClass(ReadOnlyModelViewSet):
    @action(methods=['POST'], detail=False)
    def fina(self, request):
        distrdict = {
            '0': AllManageSerialiZers().funcdata(request),
            '1': GoodsSerialiZers().funcdata(request),
        }
        return distrdict.get(request.data.get('type'), AllManageSerialiZers().funcdata(request))


#查询所有商家
class AllManageSerialiZers(ReadOnlyModelViewSet):
    serializer_class = ManageSerializers
    queryset = ManageOrm.objects.all()
    def funcdata(self, request):
        total = ManageOrm.objects.filter(name__isnull=False).count()
        allorg = ManageOrm.objects.filter(name__isnull=False)[(int(request.data.get('page'))-1)*int(request.data.get('num')):int(request.data.get('page'))*int(request.data.get('num'))]
        serializer = ManageSerializers(allorg, context={'request': request}, many=True)
        dict = {'data': serializer.data, 'total': total, "errmsg": "成功", "errno": "0"}
        return Response(dict)


#查询商家所有商品
class GoodsSerialiZers(object):
    def funcdata(self, request):
        manager_id = request.data.get('manager_id', 'zhaomemgqiqizai')
        startime = request.data.get('start', '2018-01-01')
        endtime = request.data.get('end', '2018-01-01')
        page = int(request.data.get('page', 1))
        num = int(request.data.get('num', 10))
        cursor = connections['default'].cursor()
        goodsidlist = set()
        goodsdatalist = []
        start, end = ormfunc.startend(startime, endtime)

        # 全部订单量 团购价
        try:
            cursor.execute(
                "select g.goods_id,count(g.order_number),g.goods_group_price from take_order_goods as g, take_order as o where o.manager_id = '"+manager_id+"' and o.create_date BETWEEN '"+start+"' and '"+end+"' and g.order_number = o.order_number and o.order_state = '0' GROUP BY g.goods_id")
            totalorder = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "全部订单量", "errno": "4001"}), content_type="application/json")
        for goodsid in totalorder:
            goodsidlist.add(goodsid[0])
        # 团购订单量
        try:
            cursor.execute(
                "select g.goods_id,count(g.order_number) from take_order_goods as g, take_order as o where o.manager_id = '"+manager_id+"' and o.create_date BETWEEN '"+start+"' and '"+end+"' and g.order_number = o.order_number and o.order_state = '0' and o.order_type = '1' GROUP BY g.goods_id")
            groupbuy = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "团购订单量", "errno": "4001"}), content_type="application/json")
        for goodsid in groupbuy:
            goodsidlist.add(goodsid[0])
        # 零售免费订单量
        try:
            cursor.execute(
                "select g.goods_id,count(g.order_number) from take_order_goods as g, take_order as o where o.manager_id = '"+manager_id+"' and o.create_date BETWEEN '"+start+"' and '"+start+"' and g.order_number = o.order_number and o.order_state = '0' and o.order_type = '0' GROUP BY g.goods_id")
            retailorder = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "零售免费订单量", "errno": "4001"}), content_type="application/json")
        for goodsid in retailorder:
            goodsidlist.add(goodsid[0])
        # 零售订单金额
        try:
            cursor.execute(
                "select g.goods_id,sum(actual_price) from purchase_order as o, purchase_order_goods as g where o.manager_id = '"+manager_id+"' and o.create_time BETWEEN '"+start+"' and '"+end+"' and o.order_number = g.order_number and o.order_state = '1' and o.payment = '1' and o.pay_state ='1' GROUP BY g.goods_id")
            retailprice = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "零售订单金额", "errno": "4001"}), content_type="application/json")
        for goodsid in retailprice:
            goodsidlist.add(goodsid[0])
        # 活动订单金额
        try:
            cursor.execute(
                "select g.goods_id,sum(actual_price) from purchase_order as o, purchase_order_goods as g where o.manager_id = '"+manager_id+"' and o.create_time BETWEEN '"+start+"' and '"+end+"' and o.order_number = g.order_number and o.order_state = '1' and o.payment = '2' and o.pay_state ='1' GROUP BY g.goods_id")
            activiprice = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "活动订单金额", "errno": "4001"}), content_type="application/json")
        for goodsid in activiprice:
            goodsidlist.add(goodsid[0])
        # 销售总金额
        try:
            cursor.execute(
                "select g.goods_id,sum(actual_price) from purchase_order as o, purchase_order_goods as g where o.manager_id = '"+manager_id+"' and o.create_time BETWEEN '"+start+"' and '"+end+"' and o.order_number = g.order_number and o.order_state = '1' and o.pay_state ='1' GROUP BY g.goods_id")
            totalprice = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "销售总金额", "errno": "4001"}), content_type="application/json")
        for goodsid in totalprice:
            goodsidlist.add(goodsid[0])

        # 使用代言券数量 代言券总抵扣金额 代言佣金总额 最终收入金额
        try:
            cursor.execute(
                "SELECT g.goods_id,count(g.coupons_addr),(count(g.coupons_addr) * (SELECT represent_price FROM goods WHERE id = (SELECT DISTINCT goods_id FROM purchase_order_goods WHERE coupons_addr = g.coupons_addr))),(count(g.coupons_addr) * (SELECT represent_commission FROM goods WHERE id = (SELECT DISTINCT goods_id FROM purchase_order_goods WHERE coupons_addr = g.coupons_addr))),sum(actual_price) - (count(g.coupons_addr) * (SELECT represent_commission FROM goods WHERE id = (SELECT DISTINCT goods_id FROM	purchase_order_goods WHERE	coupons_addr = g.coupons_addr)))FROM purchase_order AS o,purchase_order_goods AS g	WHERE o.manager_id = '"+manager_id+"'	AND o.create_time BETWEEN '"+start+"'AND '"+end+"' AND o.order_number = g.order_number AND o.order_state = '1' AND o.pay_state ='1' AND g.is_coupons = '1' GROUP BY g.goods_id")
            couponsnumprice = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "最终收入金额", "errno": "4001"}), content_type="application/json")
        for goodsid in couponsnumprice:
            goodsidlist.add(goodsid[0])
        #拼接商品字典
        for id in goodsidlist:

            # 规格型号
            try:
                cursor.execute(
                    "select specification_id1 from goods_property where goods_id ='"+id+"'")
                specification = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "规格型号", "errno": "4001"}), content_type="application/json")
            try:
                data = GoodsOrm.objects.filter(id=id)
            except GoodsOrm.DoesNotExist:
                return HttpResponse(status=404)
            for info in data:
                goodsdatalist.append({
                    'name': info.name, #商品名称
                    'id': info.id, #商品ID
                    'specification': specification[0][0], #规格型号
                    'market_price': to_string(info.market_price), #零售单价
                    'activity_pricr': 0, #活动单价
                    'total_delivery': 0, #总提货订单量
                    'retail_order': 0, #零售订单量
                    'activity_order': 0, #活动订单量
                    # 'free_order': 0, #免费提货量
                    'retail_amount': 0, #零售订单金额
                    'activity_amount': 0, #活动订单金额
                    'total_sales': 0, #销售总额
                    'voucher_deduction': to_string(info.represent_price), #代言券抵扣金额
                    'vocher_num': 0,#使用代言券数量
                    'totalvocher_price': 0,#代言券总抵扣金额
                    'commission': to_string(info.represent_commission), # 代言人佣金
                    'totalcommission': 0 ,# 佣金扣除总额
                    'final_revenue': 0, #最终收入金额
                })
        for key, info in enumerate(goodsdatalist):
            for data in totalorder:
                if info['id'] == data[0]:
                    goodsdatalist[key]['total_delivery'] = to_string(data[2])
                    goodsdatalist[key]['activity_pricr'] = data[1]
                break
        for key, info in enumerate(goodsdatalist):
            for data in groupbuy:
                if info['id'] == data[0]:
                    goodsdatalist[key]['activity_order'] = data[1]
                break
        for key, info in enumerate(goodsdatalist):
            for data in retailorder:
                if info['id'] == data[0]:
                    goodsdatalist[key]['retail_order'] = to_string(data[1])
                break
        for key, info in enumerate(goodsdatalist):
            for data in retailprice:
                if info['id'] == data[0]:
                    goodsdatalist[key]['retail_amount'] = to_string(data[1])
                break
        for key, info in enumerate(goodsdatalist):
            for data in activiprice:
                if info['id'] == data[0]:
                    goodsdatalist[key]['activity_amount'] = to_string(data[1])
                break
        for key, info in enumerate(goodsdatalist):
            for data in totalprice:
                if info['id'] == data[0]:
                    goodsdatalist[key]['total_sales'] = to_string(data[1])
                break
        for key, info in enumerate(goodsdatalist):
            for data in couponsnumprice:
                if info['id'] == data[0]:
                    goodsdatalist[key]['vocher_num'] = to_string(data[1])
                    goodsdatalist[key]['totalvocher_price'] = to_string(data[2])
                    goodsdatalist[key]['totalcommission'] = to_string(data[3])
                    goodsdatalist[key]['final_revenue'] = to_string(data[4])
                break
        data = {'data': {'tdgoods': goodsdatalist[(page - 1) * num:page * num], 'total': len(goodsdatalist)}, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")




'''
select (select name from goods where id = g.goods_id), sum(g.goods_amount),(sum(g.goods_amount) * (select market_price from goods where id = g.goods_id)),(sum(g.goods_amount) * (select market_price from goods where id = g.goods_id)) - sum(o.actual_price) ,sum(o.actual_price) from purchase_order as o, purchase_order_goods as g where o.pay_state = '1' and g.order_number = o.order_number GROUP BY g.goods_id ORDER BY o.CREATE_time desc
'''