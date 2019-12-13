'''
/**
* Copyright ©2017-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 北京和信汇通科技开发有限公司 版权所有
*
*/
'''
from collections import OrderedDict
from django.db import connections
from django.db.models import Q
from django.db.models import Sum, Count
from django.http import HttpResponse
import json
from django.views import View
from public.models import PurchaseOrder, UserData, TakeOrder, ManageOrm, TakeOrderLogistics, TakeOrderGoods, GoodsOrm, PurchaseOorderGoods, \
    PurchaseOrderLogistics, GoodsProperty
from reports_mjt.utils.apiauth import APIAuthParameter
from reports_mjt.utils.data_select import str_time_stamp
from reports_mjt.utils.decime import to_string
from reports_mjt.utils.ormdate import OrmFunctionObject, merchant

ormfunc = OrmFunctionObject()


class ClaOrganizationViewSeet(View):
    # 商家通过量
    def get(self, request):
        
        return TypeClass(request).create()


class TypeClass(APIAuthParameter):


    def create(self):
        distrdict = {
            '0': OrgOrder(self.request).funcdata(), #主页信息
            '2': OrgrName(self.request).funcdata(), #提货详情
            '3': ManageOrgname(self.request).funcdata(), #够买详情
            '1': ManGer(self.request).funcdata(), #根据厂家查询详情
            '4': Finance(self.request).funcdata(),  # 财务数据返回
            '5': Finance(self.request).funcdata1(),  # 财务数据返回
            '6': Finance(self.request).funcdata2(),  # 财务数据返回
        }
        if str(self.type) in distrdict:
            return distrdict[str(self.type)]
        else:
            return HttpResponse(json.dumps({"errmsg": "type参数错误", "errno": "400"}),content_type="application/json")


class OrgOrder(object):
    
    def __init__(self, request):
        self.manage = APIAuthParameter(request).manage()
    def funcdata(self):
        try:
            buyorder = PurchaseOrder.objects.values('manager_id').filter(pay_time__range=(self.manage['startTime'], self.manage['endTime']), pay_state='1', order_state='1').annotate(count=Count('order_number')).annotate(money=Sum('actual_price'))
            takeorder = TakeOrder.objects.values('manager_id').exclude(order_state='1').filter(create_date__range=(self.manage['startTime'], self.manage['endTime']), order_state='0', take_state__in=[0, 1, 2, 3]).annotate(count=Count('order_number'))
			
        except PurchaseOrder.DoesNotExist:
            return HttpResponse(status=404)
		print()
		print()
        return HttpResponse(json.dumps(ormfunc.buytake(takeorder, buyorder, merchant(), self.manage['pages'], self.manage['numberbars'])), content_type="application/json")


class ManGer(object):
    
    def __init__(self, request):
        self.manage = APIAuthParameter(request).manage()
    
    def funcdata(self):
        if self.manage['manager_id'] == 'manager_id':
            try:
                buyorder = PurchaseOrder.objects.values('manager_id').filter(pay_time__range=(self.manage['startTime'], self.manage['endTime']), order_state='1', pay_state='1').annotate(count=Count('order_number')).annotate(money=Sum('actual_price'))
            except PurchaseOrder.DoesNotExist:
                return HttpResponse(status=404)
            if self.manage['state'] == 'undefined':
                try:
                    takeorder = TakeOrder.objects.values('manager_id').filter(create_date__range=(self.manage['startTime'], self.manage['endTime']), order_state='0', take_state__in=[0, 1, 2, 3]).annotate(count=Count('order_number'))
                except TakeOrder.DoesNotExist:
                    return HttpResponse(status=404)
            else:
                try:
                    takeorder = TakeOrder.objects.values('manager_id').filter(create_date__range=(self.manage['startTime'], self.manage['endTime']), order_state='0', take_state=self.manage['state'], take_state__in=[0, 1, 2, 3]).annotate(count=Count('order_number'))
                except TakeOrder.DoesNotExist:
                    return HttpResponse(status=404)

        else:
            try:
                buyorder = PurchaseOrder.objects.values('manager_id').exclude(order_state='0').filter(manager_id=self.manage['manager_id'], pay_time__range=(self.manage['startTime'], self.manage['endTime']), pay_state='1').annotate(count=Count('order_number')).annotate(money=Sum('actual_price'))
            except PurchaseOrder.DoesNotExist:
                return HttpResponse(status=404)
            if self.manage['state'] == 'undefined':
                try:
                    takeorder = TakeOrder.objects.values('manager_id').filter(manager_id=self.manage['manager_id'], create_date__range=(self.manage['startTime'], self.manage['endTime']), order_state='0', take_state__in=[0, 1, 2, 3]).annotate(count=Count('order_number'))
                except TakeOrder.DoesNotExist:
                    return HttpResponse(status=404)
            else:
                try:
                    takeorder = TakeOrder.objects.values('manager_id').filter(manager_id=self.manage['manager_id'], create_date__range=(self.manage['startTime'], self.manage['endTime']), order_state='0', take_state=self.manage['state'], take_state__in=[0, 1, 2, 3]).annotate(count=Count('order_number'))
                except TakeOrder.DoesNotExist:
                    return HttpResponse(status=404)
        setlist = set()
        for takeid in takeorder:
            setlist.add(takeid['manager_id'])
        for buyid in buyorder:
            setlist.add(buyid['manager_id'])
        selectlist = []
        for manageid in setlist:
            try:
                managename = ManageOrm.objects.filter(Q(id=manageid) & Q(name__isnull=False)).order_by('id')
            except ManageOrm.DoesNotExist:
                return HttpResponse(status=404)
            for name in managename:
                selectlist.append({'id': name.id, 'date': [self.manage['start'], self.manage['end']], 'orgName': name.name, 'purchase': 0,'total': 0, 'tabkegoods': 0})
        return HttpResponse(json.dumps(ormfunc.buytake(takeorder, buyorder, selectlist, self.manage['pages'], self.manage['numberbars'])), content_type="application/json")


class OrgrName(object):
    
    def __init__(self, request):
        self.manage = APIAuthParameter(request).manage()
    
    def funcdata(self):
        list = []
        goodslist = []
        logisticslist = []
        goodsnamelist = []
        propertylist = []
        try:
            total = TakeOrder.objects.exclude(order_state='1').filter(manager_id=self.manage['manager_id'], create_date__range=(self.manage['startTime'], self.manage['endTime']), take_state__in=[0, 1, 2, 3])
            takeordernum = TakeOrder.objects.exclude(order_state='1').filter(manager_id=self.manage['manager_id'],create_date__range=(self.manage['startTime'], self.manage['endTime']), take_state__in=[0, 1, 2, 3]).order_by('-create_date')[(self.manage['pages'] - 1) * self.manage['numberbars']:self.manage['pages'] * self.manage['numberbars']]
        except TakeOrder.DoesNotExist:
            return HttpResponse(status=404)
        for order in takeordernum:
            list.append(
                {'goodsName': '', 'brief': '', 'orderNum': order.order_number, 'userName': order.user_name, 'phone': '',
                 'amount': '', 'msg': order.user_msg, 'province': '', 'city': '', 'area': '', 'detailAddr': '',
                 'state': order.take_state, 'logisticsCompany': '', 'LogisticsNum': '', 'goodsid': '', 'price': '',
                 'group_price': '', 'date': str_time_stamp(order.create_date.strftime('%Y-%m-%d %H:%M:%S'))})
            try:
                goodsdernum = TakeOrderGoods.objects.filter(order_number=order.order_number)
                logisticsdernum = TakeOrderLogistics.objects.filter(order_num=order.order_number)
                goodslist.append(goodsdernum)
                logisticslist.append(logisticsdernum)
            except UserData.DoesNotExist:
                return HttpResponse(status=404)
        for id in goodslist:
            for data in id:
                try:
                    goodsname = GoodsOrm.objects.filter(id=data.goods_id)
                    goodsnamelist.append(goodsname)
                    property = GoodsProperty.objects.filter(goods_id=data.goods_id)
                    propertylist.append(property)
                except UserData.DoesNotExist:
                    return HttpResponse(status=404)
        for key, info in enumerate(list):
            for goodsid in goodslist:
                for data in goodsid:
                    if info['orderNum'] == data.order_number:
                        list[key]['amount'] = data.goods_amount
                        list[key]['goodsid'] = data.goods_id
                    break
        for key, info in enumerate(list):
            for goodsid in goodsnamelist:
                for data in goodsid:
                    if info['goodsid'] == data.id:
                        list[key]['brief'] = data.brief
                        list[key]['goodsName'] = data.name
                    break
        for key, info in enumerate(list):
            for goodsid in propertylist:
                for data in goodsid:
                    if info['goodsid'] == data.goods_id:
                        list[key]['price'] = to_string(data.price)
                        list[key]['group_price'] = to_string(data.group_price)
                    break
        for key, info in enumerate(list):
            for goodsid in logisticslist:
                for data in goodsid:
                    if info['orderNum'] == data.order_num:
                        list[key]['phone'] = data.consignee_phone
                        list[key]['province'] = data.province
                        list[key]['city'] = data.city
                        list[key]['area'] = data.area
                        list[key]['detailAddr'] = data.detail_addr
                        list[key]['logisticsCompany'] = data.logistics_company
                        list[key]['LogisticsNum'] = data.logistics_num
                    break
        dict = {'tdgoods': list}
        dict['totalnum'] = len(total)
        data = {'data': dict, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")


class ManageOrgname(object):
    
    def __init__(self, request):
        self.manage = APIAuthParameter(request).manage()
    
    def funcdata(self):
        list = []
        goodslist = []
        logisticslist = []
        goodsnamelist = []
        try:
            total = PurchaseOrder.objects.filter(manager_id=self.manage['manager_id'], pay_time__range=(self.manage['startTime'], self.manage['endTime']), pay_state='1', order_state='1')
            buyordernum = PurchaseOrder.objects.filter(manager_id=self.manage['manager_id'], pay_time__range=(self.manage['startTime'], self.manage['endTime']), pay_state='1', order_state='1').order_by('-create_time')[(self.manage['pages'] - 1) * self.manage['numberbars']:self.manage['pages'] * self.manage['numberbars']]
        except PurchaseOrder.DoesNotExist:
            return HttpResponse(status=404)
        for data in buyordernum:
            list.append(
                {'orderNum': data.order_number, 'userName': '', 'phone': '', 'amount': '', 'province': '', 'city': '',
                 'area': '', 'detailAddr': '', 'goodsName': '', 'brief': '', 'value': '',
                 'amountmoney': to_string(data.actual_price), 'isUseCoupons': '', 'goodsid': '', 'date': str_time_stamp(data.create_time.strftime('%Y-%m-%d %H:%M:%S'))}
            )
            try:
                goodsdernum = PurchaseOorderGoods.objects.filter(order_number=data.order_number)
                logisticsdernum = PurchaseOrderLogistics.objects.filter(order_num=data.order_number)
                goodslist.append(goodsdernum)
                logisticslist.append(logisticsdernum)
            except PurchaseOorderGoods.DoesNotExist:
                return HttpResponse(status=404)
        for id in goodslist:
            for data in id:
                try:
                    goodsname = GoodsOrm.objects.filter(id=data.goods_id)
                    goodsnamelist.append(goodsname)
                except UserData.DoesNotExist:
                    return HttpResponse(status=404)
        for key, info in enumerate(list):
            for goodsid in goodslist:
                for data in goodsid:
                    if info['orderNum'] == data.order_number:
                        list[key]['amount'] = data.goods_amount
                        list[key]['goodsid'] = data.goods_id
                        list[key]['isUseCoupons'] = data.is_coupons
                    break
        for key, info in enumerate(list):
            for goodsid in goodsnamelist:
                for data in goodsid:
                    if info['goodsid'] == data.id:
                        list[key]['brief'] = data.brief
                        list[key]['goodsName'] = data.name
                        list[key]['value'] = to_string(data.market_price)
                    break
        for key, info in enumerate(list):
            for goodsid in logisticslist:
                for data in goodsid:
                    if info['orderNum'] == data.order_num:
                        list[key]['userName'] = data.consignee_user
                        list[key]['phone'] = data.consignee_phone
                        list[key]['province'] = data.province
                        list[key]['city'] = data.city
                        list[key]['area'] = data.area
                        list[key]['detailAddr'] = data.detail_addr
                        list[key]['logisticsCompany'] = data.logistics_company
                        list[key]['LogisticsNum'] = data.logistics_num
                    break
        dict = {'tdgoods': list}
        dict['totalnum'] = len(total)
        data = {'data': dict, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")


class Finance(object):
    def __init__(self, request):
        self.manage = APIAuthParameter(request).finance()

    def funcdata(self):
        cursor = connections['default'].cursor()
        # 商户商品信息
        try:
            cursor.execute(
                "select m.id,m.name,s.id,s.name,s.circulation, s.initial_account from goods as s, manager as m where s.state in ('2','4') and  s.foreign_key = m.foreign_key and s.name is not null GROUP BY s.id ORDER BY m.id, s.id desc "
            )
            shopgoods = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "商户商品信息", "errno": "4001"}), content_type="application/json")


        # 购买详情
        try:
            cursor.execute(
                "select g.goods_id,sum(g.goods_amount),sum(o.actual_price) from purchase_order as o, purchase_order_goods as g where o.pay_time BETWEEN '" + self.manage['startTime'] + "' and '" + self.manage['endTime'] + "' and  o.pay_state = '1' and g.order_number = o.order_number  GROUP BY g.goods_id "
            )
            buygodos = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "购买详情", "errno": "4001"}), content_type="application/json")

        # 提货详情
        try:
            cursor.execute(
                "select g.goods_id,sum(g.goods_amount) from take_order_goods as g, take_order as o where o.order_state = '0' and o.take_state in('2','3') and o.order_number = g.order_number GROUP BY g.goods_id "
            )
            takegoods = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "提货详情", "errno": "4001"}), content_type="application/json")

        # 提货详情
        try:
            cursor.execute(
                "select g.goods_id,sum(g.goods_amount) from take_order_goods as g, take_order as o where o.create_date BETWEEN '" + self.manage['startTime'] + "' and '" + self.manage['endTime'] + "' and o.order_state = '0' and o.take_state in('2','3') and o.order_number = g.order_number GROUP BY g.goods_id "
            )
            takegoodss = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "提货详情", "errno": "4001"}), content_type="application/json")

        resultdict = []
        surplus = []
        for info in shopgoods:
            datadict = OrderedDict()
            datadict['manageid'] = info[0]
            datadict['managename'] = info[1]
            datadict['goodsid'] = info[2]
            datadict['goodsname'] = info[3]
            datadict['totalnum'] = info[4]
            datadict['surplus'] = info[4]
            datadict['buynum'] = 0
            datadict['buyprice'] = 0
            datadict['takenum'] = 0

            resultdict.append(datadict)
            # 获取 商品地址和剩余数量
            try:
                cursor.execute(
                    "select goodsAddr,sum(amount) from userbalance_" + info[2][-2::] + " where userAddress != '" + info[5] + "' and goodsAddr = '" + info[2] + "'"
                )
                fromuser = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "商品地址和数量", "errno": "4001"}),  content_type="application/json")
            if fromuser[0][0] is not None:
                surplus.append(fromuser)

        for info in buygodos:
            for data in resultdict:
                if data['goodsid'] == info[0]:
                    data['buynum'] = to_string(info[1])
                    data['buyprice'] = to_string(info[2])

        for info in takegoods:
            for data in resultdict:
                if data['goodsid'] == info[0]:
                    data['surplus'] = data['totalnum'] - to_string(info[1])
        for info in takegoodss:
            for data in resultdict:
                if data['goodsid'] == info[0]:
                    data['takenum'] = to_string(info[1])
        for info in surplus:
            for key, data in enumerate(resultdict):
                if data['goodsid'] == info[0][0]:
                    data['surplus'] = data['surplus'] - to_string(info[0][1])

        dict = {'goodsdata': resultdict[(self.manage['pages'] - 1) * self.manage['numberbars']:self.manage['pages'] * self.manage['numberbars']]}
        dict['totalnum'] = len(shopgoods)
        data = {'data': dict, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")


    def funcdata1(self):
        cursor = connections['default'].cursor()
        totslprice = 0
        # 用户提现
        try:
            cursor.execute(
                "select r.mchid,(select real_name from jld_user_authentication where user_id = r.user_id), (select idcard from jld_user_authentication where user_id = r.user_id), sum(r.amount) from withdrawals_record as r where r.audit_time BETWEEN '" + self.manage['startTime'] + "' and '" + self.manage['endTime'] + "' and r.state = '1' GROUP BY user_id ORDER BY sum(r.amount) limit {}, {}".format(self.manage['pages'] - 1, self.manage['numberbars'])
            )
            shopgoods = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "用户提现1", "errno": "4001"}), content_type="application/json")

        try:
            cursor.execute(
                "select r.mchid from withdrawals_record as r where r.audit_time BETWEEN '" + self.manage['startTime'] + "' and '" + self.manage['endTime'] + "' and r.state = '1' GROUP BY user_id ORDER BY sum(r.amount)  "
            )
            total = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "用户提现2", "errno": "4001"}), content_type="application/json")

        try:
            cursor.execute(
                "select sum(r.amount) from withdrawals_record as r where r.audit_time BETWEEN '" + self.manage['startTime'] + "' and '" + self.manage['endTime'] + "' and r.state = '1' GROUP BY user_id ORDER BY sum(r.amount)  "
            )
            price = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "用户提现2", "errno": "4001"}), content_type="application/json")
        if price:
            totslprice = price[0][0]
        resultdict = []

        if shopgoods:
            for info in shopgoods:
                resultdict.append({
                    'order': info[0],
                    'date': self.manage['date'],
                    'user': info[1],
                    'id': info[2],
                    'amount_money': float(info[3]),
                })

        dict = {'userdata': resultdict}
        dict['totalnum'] = len(total)
        dict['totalprice'] = totslprice
        return HttpResponse(json.dumps({'data': dict, "errmsg": "成功", "errno": "0"}), content_type="application/json")


    def funcdata2(self):
        cursor = connections['default'].cursor()
        totslprice = 0
        # 用户提现
        try:
            cursor.execute(
                "select r.partner_trade_no,(select real_name from jld_user_authentication where user_id = r.user_id), (select idcard from jld_user_authentication where user_id = r.user_id), sum(r.amount), unix_timestamp(r.audit_time) from withdrawals_record as r where r.user_id = '" + self.manage['userid'] + "' and  r.audit_time BETWEEN '" + self.manage['startTime'] + "' and '" + self.manage['endTime'] + "' and r.state = '1' GROUP BY r.partner_trade_no ORDER BY sum(r.amount) limit {}, {}".format(self.manage['pages'] - 1, self.manage['numberbars'])
            )
            shopgoods = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "用户提现1", "errno": "4001"}), content_type="application/json")

        try:
            cursor.execute(
                "select r.mchid from withdrawals_record as r where r.user_id = '" + self.manage['userid'] + "' and  r.audit_time BETWEEN '" + self.manage['startTime'] + "' and '" + self.manage['endTime'] + "' and r.state = '1' GROUP BY r.partner_trade_no ORDER BY sum(r.amount)  "
            )
            total = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "用户提现2", "errno": "4001"}), content_type="application/json")

        try:
            cursor.execute(
                "select sum(r.amount) from withdrawals_record as r where r.user_id = '" + self.manage['userid'] + "' and  r.audit_time BETWEEN '" + self.manage['startTime'] + "' and '" + self.manage['endTime'] + "' and r.state = '1' GROUP BY r.partner_trade_no ORDER BY sum(r.amount)  "
            )
            price = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "用户提现2", "errno": "4001"}), content_type="application/json")
        if price:
            totslprice = price[0][0]
        resultdict = []

        if shopgoods:
            for info in shopgoods:
                resultdict.append({
                    'order': info[0],
                    'date': info[4],
                    'user': info[1],
                    'id': info[2],
                    'amount_money': float(info[3]),
                })

        dict = {'userdata': resultdict}
        dict['totalnum'] = len(total)
        dict['totalprice'] = totslprice
        return HttpResponse(json.dumps({'data': dict, "errmsg": "成功", "errno": "0"}), content_type="application/json")


