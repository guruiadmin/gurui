'''
/**
* Copyright ©2017-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 北京和信汇通科技开发有限公司 版权所有
*
*/
'''
import json
from django.db import connections
from django.http import HttpResponse
import datetime
from django.views import View

from reports_mjt.utils.apiauth import APIAuthParameter
from reports_mjt.utils.data_select import FunctionObject, monthtime, yeartime, yearmonthday, localutc
from reports_mjt.utils.decime import to_string
func = FunctionObject()

#商家通过量天统计
class Organization(View):

    #商家通过量
    def get(self, request):
        global cursor
        cursor = connections['default'].cursor()
        return DistributionClass(request).distribution()

class DistributionClass(APIAuthParameter):


    def distribution(self):
        distrdict = {
            '0': ReporesClass0(self.request).select(),
            '1': ReporesClass1(self.request).select(),
            '2': ReporesClass2(self.request).select(),
            '3': ReporesClass3(self.request).select(),
            '4': ReporesClass4(self.request).select(),
            '5': ReporesClass5(self.request).select(),
            '6': ReporesClass6(self.request).select(),
        }
        if str(self.type) in distrdict:
            return distrdict[str(self.type)]
        else:
            return HttpResponse(json.dumps({"errmsg": "type参数错误", "errno": "400"}),content_type="application/json")


class ReporesClass0(APIAuthParameter):

    def select(self):

        #按年月日查询
        try:
            cursor.execute(
                "select id,date_format(create_time,'%Y-%m-%d'),count(id) from manager where name is not null and create_time BETWEEN '"+self.start+"' and '"+self.end+"' GROUP BY date_format(create_time,'%Y-%m-%d')"
                           )
            merchantname = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "index商家信息", "errno": "4001"}), content_type="application/json")
        dict = func.timedict(yearmonthday(int(self.start)), yearmonthday(int(self.end)))
        for key1, sqldate in enumerate(merchantname):
            for key, date in enumerate(dict['date']):
                if sqldate[1] == date:
                    dict['number'][key] = merchantname[key1][2]
                    break
        return HttpResponse(json.dumps({'data': dict, "errmsg": "成功", "errno": "0"}), content_type="application/json")

class ReporesClass1(object):

    def __init__(self, request):
        self.data = APIAuthParameter(request).reports()

    def select(self):
        #按月查询
        startmonth = monthtime(int(self.data['start']))
        endmonth = monthtime(int(self.data['end']))
        try:
            cursor.execute(
                "select id,date_format(create_time,'%Y-%m'),count(id) from manager where name is not null and create_time BETWEEN '"+startmonth+"' and '"+endmonth+"' GROUP BY date_format(create_time,'%Y-%m')")
            merchantname = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "index商家信息", "errno": "4001"}),content_type="application/json")
        dates = set()
        dt = datetime.datetime.strptime(startmonth, "%Y-%m")
        while startmonth <= endmonth:
            dates.add(startmonth)
            dt = dt + datetime.timedelta(2)
            startmonth = dt.strftime("%Y-%m")
        date_list = [0 for _ in range(len(dates))]
        result = []
        for i in sorted(dates):
            result.append(i)
        dict = {
            'month': result,
            'number': date_list,
        }
        for key1, sqldate in enumerate(merchantname):
            for key, date in enumerate(dict['month']):
                if sqldate[1] == date:
                    dict['number'][key] = merchantname[key1][2]
                    break
        return HttpResponse(json.dumps({'data': dict, "errmsg": "成功", "errno": "0"}), content_type="application/json")

class ReporesClass2(APIAuthParameter):
    def select(self):
        #按年份查询
        s_year = int(yeartime(int(self.start)))
        e_year = int(yeartime(int(self.end)))
        try:
            cursor.execute(
                "select id,date_format(create_time,'%Y'),count(id) from manager where name is not null and create_time BETWEEN '"+localutc(int(self.start))+"' and '"+localutc(int(self.end))+"' GROUP BY date_format(create_time,'%Y')"
            )
            merchantname = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "year商家信息", "errno": "4001"}), content_type="application/json")
        yearlist = []
        while (s_year < e_year ):
            yearlist.append(s_year)
            s_year += 1
        date_list = [0 for _ in range(len(yearlist))]
        result = []
        for i in yearlist:
            result.append(i)
        dict = {
            'year': result,
            'number': date_list,
        }
        for key, date in enumerate(yearlist):
            for key1, date1 in enumerate(merchantname):
                if date1[1] == str(date):
                    dict['number'][key] = merchantname[key1][2]
                    break
        return HttpResponse(json.dumps({'data': dict, "errmsg": "成功", "errno": "0"}), content_type="application/json")


class ReporesClass3(APIAuthParameter):
    def select(self):
        #foreign_key
        try:
            cursor.execute(
                "select name from manager where foreign_key = '"+self.foreign_key+"'")
            orgname = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "商家名字", "errno": "4001"}), content_type="application/json")
        # 返回所有商家地址和名字
        try:
            cursor.execute(
                "select id,name,initial_account from goods where foreign_key = '" + self.foreign_key + "' and name is not null")
            goodsaddr = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "商品id", "errno": "4001"}),content_type="application/json")
        if not goodsaddr:
            pass
        goodsidset = set(info[0][-2::] for info in goodsaddr)
        totalnum = set()
        for info in goodsidset:
            try:
                cursor.execute(
                    "SELECT toAddr from reviewrecord_" + info + " where goodsAddr in (select id from goods where foreign_key = '"+self.foreign_key+"' and name is not null) and type in ('1','2','3')"
                )
                result = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "领抢买卡券量", "errno": "4001"}),content_type="application/json")
            if result:
                for id in result:
                    totalnum.add(id[0])
        #抢券用户数
        cardtickets = set()
        for info in goodsaddr:
            try:
                cursor.execute(
                    "select userAddr from activity_user where goodsAddr = '" + info[0] + "'"
                )
                result = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "抢券用户数", "errno": "4001"}),content_type="application/json")
            if result:
                for id in result:
                    cardtickets.add(id[0])
         #单店铺领卡券用户总量
        usertotal = set()
        for info in goodsidset:
            try:
                cursor.execute(
                    "SELECT userAddress from userbalance_" + info + " where userAddress != '" + goodsaddr[0][2] + "'"
                )
                result = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "单店铺领卡券用户总量", "errno": "4001"}), content_type="application/json")
            if result:
                for id in result:
                    usertotal.add(id[0])
        addrelist = set()
        for info in goodsidset:
            try:
                cursor.execute(
                    "select toAddr from reviewrecord_"+info+" where type = '1' and goodsAddr in (select goodsAddr from goods where foreign_key = '" + self.foreign_key + "' and name is not null)"
                )
                result = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "商家持有卡券用户总量", "errno": "4001"}),content_type="application/json")
            if result:
                for id in result:
                    addrelist.add(id[0])
        total = 0
        for info in goodsaddr:
            try:
                cursor.execute(
                    "SELECT sum(amount) from userbalance_" + info[0][-2::] + " where goodsAddr = '" + info[0] + "' and userAddress != '" + goodsaddr[0][2] + "'"
                )
                result = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "卡券领取总量", "errno": "4001"}),content_type="application/json")
            if result[0][0] is not None:
                total += int(result[0][0])

        try:
            cursor.execute(
                "select sum(g.circulation) from goods as g,manager as m where m.foreign_key = '"+self.foreign_key+"' and g.foreign_key = m.foreign_key and g.is_represent = '0' and putaway = '0'")
            totalmerchandise = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "单商家所有卡券总量", "errno": "4001"}),content_type="application/json")
        zztotal = 0
        for info in goodsaddr:
            try:
                cursor.execute(
                    "select count(amount) from transfer_record where goodsAddr = '" + info[0] + "'"
                )
                result = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "全部商品总转增次数", "errno": "4001"}),content_type="application/json")
            if result[0][0] is not None:
                zztotal += int(result[0][0])

        dict = {
            'num': len(addrelist), #商家持有卡券用户总量
            'orgname': orgname[0][0],#商家名称
            'totalmerchandise':to_string(totalmerchandise[0][0]),# 单商家所有卡券总量
            'total':total,# 卡券领取总量
            'zztotal':zztotal,#全部商品总转增次数
            'usertotal':len(usertotal),#单店铺领卡券用户总量
            'cardtickets':len(cardtickets),#抢券用户数
            'totalnum':len(totalnum),#领抢买卡券量
                }
        data = {'data': dict, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")


class ReporesClass4(APIAuthParameter):
    def select(self):
        # 商品id
        try:
            cursor.execute(
                "select name,initial_account from goods where id = '" + self.goodsid + "'")
            name = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "商品名称", "errno": "4001"}), content_type="application/json")
        #单商品卡券剩余量
        try:
            cursor.execute(
                "SELECT sum(amount) from userbalance_"+self.goodsid[-2::]+" where goodsAddr = '"+self.goodsid+"' and userAddress = '"+name[0][1]+"'"
            )
            cardvouchers = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "单商品卡券剩余量", "errno": "4001"}),content_type="application/json")
        #商铺单商品提货总用户数
        try:
            cursor.execute(
                "select count(DISTINCT user_addr) from take_order as o,take_order_goods as g where g.goods_id = '"+self.goodsid+"' and o.order_state = '0' and g.order_number = o.order_number "
            )
            whotake = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "商铺单商品提货总用户数", "errno": "4001"}),content_type="application/json")
        #单商品转赠次数
        try:
            cursor.execute(
                "select count(amount) from transfer_record where goodsAddr = '"+self.goodsid+"'"
            )
            transfers = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "单商品转赠次数", "errno": "4001"}),content_type="application/json")
        #单商品卡券领取总量
        try:
            cursor.execute(
                "SELECT sum(amount) from userbalance_" + self.goodsid[-2::] + " where goodsAddr = '" + self.goodsid + "' and userAddress != '"+name[0][1]+"'"
            )
            cardcollection = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "单商品卡券领取总量", "errno": "4001"}),content_type="application/json")
        #单商品卡券发行总量
        try:
            cursor.execute(
                "select sum(circulation) from goods where id = '" + self.goodsid + "' and is_delete = '0' and is_represent = '0' and putaway = '0'"
            )
            cardissue = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "单商品卡券发行总量", "errno": "4001"}),content_type="application/json")
        dict = {
            'name':name[0][0],#商品名字
            'cardvouchers':to_string(cardvouchers[0][0]),#单商品卡券剩余量
            'whotake':whotake[0][0],#商铺单商品提货总用户数
            'transfers':transfers[0][0],#单商品转赠次数
            'cardcollection':to_string(cardcollection[0][0]),#单商品卡券领取总量
            'cardissue':to_string(cardissue[0][0]),#单商品卡券发行总量
        }
        data = {'data': dict, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")


class ReporesClass5(APIAuthParameter):
    def select(self):

        # manager_id
        try:
            cursor.execute(
                "select count(DISTINCT user_addr),(select name from manager where id = '"+self.manager_id+"') from take_order where manager_id = '"+self.manager_id+"' and order_state = '0'"
            )
            takeuser = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "商铺申请提货总用户数", "errno": "4001"}),content_type="application/json")
        #买券用户数
        try:
            cursor.execute(
                "select count(DISTINCT user_addr) from purchase_order where manager_id = '"+self.manager_id+"'and order_state = '1' and pay_state = '1'"
            )
            buyuser = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "买券用户数", "errno": "4001"}), content_type="application/json")
        dict = {
            'orgname': takeuser[0][1],#商家名字
            'num': takeuser[0][0],#商铺申请提货总用户数
            'buyuser':buyuser[0][0],#买券用户数
        }
        data = {'data': dict, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")


class ReporesClass6(APIAuthParameter):
    def select(self):
        # 用户id
        try:
            cursor.execute(
                "select sum(g.goods_amount),(select name from jld_user where id = '"+self.useraddr+"') from take_order as o,take_order_goods as g where o.user_addr = '"+self.useraddr+"' and o.order_state = '0' and o.order_number = g.order_number"
            )
            userdata = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "用户申请提货量", "errno": "4001"}), content_type="application/json")
        data = {'num': to_string(userdata[0][0]), 'username': userdata[0][1]}
        data = {'data': data, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")
