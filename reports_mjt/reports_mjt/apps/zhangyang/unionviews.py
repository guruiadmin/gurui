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
from django.views import View
import json
import time
import datetime

from django_redis import get_redis_connection

from public.models import Endorsementuser, UserData
from reports_mjt.utils.apiauth import APIAuthParameter
from reports_mjt.utils.data_select import commission_price, time_stamp, str_time_stamp_date
from reports_mjt.utils.decime import to_string


#小程序
class SmallProgram(View):
    def get(self, request):
        global null
        null = ''
        global false
        false = False
        global true
        true = True
        self.data = request.GET.get('param')
        try:
            eval(get_redis_connection('default').get(eval(self.data)['token']))
        except:
            return HttpResponse(json.dumps({"errmsg": "token已过期", "errno": "401"}), content_type="application/json")
        
        return DistributionClass(request).distribution()


class DistributionClass(APIAuthParameter):

    def distribution(self):
        distrdict = {
            '1': RealtimeData(self.request).funcdata(),
            '2': Commission3(self.request).funcdata(),  # 入账佣金
            '3': Commission2(self.request).funcdata(),  # 带解冻佣金
            '4': Commission4(self.request).funcdata(),  # 退款佣金
            '5': Cash_Withdrawal(self.request).funcdata(),  # 提现
        }

        if str(self.zytype) in distrdict:
            return distrdict[str(self.zytype)]
        else:
            return HttpResponse(json.dumps({"errmsg": "type参数错误", "errno": "400"}), content_type="application/json")


class Cash_Withdrawal(object):

    def __init__(self, request):
        self.data = APIAuthParameter(request).getRedis()

    def funcdata(self):
        cursor = connections['default'].cursor()
        timedate = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        time_stamp = int(time.time())
        # 可提现
        resultwithdrawal = 0
        try:
            cursor.execute(
                "SELECT sum(price) FROM (SELECT COALESCE (sum(commission),0) as price FROM goods_presell_order WHERE sharer_id = '"+self.data['userid']+"' AND sale = '3' UNION all SELECT (COALESCE (sum(g.commission * g.goods_amount),0) - (SELECT COALESCE(sum(amount), 0)FROM withdrawals_record WHERE user_id = '"+self.data['userid']+"' AND state IN ('1', '0'))) FROM purchase_order_goods AS g, purchase_order AS o WHERE g.affiliateID = '"+self.data['userid'] +"' AND o.pay_state = '1' AND o.pay_time IS NOT NULL and o.pay_time < '"+commission_price(time_stamp)+"' AND o.order_number = g.order_number) a"

            )
            withdrawal = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "可提现4", "errno": "400"}), content_type="application/json")
        if withdrawal and withdrawal[0][0] > 0:
            resultwithdrawal = withdrawal[0][0]
            try:
                sumcommin = Endorsementuser.objects.filter(id=self.data['userid'])
            except Endorsementuser.DoesNotExist:
                return HttpResponse(status=404)
            # 如果已有信息
            if sumcommin:
                userinfo = Endorsementuser.objects.get(id=self.data['userid'])
                userinfo.cash_withdrawal = withdrawal[0][0]
                userinfo.save()
            #如果没有
            else:
                userinfo = UserData.objects.get(id=self.data['userid'])
                enduser = Endorsementuser()
                enduser.id = userinfo.id
                enduser.unionid = userinfo.unionid
                enduser.phone = userinfo.phone
                enduser.name = userinfo.name
                enduser.wx_nick_name = userinfo.wx_nick_name
                enduser.sex = userinfo.sex
                enduser.cash_withdrawal = withdrawal[0][0]
                enduser.create_time = timedate
                enduser.save()
        else:
            try:
                sumcommin = Endorsementuser.objects.filter(id=self.data['userid'])
            except Endorsementuser.DoesNotExist:
                return HttpResponse(status=404)
                # 如果已有信息
            if sumcommin:
                userinfo = Endorsementuser.objects.get(id=self.data['userid'])
                userinfo.cash_withdrawal = 0
                userinfo.save()
                    # 如果没有
            else:
                userinfo = UserData.objects.get(id=self.data['userid'])
                enduser = Endorsementuser()
                enduser.id = userinfo.id
                enduser.unionid = userinfo.unionid
                enduser.phone = userinfo.phone
                enduser.name = userinfo.name
                enduser.wx_nick_name = userinfo.wx_nick_name
                enduser.sex = userinfo.sex
                enduser.create_time = timedate
                enduser.save()

        # 冻结
        resulthaw = 0
        try:
            cursor.execute(
                "SELECT sum(price) FROM (SELECT COALESCE (sum(commission),0) as price FROM goods_presell_order WHERE sharer_id = '" + self.data['userid'] + "' AND sale = '1' UNION all select COALESCE(sum(g.commission * g.goods_amount ), 0) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '"+self.data['userid']+"' and o.pay_state = '1' and o.pay_time is not null and o.pay_time > '"+commission_price(time_stamp)+"' and o.order_number = g.order_number) a"

            )
            thaw = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "冻结", "errno": "400"}), content_type="application/json")
        if thaw and thaw[0][0] > 0:
            resulthaw = thaw[0][0]
            try:
                sumcommin = Endorsementuser.objects.filter(id=self.data['userid'])
            except Endorsementuser.DoesNotExist:
                return HttpResponse(status=404)
            # 如果已有信息
            if sumcommin:
                userinfo = Endorsementuser.objects.get(id=self.data['userid'])
                userinfo.frozen = thaw[0][0]
                userinfo.save()

            # 如果没有
            else:
                userinfo = UserData.objects.get(id=self.data['userid'])
                enduser = Endorsementuser()
                enduser.id = userinfo.id
                enduser.unionid = userinfo.unionid
                enduser.phone = userinfo.phone
                enduser.name = userinfo.name
                enduser.wx_nick_name = userinfo.wx_nick_name
                enduser.sex = userinfo.sex
                enduser.frozen = thaw[0][0]
                enduser.create_time = timedate
                enduser.save()
        else:
            try:
                sumcommin = Endorsementuser.objects.filter(id=self.data['userid'])
            except Endorsementuser.DoesNotExist:
                return HttpResponse(status=404)
                # 如果已有信息
            if sumcommin:
                userinfo = Endorsementuser.objects.get(id=self.data['userid'])
                userinfo.frozen = 0
                userinfo.save()
                # 如果没有
            else:
                userinfo = UserData.objects.get(id=self.data['userid'])
                enduser = Endorsementuser()
                enduser.id = userinfo.id
                enduser.unionid = userinfo.unionid
                enduser.phone = userinfo.phone
                enduser.name = userinfo.name
                enduser.wx_nick_name = userinfo.wx_nick_name
                enduser.sex = userinfo.sex
                enduser.frozen = 0
                enduser.create_time = timedate
                enduser.save()


        return HttpResponse(json.dumps({'data': {'thaw': to_string(resulthaw), 'withdrawal': to_string(resultwithdrawal)}, "errmsg": "成功", "errno": "200"}), content_type="application/json")


class RealtimeData(object):

    def __init__(self, request):
        self.data = APIAuthParameter(request).getRedis()

    def funcdata(self):
        cursor = connections['default'].cursor()
        time_stamp_index = int(time.time())

        #今日购买订单量
        cursor.execute(
                "SELECT sum(price) FROM (SELECT count(order_number) as price FROM goods_presell_order WHERE sharer_id = '" + self.data['userid'] + "' and create_time between '" + time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' AND sale in ('1','3')  UNION all select count(g.order_number) from purchase_order as o, purchase_order_goods as g where g.affiliateID = '" + self.data['userid'] + "' and o.pay_state = '1' and o.pay_time is not null and o.pay_time between '" + time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' and o.order_number = g.order_number) a"

            )
        todaybuyorder = cursor.fetchall()

        # 带解冻金额
        try:
            cursor.execute(
                "SELECT sum(price) FROM (SELECT COALESCE (sum(commission),0) as price FROM goods_presell_order WHERE sharer_id = '" + self.data['userid'] + "' AND sale = '1' UNION all select COALESCE(sum(g.commission * g.goods_amount ), 0) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" + self.data['userid'] + "' and o.pay_state = '1' and o.pay_time is not null and o.pay_time > '" + commission_price(time_stamp_index) + "' and o.order_number = g.order_number) a"
            )
            daijiedong = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "今日购买订单量", "errno": "400"}), content_type="application/json")

        # 累计总收入
        try:
            cursor.execute(
                "SELECT sum(price) FROM (SELECT COALESCE (sum(commission),0) as price FROM goods_presell_order WHERE sharer_id = '" + self.data['userid'] + "' AND sale in ('1','3') UNION all select COALESCE(sum(g.commission * g.goods_amount), 0) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" + self.data['userid'] + "' and o.pay_state = '1'  and o.pay_time is not null and o.order_number = g.order_number) a"
            )
            numpayments = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "累计总收入1", "errno": "400"}), content_type="application/json")

        #今日佣金收入
        todaycommission = 0
        # 代言人的所有券地址
        try:
            cursor.execute(
                "SELECT sum(price) FROM (SELECT COALESCE (sum(commission),0) as price FROM goods_presell_order WHERE sharer_id = '" + self.data['userid'] + "' and create_time between '" +time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' AND sale in ('1','3')  UNION all select COALESCE(sum(g.commission * g.goods_amount), 0) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" + self.data['userid'] + "' and o.pay_state = '1'  and o.pay_time is not null and o.pay_time between '" +time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' and o.order_number = g.order_number) a"
            )
            conponid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "今日佣金收入", "errno": "400"}), content_type="application/json")
        if conponid:
            todaycommission = conponid[0][0]

        # 最近一笔收入
        lastincome = -1
        lastdate = '1559530800'
        # 代言人的所有券地址
        try:
            cursor.execute(
                "select COALESCE(commission, 0) ,unix_timestamp(create_time),create_time as create_time from goods_presell_order where sharer_id = '"+self.data['userid']+"' and create_time between '" +time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' and sale in ('1','3')  UNION select COALESCE(g.commission * g.goods_amount, 0) ,unix_timestamp(o.pay_time), o.pay_time as create_time from purchase_order as o, purchase_order_goods as g where g.affiliateID = '" + self.data['userid'] + "' and o.pay_state = '1' and o.pay_time is not null and o.pay_time between '" +time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' and o.order_number = g.order_number ORDER BY create_time desc LIMIT 1"

            )
            conponid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "最近一笔收入", "errno": "400"}), content_type="application/json")
        if conponid and conponid[0][1] is not None:
            lastdate = conponid[0][1]
            lastincome = conponid[0][0]


        # 今日退佣
        retreatincome = 0
        # 代言人的所有券地址
        try:
            cursor.execute(
                "SELECT sum(price) FROM (SELECT COALESCE (sum(commission),0) as price FROM goods_presell_order WHERE sharer_id = '" + self.data['userid'] + "' and refund_time between '" + time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' AND sale ='2'  UNION all select COALESCE(sum(g.commission * g.goods_amount), 0) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" + self.data['userid']+ "' and o.pay_state = '2'  and o.pay_time is not null and  o.pay_time between '" + time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' and o.order_number = g.order_number) a"

            )
            conponid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "今日退佣", "errno": "400"}), content_type="application/json")
        if conponid:
            retreatincome = conponid[0][0]

        # 今日退订单
        try:
            cursor.execute(
                "SELECT sum(price) FROM (SELECT count(order_number) as price FROM goods_presell_order WHERE sharer_id = '" + self.data['userid'] + "' and refund_time between '" + time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' AND sale ='2'  UNION all select count(g.order_number) from purchase_order as o, purchase_order_goods as g where g.affiliateID = '" + self.data['userid'] + "' and o.pay_state = '2' and o.pay_time is not null and o.pay_time between '" +time_stamp()['today'][0] + "' and '" + time_stamp()['today'][1] + "' and o.order_number = g.order_number) a"

            )
            retreatorder = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "今日退订单", "errno": "400"}),  content_type="application/json")
        dict = {
            'todaybuyorder': to_string(todaybuyorder[0][0]),  # 今日订单量
            'todaycommission': to_string(todaycommission),  # 今日预计收入
            'lastincome': to_string(lastincome),#最近一笔收入
            'lastdate': int(round(int(lastdate) * 1000)),#最后收入时间
            'retreatincome': to_string(retreatincome),#今日退佣
            'retreatorder': to_string(retreatorder[0][0]),#今日退订单
            'numpayments': to_string(numpayments[0][0]), #累计总收入
            'jiedong': to_string(daijiedong[0][0]) #待解冻
        }
        return HttpResponse(json.dumps({'data': dict, "errmsg": "成功", "errno": "200"}), content_type="application/json")


class Commission2(object):

    def __init__(self, request):
        self.data = APIAuthParameter(request).getRedis()

    def funcdata(self):
        cursor = connections['default'].cursor()
        time_stamp = int(time.time())
        #带解冻佣金
        try:
            cursor.execute(
     "select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)),@@SESSION .time_zone,'+08:00'),'%Y-%m-%d'),sum(price),sum(number) from (select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d') as create_time,COALESCE(sum(commission), 0) as price ,count(order_number) as number from goods_presell_order where sharer_id = '"+self.data['userid']+"' and sale = '1' GROUP BY DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d') UNION select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')as create_time,COALESCE(sum(g.commission * g.goods_amount ), 0),count(g.order_number) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '"+self.data['userid']+"' and o.pay_state = '1' and o.pay_time is not null and o.pay_time > '"+commission_price(time_stamp)+"' and o.order_number = g.order_number GROUP BY DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')) a GROUP BY create_time ORDER BY create_time desc"

            )
            data = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "带解冻佣金1", "errno": "400"}), content_type="application/json")
        dateresult = []
        if data:
            for info in data:
                dateresult.append({
                    'date': info[0],  # 日期
                    'totalprice': float(to_string(info[1])),  # 共计佣金
                    'totalnum': float(info[2]),  # 共计订单数
                    'data': [],
                    'datetime': round(int(str_time_stamp_date(info[0])) * 1000),  # 时间戳日期

                })
            try:
                cursor.execute(
                    "select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d') ,unix_timestamp(create_time) as create_time,goods_amount,COALESCE((commission ), 0), (select name from goods where id = goods_id),(select main_photo from goods where id = goods_id) from goods_presell_order where sharer_id = '"+self.data['userid']+"' and sale = '1' GROUP BY order_number UNION select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')as create_time,unix_timestamp(o.pay_time),g.goods_amount,COALESCE((g.commission * g.goods_amount ), 0), (select name from goods where id = g.goods_id),(select main_photo from goods where id = g.goods_id) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '"+self.data['userid']+"' and o.pay_state = '1' and o.pay_time is not null and o.pay_time > '"+commission_price(time_stamp)+"' and o.order_number = g.order_number GROUP BY g.order_number ORDER BY create_time desc"

                )
                withthawing = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "带解冻佣金2", "errno": "400"}), content_type="application/json")
            result = []
            if withthawing:
                for info in withthawing:
                    result.append({
                        'date': info[0],  # 日期
                        'time': round(int(info[1]) * 1000),  # 时间
                        'latestime': round(int(info[1] + 604800) * 1000),  # 到期时间
                        'num': float(info[2]),  # 件数
                        'commission': float(to_string(info[3])),  # 佣金
                        'name': info[4],  # 名字
                        'photo': info[5],  # 图片
                    })
            for date in dateresult:
                for timeinfo in result:
                    if date['date'] == timeinfo['date']:
                        date['data'].append(timeinfo)
            if self.data['token_active_data']:
                for date in result:
                    if date['name'] == eval(self.data['token_active_data'])['goodsName']:
                        date['latestime'] = int(eval(self.data['token_active_data'])['endTime'])
            return HttpResponse(json.dumps({'data': {"list": dateresult[(int(self.data['pageno']) - 1) * int(self.data['pagesize']):int(self.data['pageno']) * int(self.data['pagesize'])]}, "errmsg": "成功", "errno": "200"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'data': dateresult, "errmsg": "成功", "errno": "200"}),  content_type="application/json")


class Commission3(object):


    def __init__(self, request):
        self.data = APIAuthParameter(request).getRedis()

    def funcdata(self):
        cursor = connections['default'].cursor()
        time_stamp = int(time.time())
        # 入账佣金
        try:
            cursor.execute(
                "select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)),@@SESSION .time_zone,'+08:00'),'%Y-%m-%d'),sum(price),sum(number) from (select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d') as create_time,COALESCE(sum(commission), 0) as price ,count(order_number) as number from goods_presell_order where sharer_id = '" +self.data[ 'userid'] + "' and sale = '3' GROUP BY DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d') UNION select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')as create_time,COALESCE(sum(g.commission * g.goods_amount ), 0),count(g.order_number) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" +self.data['userid'] + "' and o.pay_state = '1' and o.pay_time is not null and o.pay_time < '" + commission_price(time_stamp) + "' and o.order_number = g.order_number GROUP BY DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')) a GROUP BY create_time ORDER BY create_time desc"
            )
            data = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "入账佣金", "errno": "400"}), content_type="application/json")
        dateresult = []
        if data:
            for info in data:
                dateresult.append({
                    'date': info[0],  # 日期
                    'totalprice': float(info[1]),  # 共计佣金
                    'totalnum': float(info[2]),  # 共计订单数
                    'data': [],
                    'datetime': round(int(str_time_stamp_date(info[0])) * 1000),  # 时间戳日期
                })
            try:
                cursor.execute(
                    "select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d'),unix_timestamp(create_time) as create_time,goods_amount,COALESCE((commission ), 0), (select name from goods where id = goods_id),(select main_photo from goods where id = goods_id) from goods_presell_order where sharer_id = '" + self.data['userid'] + "' and sale = '3' GROUP BY order_number UNION select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')as create_time,unix_timestamp(o.pay_time),g.goods_amount,COALESCE((g.commission * g.goods_amount ), 0), (select name from goods where id = g.goods_id),(select main_photo from goods where id = g.goods_id) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" + self.data['userid'] + "' and o.pay_state = '1' and o.pay_time is not null and o.pay_time < '" + commission_price(time_stamp) + "' and o.order_number = g.order_number GROUP BY g.order_number ORDER BY create_time desc"
                )
                withthawing = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "入账佣金", "errno": "400"}), content_type="application/json")
            result = []
            if withthawing:
                for info in withthawing:
                    result.append({
                        'date': info[0],  # 日期
                        'time': round(int(info[1]) * 1000),  # 时间
                        'latestime': round(int(info[1] + 604800) * 1000),  # 到期时间
                        'num': float(info[2]),  # 件数
                        'commission': float(info[3]),  # 佣金
                        'name': info[4],  # 名字
                        'photo': info[5],  # 图片
                    })
            for date in dateresult:
                for timeinfo in result:
                    if date['date'] == timeinfo['date']:
                        date['data'].append(timeinfo)
            if self.data['token_active_data']:
                for date in result:
                    if date['name'] == eval(self.data['token_active_data'])['goodsName']:
                        date['latestime'] = int(eval(self.data['token_active_data'])['endTime'])
            return HttpResponse(json.dumps({'data': {"list": dateresult[(int(self.data['pageno']) - 1) * int(self.data['pagesize']):int(self.data['pageno']) * int(self.data['pagesize'])]}, "errmsg": "成功", "errno": "200"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'data': dateresult, "errmsg": "成功", "errno": "200"}),   content_type="application/json")


class Commission4(object):


    def __init__(self, request):
        self.data = APIAuthParameter(request).getRedis()

    def funcdata(self):
        cursor = connections['default'].cursor()
        # 退款佣金
        try:
            cursor.execute(
                "select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)),@@SESSION .time_zone,'+08:00'),'%Y-%m-%d'),sum(price),sum(number) from (select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d') as create_time,COALESCE(sum(commission), 0) as price ,count(order_number) as number from goods_presell_order where sharer_id = '" + self.data['userid'] + "' and sale = '2' GROUP BY DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(create_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d') UNION select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')as create_time,COALESCE(sum(g.commission * g.goods_amount ), 0),count(g.order_number) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" + self.data[ 'userid'] + "' and o.pay_state = '2' and o.pay_time is not null and o.order_number = g.order_number GROUP BY DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')) a GROUP BY create_time ORDER BY create_time desc"

            )
            data = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "退款佣金1", "errno": "400"}), content_type="application/json")
        dateresult = []
        if data:
            for info in data:
                dateresult.append({
                    'date': info[0],  # 日期
                    'totalprice': float(info[1]),  # 共计佣金
                    'totalnum': float(info[2]),  # 共计订单数
                    'data': [],
                    'datetime': round(int(str_time_stamp_date(info[0])) * 1000),  # 时间戳日期
                })
            try:
                cursor.execute(
                    "select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(refund_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d'),unix_timestamp(create_time),goods_amount,COALESCE((commission ), 0), (select name from goods where id = goods_id),(select main_photo from goods where id = goods_id),unix_timestamp(refund_time) as refund_time from goods_presell_order where sharer_id = '"+self.data['userid']+"' and sale = '2' GROUP BY order_number UNION  select DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(unix_timestamp(o.pay_time)), @@session.time_zone,'+08:00'),'%Y-%m-%d')as create_time,unix_timestamp(o.pay_time),g.goods_amount,COALESCE((g.commission * g.goods_amount ), 0), (select name from goods where id = g.goods_id),(select main_photo from goods where id = g.goods_id),unix_timestamp(a.createdAt) from purchase_order_goods as g, purchase_order as o, apply_sale as a where g.affiliateID = '"+self.data['userid']+"' and o.pay_state = '2' and o.order_number = g.order_number and a.outTradeNo = o.order_number GROUP BY g.order_number ORDER BY refund_time desc"

                )
                withthawing = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "退款佣金2", "errno": "400"}),   content_type="application/json")
            result = []
            if withthawing:
                for info in withthawing:
                    result.append({
                        'date': info[0],  # 日期
                        'time': round(int(info[1]) * 1000),  # 时间
                        'latestime': round(int(info[6]) * 1000),  # 退款佣金时间
                        'num': float(info[2]),  # 件数
                        'commission': float(info[3]),  # 佣金
                        'name': info[4],  # 名字
                        'photo': info[5],  # 图片
                    })
            for date in dateresult:
                for timeinfo in result:
                    if date['date'] == timeinfo['date']:
                        date['data'].append(timeinfo)
            return HttpResponse(json.dumps({'data': {"list": dateresult[(int(self.data['pageno']) - 1) * int(self.data['pagesize']):int(self.data['pageno']) * int(self.data['pagesize'])]}, "errmsg": "成功", "errno": "200"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'data': dateresult, "errmsg": "成功", "errno": "200"}), content_type="application/json")


