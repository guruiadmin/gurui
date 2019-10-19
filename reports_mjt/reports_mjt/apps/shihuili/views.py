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
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection

from reports_mjt.utils.data_select import datedict, FunctionObject, localutc
from reports_mjt.utils.decime import to_string
func = FunctionObject()
#系统首页
class SystemHomePage(View):
    def get(self, request):
        global true
        true = True
        global null
        null = ''
        global false
        false = False
        type = request.GET.get('type')
        token = request.GET.get('token')
        start_day = request.GET.get('start')
        end_day = request.GET.get('end')
        year = request.GET.get('year')
        month = request.GET.get('month')
        page = request.GET.get('page')
        num = request.GET.get('numberbars')
        redis_conn = get_redis_connection('default')
        try:
            tokendata = eval(redis_conn.get(token))
        # tokendata = eval(get_redis_connection('default').get(request.GET.get('token')))
        except:
            return HttpResponse(json.dumps({"errmsg": "token已过期", "errno": "4001"}), content_type="application/json")
        foreign_key = tokendata['foreignKey']
        manager_id = tokendata['managerId']

        if not start_day and not end_day:
            pass
        elif start_day in ['month', 'week', 'total', 'yesday', 'months']:
            datestart = datedict[start_day][0]
            dateend = datedict[start_day][1]
        else:
            datestart = localutc(int(start_day))
            dateend = localutc(int(end_day))
        cursor = connections['default'].cursor()
        if not all([type, token]):
            return HttpResponse(json.dumps({"errmsg": "type token参数未传", "errno": "4001"}), content_type="application/json")
        elif type == '0':
            #今日订单总量今日销售总额
            try:
                cursor.execute(
                    "select count(order_number),COALESCE(SUM(order_price),0) from purchase_order where manager_id = '"+str(manager_id)+"' and order_state='1' and create_time BETWEEN '"+datedict['today'][0]+"' and '"+datedict['today'][1]+"' and pay_state ='1'")
                ordervolumesalestoday = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "今日订单总量今日销售总额", "errno": "4001"}), content_type="application/json")
            # 昨日销售总额
            try:
                cursor.execute(
                    "select COALESCE(SUM(order_price),0) from purchase_order where manager_id = '"+str(manager_id)+"' and order_state='1' and create_time BETWEEN '" + datedict['yesday'][0] + "' and '" + datedict['yesday'][1] + "' and pay_state ='1'"
                )
                totalsalesyesdate = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "昨日销售总额", "errno": "4001"}),content_type="application/json")
            # 七日销售总额
            try:
                cursor.execute(
                    "select COALESCE(SUM(order_price),0) from purchase_order where manager_id = '"+str(manager_id)+"' and order_state='1' and create_time BETWEEN '" + datedict['week'][0] + "' and '" + datedict['today'][1] + "' and pay_state ='1'"
                )
                totalsalesweek= cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "七日销售总额", "errno": "4001"}),content_type="application/json")
            # 商品总览
            #已下架商品
            try:
                cursor.execute(
                    "select count(id) from goods where foreign_key = '"+foreign_key+"' and putaway = '1' and name is not null"
                )
                offshelfmerchandise = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "已下架商品", "errno": "4001"}),content_type="application/json")

            # 已上架商品
            try:
                cursor.execute(
                    "select count(id) from goods where foreign_key = '"+foreign_key+"' and putaway = '0' and name is not null"
                )
                goodsonshelves = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "已下架商品", "errno": "4001"}),content_type="application/json")

            # 全部商品
            try:
                cursor.execute(
                    "select count(id) from goods where foreign_key = '"+foreign_key+"' and name is not null"
                )
                tightstock = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "全部商品", "errno": "4001"}), content_type="application/json")

            # 用户今日新增
            try:
                cursor.execute(
                    "select count(DISTINCT user_addr) from purchase_order where manager_id = '"+str(manager_id)+"' and order_state = '1' and pay_state = '1' and user_addr in (select jld_user.id from jld_user where create_time BETWEEN '" + datedict['today'][0] + "' and '" + datedict['today'][1] + "')")
                useraddtoday = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "用户今日新增", "errno": "4001"}), content_type="application/json")

            # 用户昨日新增
            try:
                cursor.execute(
                    "select count(DISTINCT user_addr) from purchase_order where manager_id = '"+str(manager_id)+"' and order_state = '1' and pay_state = '1' and user_addr in (select jld_user.id from jld_user where create_time BETWEEN '" + datedict['yesday'][0] + "' and '" + datedict['yesday'][1] + "')"
                )
                useraddyesday = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "用户昨日新增", "errno": "4001"}), content_type="application/json")
            # 用户本月新增
            try:
                cursor.execute(
                    "select count(DISTINCT user_addr) from purchase_order where manager_id = '"+str(manager_id)+"' and order_state = '1' and pay_state = '1' and user_addr in (select jld_user.id from jld_user where create_time BETWEEN '" + datedict['day_begin'][0] + " 00:00:00' and '" + datedict['day_end'][0] + " 23:59:59')"
                )
                useraddmonth = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "用户昨日新增", "errno": "4001"}), content_type="application/json")
            membershipnum = set()
            # 会员总数
            try:
                cursor.execute(
                    "select id from goods where foreign_key = '"+foreign_key+"' and name is not null"
                )
                goodsid = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "goodsid", "errno": "4001"}), content_type="application/json")
            for id in goodsid:
                # 会员总数
                try:
                    cursor.execute(
                        "select userAddr from relation where goodsAddr = '" + id[0] + "'"
                    )
                    usercount = cursor.fetchall()
                except:
                    return HttpResponse(json.dumps({"errmsg": "会员总数", "errno": "4001"}), content_type="application/json")
                if not usercount:
                    pass
                for data in usercount:
                    membershipnum.add(data[0])
            dict = {
                'membershipnum': len(membershipnum),#会员总数
                'useraddmonth': useraddmonth[0][0],#用户本月新增
                'useraddyesday': useraddyesday[0][0],#用户昨日新增
                'useraddtoday': useraddtoday[0][0],#用户今日新增
                'tightstock': tightstock[0][0],#全部商品
                'goodsonshelves': goodsonshelves[0][0],#已上架商品
                'offshelfmerchandise': offshelfmerchandise[0][0],#已下架商品
                'totalsalesyesdate': to_string(totalsalesyesdate[0][0]),#昨日销售总额
                'totalsalesweek': to_string(totalsalesweek[0][0]),#七日销售总额
                'ordervolumetoday': ordervolumesalestoday[0][0],#今日订单总量
                'salestoday': to_string(ordervolumesalestoday[0][1]),#今日销售总额
            }
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")

        #待处理事物
        elif type == '1':
            # 待付款订单
            try:
                cursor.execute(
                    "select count(order_number) from purchase_order where manager_id = '"+manager_id+"' and order_state='1' and pay_state = '0'"
                )
                ordertobepaid = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "待付款订单", "errno": "4001"}), content_type="application/json")
            # 待发货订单
            try:
                cursor.execute(
                    "select count(order_number) from take_order where manager_id = '"+manager_id+"' and take_state in ('0','1')")
                standbyorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "待发货订单", "errno": "4001"}), content_type="application/json")
            # 已发货订单
            try:
                cursor.execute(
                    "select count(order_number) from take_order where manager_id = '" + manager_id + "' and take_state in ('2','3')"
                )
                outgoingorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "已发货订单", "errno": "4001"}), content_type="application/json")

            # 已完成订单
            try:
                cursor.execute(
                    "select count(purchase_number) from take_order where manager_id = '"+manager_id+"' and take_state = '3'"
                )
                completedorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "已完成订单", "errno": "4001"}), content_type="application/json")

            # 本周提货订单量
            try:
                cursor.execute(
                    "select count(order_number) from take_order where manager_id = '"+manager_id+"' and create_date bETWEEN '" + datedict['week'][0] + " ' and '" + datedict['today'][1] + "' "
                )
                weekordertake = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "本周提货订单量", "errno": "4001"}), content_type="application/json")
            # 本月提货量
            try:
                cursor.execute(
                    "select count(order_number) from take_order where manager_id = '"+manager_id+"' and create_date bETWEEN '" + datedict['month'][0] + "' and '" + datedict['today'][1] + "'"
                )
                monthordertake = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "本月提货量", "errno": "4001"}), content_type="application/json")

            # 本周购买量
            try:
                cursor.execute(
                    "select COALESCE(sum(actual_price),0) from purchase_order where manager_id = '"+manager_id+"' and order_state='1' and create_time bETWEEN '" + datedict['week'][0] + "' and '" + datedict['today'][1] + "' and pay_state ='1'")
                weekorderbuy = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "本月购买量", "errno": "4001"}), content_type="application/json")

            # 本月购买量
            try:
                cursor.execute(
                    "select COALESCE(sum(actual_price),0) from purchase_order where manager_id = '"+manager_id+"' and order_state='1' and create_time bETWEEN '" + datedict['day_begin'][0] + " 00:00:00' and '" + datedict['day_end'][0] + " 23:59:59' and pay_state ='1'"
                )
                monthorderbuy = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "本月购买量", "errno": "4001"}), content_type="application/json")
            # 处理退货
            try:
                cursor.execute(
                    "select count(outTradeNo) from apply_sale where orgAddr = '"+manager_id+"' and type = '1' and state in ('0','1')"
                )
                returngoods = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "处理退货", "errno": "4001"}), content_type="application/json")
            # 处理退款
            try:
                cursor.execute(
                    "select count(outTradeNo) from apply_sale where orgAddr = '"+manager_id+"' and type = '2' and state in ('0','1')"
                )
                returnmony = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "处理退款", "errno": "4001"}), content_type="application/json")
            dict = {
                'ordertobepaid': ordertobepaid[0][0],  # 待付款订单
                'standbyorder': standbyorder[0][0],  # 待发货订单
                'outgoingorder': outgoingorder[0][0],  # 已发货订单
                'completedorder': completedorder[0][0],  # 已完成订单
                'weekordertake': weekordertake[0][0],  # 本周提货订单量
                'monthordertake': monthordertake[0][0],  # 本月提货量
                'weekorderbuy': to_string(weekorderbuy[0][0]),  # 本周购买总额
                'monthorderbuy': to_string(monthorderbuy[0][0]),  # 本月购买总额
                'returngoods': to_string(returngoods[0][0]),  # 处理退货
                'returnmony': to_string(returnmony[0][0]),  # 处理退款
            }
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")

        # 综合统计本周，本月，选择时间 提货
        elif type == '2':
            if not all([start_day, end_day]):
                return HttpResponse(json.dumps({"errmsg": "时间未传", "errno": "4001"}), content_type="application/json")
            # 选择提货量
            try:
                cursor.execute(
                    "select count(order_number),date_format(create_date,'%Y-%m-%d') from take_order where manager_id = '"+manager_id+"' and order_state = '0' and create_date bETWEEN '"+datestart+"' and '"+dateend+"' GROUP BY date_format(create_date,'%Y-%m-%d')"
                )
                selecttakenum = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "本月提货量", "errno": "4001"}), content_type="application/json")
            import pandas as pd
            date = pd.date_range(datestart, dateend, freq='D')
            week = [int(i.strftime("%w")) for i in date]  # 0表示星期日
            dataframe = pd.DataFrame({'date': date, 'week': week, 'num': 0.00})
            for key1, sqldate in enumerate(selecttakenum):
                for key, date in enumerate(dataframe['date']):
                    if sqldate[1] == date.strftime('%Y-%m-%d'):
                        dataframe['num'][key] = selecttakenum[key1][0]
                        break
            result = json.loads(dataframe.to_json())
            data = {'data': result, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        # ccc
        elif type == '3':
            if not all([start_day, end_day]):
                return HttpResponse(json.dumps({"errmsg": "时间未传", "errno": "4001"}), content_type="application/json")
            # 选择购买量
            try:
                cursor.execute(
                    "select sum(actual_price),date_format(create_time,'%Y-%m-%d') from purchase_order where manager_id = '"+manager_id+"' and order_state='1' and create_time bETWEEN '"+datestart+"' and '"+dateend+"' and pay_state = '1' GROUP BY date_format(create_time,'%Y-%m-%d')")
                selectbuynum = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "本月购买量", "errno": "4001"}), content_type="application/json")
            import pandas as pd
            date = pd.date_range(datestart, dateend, freq='D')
            week = [int(i.strftime("%w")) for i in date] # 0表示星期日
            dataframe = pd.DataFrame({'date': date, 'week': week, 'num': 0.00})
            for key1, sqldate in enumerate(selectbuynum):
                for key, date in enumerate(dataframe['date']):
                    if sqldate[1] == date.strftime('%Y-%m-%d'):
                        dataframe['num'][key] = selectbuynum[key1][0]
                        break
            result = json.loads(dataframe.to_json())
            return JsonResponse({'data': result, "errmsg": "成功", "errno": "0"})

        # 交易数据
        elif type == '4':
            if not all([start_day, end_day]):
                return HttpResponse(json.dumps({"errmsg": "时间未传", "errno": "4001"}), content_type="application/json")

            # 下单人数，订单数，下单件数，下单金额
            try:
                cursor.execute(
                    "select COALESCE(count(o.user_addr),0),COALESCE(count(o.order_number),0),COALESCE(sum(g.goods_amount),0),COALESCE(sum(o.actual_price),0) from purchase_order as o,purchase_order_goods as g where manager_id = '" + manager_id + "' and o.order_state='1' and o.create_time bETWEEN '" + datestart + "' and '" + dateend + "' and o.order_number = g.order_number and pay_state != '2'")
                unpaidorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "今日订单总量今日销售总额", "errno": "4001"}), content_type="application/json")

            # 付款人数，付款订单数，付款件数，付款金额
            try:
                cursor.execute(
                    "select distinct count(o.user_addr),count(o.order_number),COALESCE(sum(g.goods_amount),0),COALESCE(sum(o.actual_price),0) from purchase_order as o,purchase_order_goods as g where manager_id = '" + manager_id + "' and o.order_state='1' and  o.create_time bETWEEN '" + datestart + "' and '" + dateend + "' and o.order_number = g.order_number and o.pay_state ='1'"
                )
                orderpaid = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "昨日销售总额", "errno": "4001"}), content_type="application/json")

            # 有效订单数
            try:
                cursor.execute(
                    "select count(order_number) from purchase_order where manager_id = '" + manager_id + "' and order_state='1' and create_time bETWEEN '" + datestart + "' and '" + dateend + "' and pay_state ='1'"
                )
                limitorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "七日销售总额", "errno": "4001"}), content_type="application/json")

            # 退款金额
            try:
                cursor.execute(
                    "select COALESCE(sum(refundFee),0) from apply_sale where orgAddr = '" + manager_id + "' and createdAt bETWEEN '" + datestart + "' and '" + dateend + "'"
                )
                offshelfmerchandise = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "已下架商品", "errno": "4001"}), content_type="application/json")

            # 客单价
            try:
                cursor.execute(
                    "select COALESCE(Round(sum(actual_price) / count(user_addr),2),0) from purchase_order where manager_id = '" + manager_id + "'and order_state='1'and pay_state = '1' and create_time bETWEEN '" + datestart + "' and '" + dateend + "'"
                )
                customerunitprice = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "已下架商品", "errno": "4001"}), content_type="application/json")
            dict = {
                'ordernum': to_string(unpaidorder[0][0]),  # 下单人数
                'ordernumber': unpaidorder[0][1],  # 订单数
                'lowerunitnum': to_string(unpaidorder[0][2]),  # 下单件数
                'orderamount': to_string(unpaidorder[0][3]),  # 下单金额
                'numpayments': orderpaid[0][0],  # 付款人数
                'numpaymentsorder': orderpaid[0][1],  # 付款订单数
                'numberpayments': to_string(orderpaid[0][2]),  # 付款件数
                'paymentsamount': to_string(orderpaid[0][3]),  # 付款金额
                'limitorder': limitorder[0][0],  # 有效订单数
                'offshelfmerchandise': to_string(offshelfmerchandise[0][0]),  # 退款金额
                'customerunitprice': to_string(customerunitprice[0][0]),  # 客单价
                'numbervisitors': 0,  # 浏览人数
            }
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        # 新老客户交易构成
        elif type == '5':
            if not all([year, month]):
                return HttpResponse(json.dumps({"errmsg": 'year,month$参数缺失', "errno": 4001}), content_type="application/json")
            import calendar
            try:
                monthRange = calendar.monthrange(eval(month), eval(month))
            except:
                return HttpResponse(json.dumps({"errmsg": "月份必须是1月-12月之间", "errno": 4001}), content_type="application/json")
            import datetime
            try:
                startTime = datetime.datetime(eval(year), eval(month), 1).strftime("%Y-%m-%d")
                end = datetime.datetime(eval(year), eval(month), 1) + datetime.timedelta(monthRange[1] - 1)
                endTime = end.strftime("%Y-%m-%d")
            except:
                return HttpResponse(json.dumps({"errmsg": "年份或者月份错误", "errno": 4001}), content_type="application/json")
            # 新客户付款金额 新客户付款人数
            try:
                cursor.execute(
                    "select count(distinct user_addr),COALESCE(sum(actual_price),0) from purchase_order where manager_id = '" + manager_id + "' and order_state='1'and create_time BETWEEN '" + startTime + " 00:00:00' and '" + endTime + " 23:59:59' and pay_state ='1' and user_addr in (select id from jld_user where create_time BETWEEN '" + startTime + " 00:00:00' and '" + endTime + " 23:59:59')")
                newclient = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "新客户", "errno": "4001"}), content_type="application/json")
            # 旧客户付款金额 旧客户付款人数
            try:
                cursor.execute(
                    "select count(distinct user_addr),COALESCE(sum(actual_price),0) from purchase_order where manager_id = '" + manager_id + "' and order_state='1'and create_time BETWEEN '" + startTime + " 00:00:00' and '" + endTime + " 23:59:59' and pay_state ='1' and user_addr not in (select id from jld_user where create_time BETWEEN '" + startTime + " 00:00:00' and '" + endTime + " 23:59:59')")
                oldclient = cursor.fetchall()

            except:
                return HttpResponse(json.dumps({"errmsg": "老客户", "errno": "4001"}), content_type="application/json")
            dict = {'newclientmoney': to_string(newclient[0][1]),  # 新客户付款人数
                    'newclientnum': newclient[0][0],  # 新客户付款金额
                    'oldclientmonry': to_string(oldclient[0][1]),  # 旧客户付款人数
                    'oldclientnum': oldclient[0][0]}  # 旧客户付款金额
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")

        # 交易数据
        elif type == '6':
            if not all([start_day, end_day]):
                return HttpResponse(json.dumps({"errmsg": "时间未传", "errno": "4001"}), content_type="application/json")
            # 交易数据
            try:
                cursor.execute(
                    "select actual_price from purchase_order where manager_id = '" + manager_id + "' and order_state='1'and pay_state = '1'and create_time bETWEEN '" + datestart + "' and '" + dateend + "' GROUP BY order_number ORDER BY actual_price")
                transactiondata = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "交易数据", "errno": "4001"}), content_type="application/json")
            list1 = [i for i in transactiondata if 0 < i[0] < 51]
            list2 = [i for i in transactiondata if 51 <= i[0] < 101]
            list3 = [i for i in transactiondata if 101 <= i[0] < 201]
            list4 = [i for i in transactiondata if 201 <= i[0] < 501]
            list5 = [i for i in transactiondata if 501 <= i[0] < 1000]
            list6 = [i for i in transactiondata if 1001 <= i[0] < 5001]
            list7 = [i for i in transactiondata if 5001 <= i[0] < 10001]
            list8 = [i for i in transactiondata if i[0] > 10001]
            dict = {
                '0-50元': len(list1),
                '51-100元': len(list2),
                '101-200元': len(list3),
                '201-500元': len(list4),
                '501-1000元': len(list5),
                '1001-5000元': len(list6),
                '5001-10000元': len(list7),
                '10001元以上': len(list8),
            }
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")

        # 商品统计
        elif type == '7':
            if not all([start_day, end_day, page, num]):
                return HttpResponse(json.dumps({"errmsg": "商家地址未传", "errno": "4001"}), content_type="application/json")
            numberbars = int(num)
            pages = int(page)
            # 商品销售情况  提货数量
            try:
                cursor.execute(
                    "select g.goods_id ,sum(g.goods_amount) from take_order as o,take_order_goods as g where o.manager_id = '" + manager_id + "' and o.create_date bETWEEN '" + datestart + "' and '" + dateend + "' and o.order_number = g.order_number GROUP BY g.goods_id")
                takegoodsnum = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "提货数量", "errno": "4001"}), content_type="application/json")

            # 商品销售情况  销售数量 销售金额
            try:
                cursor.execute(
                    "select g.goods_id,sum(g.goods_amount),sum(o.actual_price) from purchase_order as o, purchase_order_goods as g where o.manager_id = '" + manager_id + "' and o.order_state = '1' and o.create_time bETWEEN '" + datestart + "' and '" + dateend + "' and g.order_number = o.order_number and o.pay_state = '1' GROUP BY g.goods_id")
                amountsales = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "销售数量 销售金额", "errno": "4001"}), content_type="application/json")
            # 商品销售情况  付款人数 订单号
            try:
                cursor.execute(
                    "select g.goods_id, count(DISTINCT o.user_addr) from purchase_order as o, purchase_order_goods as g where o.manager_id = '" + manager_id + "' and o.order_state = '1' and o.create_time bETWEEN '" + datestart + "' and '" + dateend + "' and g.order_number = o.order_number and o.pay_state = '1' GROUP BY g.goods_id")
                peopel = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "付款人数 订单号", "errno": "4001"}), content_type="application/json")
            setlist = set()
            for i in takegoodsnum:
                setlist.add(i[0])
            for j in amountsales:
                setlist.add(j[0])
            for x in peopel:
                setlist.add(x[0])
            totalgoods = []
            for naem in setlist:
                # 商品销售情况  商品id  name
                try:
                    cursor.execute(
                        "select id,name from goods where id = '" + naem + "'")
                    idname = cursor.fetchall()
                except:
                    return HttpResponse(json.dumps({"errmsg": "商品id_name", "errno": "4001"}), content_type="application/json")
                totalgoods.append(idname)
            splilist = []
            for name in totalgoods:
                merchamt = {'id': name[0][0],
                            'numpayments': 0,  # 付款人数
                            'orgName': name[0][1],
                            'quantity': 0,  # 提货数量
                            'salesvolumes': 0,  # 销售数量
                            'saleamount': 0}  # 销售金额
                splilist.append(merchamt)
            for takekey, take in enumerate(takegoodsnum):
                for key, id in enumerate(splilist):
                    if take[0] == id['id']:
                        splilist[key]['quantity'] = to_string(takegoodsnum[takekey][1])
                        break
            for buykey, take in enumerate(amountsales):
                for key, id in enumerate(splilist):
                    if take[0] == id['id']:
                        splilist[key]['salesvolumes'] = to_string(amountsales[buykey][1])
                        splilist[key]['saleamount'] = to_string(amountsales[buykey][2])
                        break
            for takekey, take in enumerate(peopel):
                for key, id in enumerate(splilist):
                    if take[0] == id['id']:
                        splilist[key]['numpayments'] = to_string(peopel[takekey][1])
                        break
            dict = {'data': splilist[(pages - 1) * numberbars:pages * numberbars]}
            totalnum = len(splilist)
            dict['totalnum'] = totalnum
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")

        # 综合统计
        elif type == '8':
            if not all([start_day, end_day]):
                return HttpResponse(json.dumps({"errmsg": "时间未传", "errno": "4001"}), content_type="application/json")
            # 订单统计
            # 销售总额 订单总量
            try:
                cursor.execute(
                    "select sum(actual_price),count(order_number) from purchase_order where manager_id = '" + manager_id + "' and order_state = '1' and create_time BETWEEN '" + datestart + "' and '" + dateend + "' and pay_state ='1'")
                totalsalveorder = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "销售总额 订单总量", "errno": "4001"}), content_type="application/json")
            # 退货总数
            try:
                cursor.execute(
                    "select sum(amount) from apply_sale where orgAddr = '" + manager_id + "' and createdAt BETWEEN '" + datestart + "' and '" + dateend + "'")
                totalreturn = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "退货总数", "errno": "4001"}), content_type="application/json")
            # 用户提货总量完成
            try:
                cursor.execute(
                    "select sum(g.goods_amount) from take_order as t, take_order_goods as g where t.manager_id = '" + manager_id + "' and t.order_number = g.order_number  and t.take_state = '3' and t.create_date BETWEEN '" + datestart + "' and '" + dateend + "'")
                completedelivery = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "退货总数", "errno": "4001"}), content_type="application/json")
            # 退货总量
            try:
                cursor.execute(
                    "select sum(g.goods_amount) from take_order as t, take_order_goods as g where t.manager_id = '" + manager_id + "' and t.order_number = g.order_number  and t.create_date BETWEEN '" + datestart + "' and '" + dateend + "'")
                take = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "退货总数", "errno": "4001"}), content_type="application/json")

            # 商品总量
            try:
                cursor.execute(
                    "select sum(circulation) from goods where foreign_key = '" + foreign_key + "' and is_delete = '0' and is_represent = '0' and putaway = '0' and create_time BETWEEN '" + datestart + "' and '" + dateend + "' and name is not null")
                totalshop = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "商品总量", "errno": "4001"}), content_type="application/json")
            totaluser = set()
            # 会员总数
            try:
                cursor.execute(
                    "select id,name ,initial_account from goods where foreign_key = '" + foreign_key + "' and name is not null"
                )
                goodsid = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "goodsid", "errno": "4001"}), content_type="application/json")
            for id in goodsid:
                # 会员总数
                try:
                    cursor.execute(
                        "select userAddr from relation where goodsAddr = '" + id[0] + "' and createdAt BETWEEN '" + datestart + "' and '" + dateend + "'"
                    )
                    usercount = cursor.fetchall()
                except:
                    return HttpResponse(json.dumps({"errmsg": "会员总数", "errno": "4001"}), content_type="application/json")
                if usercount:
                    for data in usercount:
                        totaluser.add(data[0])
            # 购买卡券用户
            try:
                cursor.execute(
                    "select count(DISTINCT user_addr) from purchase_order where manager_id = '" + manager_id + "' and order_state = '1' and create_time BETWEEN '" + datestart + "' and '" + dateend + "' and pay_state ='1' ")
                totaluserbuy = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "用户总数", "errno": "4001"}), content_type="application/json")
            goodsidset = set()
            total = 0
            for info in goodsid:
                goodsidset.add(info[0][-2::])
                try:
                    cursor.execute(
                        "select sum(amount) from transfer_record where goodsAddr = '" + info[0] + "' and createdAt BETWEEN '" + datestart + "' and '" + dateend + " '"
                    )
                    result = cursor.fetchall()
                    if result[0][0] is not None:
                        total += result[0][0]
                except:
                    return HttpResponse(json.dumps({"errmsg": "转赠总数", "errno": "4001"}), content_type="application/json")
            # 领取卡券
            receive = 0
            for info in goodsidset:
                try:
                    cursor.execute(
                        "select sum(amount) from reviewrecord_" + info + " where type = '1' and createdAt BETWEEN '" + datestart + "' and '" + dateend + "' and goodsAddr in (select goodsAddr from goods where foreign_key = '" + foreign_key + "' and name is not null)"
                    )
                    result = cursor.fetchall()
                    if result[0][0] is not None:
                        receive += result[0][0]
                except:
                    return HttpResponse(json.dumps({"errmsg": "领取卡券", "errno": "4001"}), content_type="application/json")

            # 卡券剩余
            surplus = 0
            for info in goodsidset:
                try:
                    cursor.execute(
                        "SELECT sum(amount) from userbalance_" + info + " where userAddress = '" + goodsid[0][2] + "' and createdAt BETWEEN '" + datestart + "' and '" + dateend + "'"
                    )
                    result = cursor.fetchall()
                    if result[0][0] is not None:
                        surplus += result[0][0]
                except:
                    return HttpResponse(json.dumps({"errmsg": "卡券剩余", "errno": "4001"}), content_type="application/json")
            # 购买卡券用户
            buycard = set()
            for info in goodsidset:
                try:
                    cursor.execute(
                        "select toAddr from reviewrecord_" + info + " where type = '3' and createdAt BETWEEN '" + datestart + "' and '" + dateend + "' and goodsAddr in (select goodsAddr from goods where foreign_key = '" + foreign_key + "' and name is not null)"
                    )
                    result = cursor.fetchall()
                    if result:
                        buycard.add(result[0][0])
                except:
                    return HttpResponse(json.dumps({"errmsg": "购买卡券用户", "err no": "4001"}), content_type="application/json")
            dict = {
                'totalsales': to_string(totalsalveorder[0][0]),  # 销售总额
                'totalorders': to_string(totalsalveorder[0][1]),  # 订单总量
                'totalreturn': to_string(totalreturn[0][0]),  # 退货总量
                'completedelivery': to_string(completedelivery[0][0]),  # 提货总量完成
                'take': to_string(take[0][0]),  # 用户提货
                'totalshop': to_string(totalshop[0][0]),  # 商品总量
                'totaluser': len(totaluser),  # 用户总数
                'totaluserbuy': totaluserbuy[0][0],  # 用户购买总数
                'totalnumcardcoupon': to_string(total),  # 卡券转赠总数
                'todaytotalviews': 0,  # 今日总浏览量
                'totacardreceipt': to_string(receive),  # 卡券领取总量
                'totalcardsurplus': to_string(surplus),  # 卡券剩余总量
                'buycard': len(buycard),  # 购买卡券用户
            }
            data = {'data': dict, "errmsg": "成功", "errno": "0"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:

            return HttpResponse(json.dumps({"errmsg": "type参数错误", "errno": "4001"}), content_type="application/json")
