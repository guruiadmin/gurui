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
from reports_mjt.utils.decime import MyEncoder

mm = MyEncoder()

class ActiPersonQuery(View):

    def get(self, request):

        cursor = connections['default'].cursor()
        try:
            cursor.execute(
                "select r.activity, r.activityid, r.fromUserAddr,(select name from goods where id = r.goodsAddr) ,(select wx_nick_name from jld_user where id = r.fromUserAddr), sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),count(r.id), ((sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob))) / count(r.id)),min(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),max(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)) from rob_help as r, org_activity as a where r.activityid = a.id and r.activity is not null GROUP BY r.activityid, r.fromUserAddr order by count(r.id) desc"
            )
            activityid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "根据id和人分组", "errno": "4001"}), content_type="application/json")
        try:
            cursor.execute(
                "select r.activity, r.activityid, r.fromUserAddr,(select name from goods where id = r.goodsAddr) ,(select wx_nick_name from jld_user where id = r.fromUserAddr), sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),count(r.id), ((sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob))) / count(r.id)),min(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),max(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)) from rob_help as r, org_activity as a where r.activityid = a.id and r.activity is not null GROUP BY r.fromUserAddr order by count(r.id) desc"
            )
            userid = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "根据人分组", "errno": "4001"}), content_type="application/json")

        try:
            cursor.execute(
                "select r.activity, r.activityid, r.fromUserAddr,(select name from goods where id = r.goodsAddr) ,(select wx_nick_name from jld_user where id = r.fromUserAddr), sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),count(r.id), ((sum(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob))) / count(r.id)),min(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)),max(unix_timestamp(r.createdAt) -unix_timestamp(a.startRob)) from rob_help as r, org_activity as a where r.activityid = a.id and r.activity is not null GROUP BY r.activity, r.fromUserAddr order by count(r.id) desc"
            )
            activity = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": "根据id和人分组", "errno": "4001"}), content_type="application/json")
        import xlwt

        book = xlwt.Workbook()  # 新建一个excel
        sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
        row = 0  # 控制行
        for stu in activityid:
            col = 0  # 控制列
            for s in stu:  # 再循环里面list的值，每一列
                sheet.write(row, col, s)
                col += 1
            row += 1
        book.save('goods_user.xls')  # 保存到当前目录下
        book = xlwt.Workbook()  # 新建一个excel
        sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
        row = 0  # 控制行
        for stu in userid:
            col = 0  # 控制列
            for s in stu:  # 再循环里面list的值，每一列
                sheet.write(row, col, s)
                col += 1
            row += 1
        book.save('user.xls')  # 保存到当前目录下

        book = xlwt.Workbook()  # 新建一个excel
        sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
        row = 0  # 控制行
        for stu in activity:
            col = 0  # 控制列
            for s in stu:  # 再循环里面list的值，每一列
                sheet.write(row, col, s)
                col += 1
            row += 1
        book.save('activity_user.xls')  # 保存到当前目录下
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
        return HttpResponse(json.dumps({"P":"P"}), content_type="application/json")
