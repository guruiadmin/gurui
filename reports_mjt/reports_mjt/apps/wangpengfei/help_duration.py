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
import xlwt
from django.db import connections
from django.http import HttpResponse
import json
from django.views import View
import datetime

from public.models import Endorsementuser
from reports_mjt.utils.data_select import commission_price
from reports_mjt.utils.decime import MyEncoder, to_string
import time

mm = MyEncoder()

#小程序
class Activity(View):
    def get(self, request):
        global cursor
        cursor = connections['default'].cursor()
        distrdict = {
            '0': PythonClass0().funcdata(),
            '1': PythonClass1().funcdata(),
            '2': PythonClass2().funcdata(),
            '3': PythonClass3().funcdata(),#佣金导出
            '4': PythonClass4().funcdata(),  # 恢复佣金数据
        }
        return distrdict.get(request.GET.get('type'))


class PythonClass4(object):
    def funcdata(self):
        timedate = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        time_stamp = int(time.time())
        # 可提现
        try:
            cursor.execute(
                "select affiliateID from purchase_order, purchase_order_goods where affiliateID is not null GROUP BY affiliateID"
            )
            affid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "可提现", "errno": "400"}), content_type="application/json")
        for usid in affid:
            try:
                cursor.execute(
                    "select COALESCE(sum(g.commission * g.goods_amount), 0) - (select COALESCE(sum(amount),0) from withdrawals_record where user_id = '" + usid[ 0] + "' and state IN ('1', '0')) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" + usid[0] + "' and o.pay_state = '1' and o.pay_time < '" + commission_price( time_stamp) + "' and o.order_number = g.order_number"
                )
                withdrawal = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "可提现", "errno": "400"}), content_type="application/json")
            if withdrawal[0][0] > 0:

                try:
                    sum = Endorsementuser.objects.filter(id=usid[0]).count()
                except Endorsementuser.DoesNotExist:
                    return HttpResponse(status=404)
                if sum > 0:
                    cursor.execute(
                        "update endorsement_user set cash_withdrawal = '" + str(withdrawal[0][0]) + "' Where id='{}'".format(usid[0])
                    )
                else:
                    cursor.execute(
                        "select id,unionid,phone,name,wx_nick_name,sex,head_url,wx_head_url from jld_user where id = '" + usid[0] + "'"
                    )
                    datall = cursor.fetchall()
                    try:
                        cursor.execute(
                            "insert into endorsement_user(id,unionid,phone,name,wx_nick_name,sex,head_url,wx_head_url,cash_withdrawal,create_time) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(datall[0][0], datall[0][1], datall[0][2], datall[0][3], datall[0][4], datall[0][5], datall[0][6], datall[0][7], withdrawal[0][0], timedate)
                        )
                    except:
                        return HttpResponse(json.dumps({"errmsg": "可提现2", "errno": "400"}),  content_type="application/json")

            # 冻结
            try:
                cursor.execute(
                    "select COALESCE(sum(g.commission * g.goods_amount), 0) from purchase_order_goods as g, purchase_order as o where g.affiliateID = '"+  usid[0] + "' and o.pay_state = '1' and o.pay_time > '" + commission_price(time_stamp) + "' and o.order_number = g.order_number "
                )
                thaw = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "冻结", "errno": "400"}), content_type="application/json")
            if thaw[0][0] > 0:
                try:
                    sum = Endorsementuser.objects.filter(id=usid[0]).count()
                except Endorsementuser.DoesNotExist:
                    return HttpResponse(status=404)
                if sum > 0:
                    cursor.execute(
                        "update endorsement_user set frozen = '" + str(thaw[0][0]) + "' Where id='{}'".format(usid[0])
                    )
                else:
                    cursor.execute(
                        "select id,unionid,phone,name,wx_nick_name,sex,head_url,wx_head_url from jld_user where id = '" + usid[0] + "'"
                    )
                    datall = cursor.fetchall()
                    try:
                        cursor.execute(
                            "insert into endorsement_user(id,unionid,phone,name,wx_nick_name,sex,head_url,wx_head_url,frozen,create_time) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format( datall[0][0], datall[0][1], datall[0][2], datall[0][3], datall[0][4], datall[0][5], datall[0][6], datall[0][7], thaw[0][0], timedate)
                        )
                    except:
                        return HttpResponse(json.dumps({"errmsg": "可冻结2", "errno": "400"}),  content_type="application/json")

        return HttpResponse(json.dumps({'data': {'thaw': 'llll', 'withdrawal': 'kkkk'}, "errmsg": "成功", "errno": "200"}), content_type="application/json")


class PythonClass3(object):
    def funcdata(self):
        time_stamp = int(time.time())
        # 可提现
        try:
            cursor.execute(
                "select g.affiliateID from purchase_order as o, purchase_order_goods as g where g.order_number = o.order_number and g.affiliateID is not null GROUP BY g.affiliateID"
            )
            affid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "可提现", "errno": "400"}), content_type="application/json")
        cashlist = []
        forzelist = []
        for usid in affid:
            try:
                cursor.execute(
                    "select COALESCE(sum(g.commission * g.goods_amount), 0) - (select COALESCE(sum(amount),0) from withdrawals_record where user_id = '" +
                    usid[
                        0] + "' and state in ('1','0')),(select name from jld_user where id = g.affiliateID),g.affiliateID from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" +
                    usid[0] + "' and o.pay_state = '1' and o.pay_time < '" + commission_price(
                        time_stamp) + "' and o.order_number = g.order_number"
                )
                withdrawal = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "可提现", "errno": "400"}), content_type="application/json")
            if withdrawal[0][0] > 0:
                cashlist.append(withdrawal)

            # 冻结
            try:
                cursor.execute(
                    "select COALESCE(sum(g.commission * g.goods_amount ), 0),(select name from jld_user where id = g.affiliateID),g.affiliateID  from purchase_order_goods as g, purchase_order as o where g.affiliateID = '" +
                    usid[0] + "' and o.pay_state = '1' and o.pay_time > '" + commission_price(
                        time_stamp) + "' and o.order_number = g.order_number "
                )
                thaw = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "冻结", "errno": "400"}), content_type="application/json")
            if thaw[0][0] > 0:
                forzelist.append(thaw)
        resultdict = []
        for info in affid:
            datadict = OrderedDict()
            datadict['id'] = info[0]
            datadict['name'] = ''
            datadict['cash'] = 0
            datadict['frozen'] = 0
            resultdict.append(datadict)

        for info in forzelist:
            for data in resultdict:
                if data['id'] == info[0][2]:
                    data['frozen'] = to_string(info[0][0])
                    data['name'] = to_string(info[0][1])

        for info in cashlist:
            for data in resultdict:
                if data['id'] == info[0][2]:
                    data['cash'] = to_string(info[0][0])
                    data['name'] = to_string(info[0][1])

        book = xlwt.Workbook()  # 新建一个excel
        sheet = book.add_sheet('case1_sheet', cell_overwrite_ok=True)  # 添加一个sheet页
        row0 = ["用户ID", "用户名称", "入账", "解冻中"]
        row = 0  # 控制行
        # 生成第一行
        for i in range(0, len(row0)):
            sheet.write(0, i, row0[i])
            row += 1

        row = 1  # 控制行
        for stu in resultdict:
            col = 0  # 控制列
            for s in stu:  # 再循环里面list的值，每一列
                sheet.write(row, col, stu.get(s))
                col += 1
            row += 1
        book.save('Commission.xls')  # 保存到当前目录下

        return HttpResponse(
            json.dumps({'data': {'thaw': 'llll', 'withdrawal': 'kkkk'}, "errmsg": "成功", "errno": "200"}),
            content_type="application/json")


class PythonClass1(object):

    def funcdata(self):
        try:
            cursor.execute(
                "select DATE_FORMAT(o.create_time,'%Y-%m-%d'),(select name from manager where id = o.manager_id), sum(g.goods_amount), sum(o.actual_price) from purchase_order as o, purchase_order_goods as g where o.pay_state = '1' and g.order_number = o.order_number GROUP BY DATE_FORMAT(o.create_time,'%Y-%m-%d'), o.manager_id ORDER BY o.CREATE_time desc"

            )
            managefinance = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "根据日期商家分组", "errno": "4001"}), content_type="application/json")
        try:
            cursor.execute(
                "select DATE_FORMAT(o.create_time,'%Y-%m-%d'), sum(g.goods_amount), sum(o.actual_price) from purchase_order as o, purchase_order_goods as g where o.pay_state = '1' and g.order_number = o.order_number GROUP BY DATE_FORMAT(o.create_time,'%Y-%m-%d') ORDER BY o.CREATE_time desc"

            )
            finance = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "根据日期分组", "errno": "4001"}), content_type="application/json")
        # import xlwt

        # book = xlwt.Workbook()  # 新建一个excel
        # sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
        # row = 0  # 控制行
        # for stu in finance:
        #     col = 0  # 控制列
        #     for s in stu:  # 再循环里面list的值，每一列
        #         sheet.write(row, col, s)
        #         col += 1
        #     row += 1
        # book.save('finance.xls')  # 保存到当前目录下
        return HttpResponse(json.dumps({"P": "P"}), content_type="application/json")


class PythonClass0(object):

    def funcdata(self):
        try:
            cursor.execute(
                "select r.activity, r.activityid, r.fromUserAddr,(select name from goods where id = r.goodsAddr) ,(select wx_nick_name from jld_user where id = r.fromUserAddr), sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),count(r.id), ((sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob))) / count(r.id)),min(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),max(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)) from rob_help as r, org_activity as a where r.activityid = a.id and r.activityid is not null GROUP BY r.activityid, r.fromUserAddr order by count(r.id) desc"
            )
            activityid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "根据id和人分组", "errno": "4001"}), content_type="application/json")
        try:
            cursor.execute(
                # "select r.activity, r.activityid, r.fromUserAddr,(select name from goods where id = r.goodsAddr) ,(select wx_nick_name from jld_user where id = r.fromUserAddr), sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),count(r.id), ((sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob))) / count(r.id)),min(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),max(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)) from rob_help as r, org_activity as a where r.activityid = a.id and r.activity is not null GROUP BY r.fromUserAddr order by count(r.id) desc"


                "select r.fromUserAddr,(select wx_nick_name from jld_user where id = r.fromUserAddr), sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),count(r.id), ((sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob))) / count(r.id)),min(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),max(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)) from rob_help as r, org_activity as a where r.activityid = a.id GROUP BY r.fromUserAddr order by count(r.id) desc"
            )
            userid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "根据人分组", "errno": "4001"}), content_type="application/json")

        try:
            cursor.execute(
                "select DISTINCT userAddr, (select wx_nick_name from jld_user where id = userAddr) from activity_user where userAddr not in (select DISTINCT fromUserAddr from rob_help)"
            )
            notuserid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": '没有助力', "errno": "4001"}), content_type="application/json")
        try:
            cursor.execute(
                "select r.activity, r.activityid, r.fromUserAddr,(select name from goods where id = r.goodsAddr) ,(select wx_nick_name from jld_user where id = r.fromUserAddr), sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),count(r.id), ((sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob))) / count(r.id)),min(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),max(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)) from rob_help as r, org_activity as a where r.activityid = a.id GROUP BY r.activity, r.fromUserAddr order by count(r.id) desc"
            )
            activity = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "根据id和人分组", "errno": "4001"}), content_type="application/json")
        # import xlwt
        #
        # book = xlwt.Workbook()  # 新建一个excel
        # sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
        # row = 0  # 控制行
        # for stu in activityid:
        #     col = 0  # 控制列
        #     for s in stu:  # 再循环里面list的值，每一列
        #         sheet.write(row, col, s)
        #         col += 1
        #     row += 1
        # book.save('goods_user.xls')  # 保存到当前目录下
        # book = xlwt.Workbook()  # 新建一个excel
        # sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
        # row = 0  # 控制行
        # for stu in userid:
        #     col = 0  # 控制列
        #     for s in stu:  # 再循环里面list的值，每一列
        #         sheet.write(row, col, s)
        #         col += 1
        #     row += 1
        # book.save('user.xls')  # 保存到当前目录下
        #
        # book = xlwt.Workbook()  # 新建一个excel
        # sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
        # row = 0  # 控制行
        # for stu in notuserid:
        #     col = 0  # 控制列
        #     for s in stu:  # 再循环里面list的值，每一列
        #         sheet.write(row, col, s)
        #         col += 1
        #     row += 1
        # book.save('notuser.xls')  # 保存到当前目录下
        #
        # book = xlwt.Workbook()  # 新建一个excel
        # sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
        # row = 0  # 控制行
        # for stu in activity:
        #     col = 0  # 控制列
        #     for s in stu:  # 再循环里面list的值，每一列
        #         sheet.write(row, col, s)
        #         col += 1
        #     row += 1
        # book.save('activity_user.xls')  # 保存到当前目录下
        # # 实验
        # try:
        #     cursor.execute(
        #         "select id from org_activity where times = 1"
        #     )
        #     id1 = cursor.fetchall()
        # except:
        #     return HttpResponse(json.dumps({"errmsg": "打开新用户总量", "errno": "4001"}), content_type="application/json")
        # idlist = []
        # idinfo = set()
        # for id in id1:
        #     # try:
        #     #     cursor.execute(
        #     #         "select activityId,goodsAddr,count(DISTINCT toUserAddr),createdAt from rob_help where activityid = '" + id[0]+ "' "
        #     #     )
        #     #     id2 = cursor.fetchall()
        #     # except:
        #     #     return HttpResponse(json.dumps({"errmsg": "打开新用户总量", "errno": "4001"}),   content_type="application/json")
        #     try:
        #         cursor.execute(
        #             "select activityid,toUserAddr,fromUserAddr from rob_help where activityid = '" + id[0]+ "' "
        #               # "select activityid,goodsAddr,toUserAddr,createdAt from rob_help where activityid = '188bbbc0-8123-11e9-97b6-9bf1cffb7d69' "
        #         )
        #         id3 = cursor.fetchall()
        #     except:
        #         return HttpResponse(json.dumps({"errmsg": "打开新用户总量", "errno": "4001"}),   content_type="application/json")
        #     for info in id3:
        #         if not info:
        #             pass
        #         elif info in idlist:
        #             idinfo.add(info)
        #         else:
        #             idlist.append(info)
        # infolist = []
        # for id in idinfo:
        #     try:
        #         cursor.execute(
        #             "select activityId,goodsAddr,toUserAddr,createdAt from rob_help where activityid = '" + id[0]+ "' and toUserAddr = '"+id[1]+"' "
        #         )
        #         iddata = cursor.fetchall()
        #     except:
        #         return HttpResponse(json.dumps({"errmsg": "打开新用户总量", "errno": "4001"}),   content_type="application/json")
        #     if iddata:
        #         for info in iddata:
        #             infolist.append({'activityid': info[0], 'goodsAddr': info[1], 'toUserAddr': info[2], 'createdAt': mm.default(info[3])})
        # data = {'data': infolist}

        return HttpResponse(json.dumps({"P": "P"}), content_type="application/json")


class PythonClass2(object):

    def funcdata(self):
        # 财务需要
        start = '2019-07-21 16:00:00'
        end = '2019-07-28 16:00:00'
        # 商户商品信息
        try:
            cursor.execute(
                "select m.id,m.name,s.id,s.name,s.circulation, s.initial_account from goods as s, manager as m where s.state in ('2','4') and  s.foreign_key = m.foreign_key and s.name is not null GROUP BY s.id ORDER BY m.id, s.id desc"
            )
            shopgoods = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "商户商品信息", "errno": "4001"}), content_type="application/json")

        # 购买详情
        try:
            cursor.execute(
                "select g.goods_id,sum(g.goods_amount),sum(o.actual_price) from purchase_order as o, purchase_order_goods as g where o.pay_time BETWEEN '" + start + "' and '" + end + "' and  o.pay_state = '1' and g.order_number = o.order_number  GROUP BY g.goods_id "
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
                "select g.goods_id,sum(g.goods_amount) from take_order_goods as g, take_order as o where o.create_date BETWEEN '" + start + "' and '" + end + "' and o.order_state = '0' and o.take_state in('2','3') and o.order_number = g.order_number GROUP BY g.goods_id "
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
            # try:
            cursor.execute(
                "select goodsAddr,sum(amount) from userbalance_" + info[2][-2::] + " where userAddress != '" + info[5] + "' and goodsAddr = '" + info[2] + "'"
            )
            fromuser = cursor.fetchall()
            # except:
            #     return HttpResponse(json.dumps({"errmsg": "商品地址和数量", "errno": "4001"}),  content_type="application/json")
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

        book = xlwt.Workbook()  # 新建一个excel
        sheet = book.add_sheet('case1_sheet', cell_overwrite_ok=True)  # 添加一个sheet页
        row0 = ["商户ID", "商户名称", "商品ID", "商品名称", "发行总数", "库存数量", "购买数量", "购买金额", "提货数量"]
        row = 0  # 控制行
        # 生成第一行
        for i in range(0, len(row0)):
            sheet.write(0, i, row0[i])
            row += 1

        row = 1  # 控制行
        for stu in resultdict:
            col = 0  # 控制列
            for s in stu:  # 再循环里面list的值，每一列
                sheet.write(row, col, stu.get(s))
                col += 1
            row += 1
        book.save('finance.xls')  # 保存到当前目录下
        # with open("Finance.csv", "w") as csvfile:
        #     writer = csv.writer(csvfile)
        #
        #     # 先写入columns_name
        #     writer.writerow(["商户ID", "商户名称", "商品ID", "商品名称", "发行总数", "库存数量", "购买数量", "购买金额", "提货数量"])
        #     # 写入多行用writerows
        #     for write in resultdict:
        #         writer.writerow([write["manageid"], write["managename"], write["goodsid"], write["goodsname"], str(write["totalnum"]), str(write["surplus"]), str(write["buynum"]), str(write["buyprice"]), str(write["takenum"])])
        return HttpResponse(json.dumps({'data': 222, "errmsg": "555", "errno": "4001"}),  content_type="application/json")

#http://127.0.0.1:8000/wapi/wpf?type=1

