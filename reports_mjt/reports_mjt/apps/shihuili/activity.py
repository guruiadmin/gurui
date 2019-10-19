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
from datetime import datetime
from django.views import View
from public.models import OrgActivity, GoodsOrm, ManageOrm
from reports_mjt.utils.data_select import localutc, userutc
from reports_mjt.utils.decime import MyEncoder

func = MyEncoder()

class ActiPersonQuery(View):
    def get(self, request):
        start = request.GET.get('start', '1438473600.0')
        end = request.GET.get('end', '1438473600.0')
        page = request.GET.get('page', 1)
        num = request.GET.get('num', 10)
        type = request.GET.get('type')

        infodict = {
            'start': str(localutc(float(start))),
            'end': str(localutc(float(end))),
            'page': page,
            'type': type,
            'num': num,
        }
        return TypeClass().create(infodict)

class TypeClass(object):
    def create(self, dict):
        distrdict = {
            '0': Select1().funcdata(dict),  # 选择时间查询
            '1': Total().funcdata(dict),  # 全部活动
            '2': HaveHand().funcdata(dict),  # 进行中
            '3': HasEnd().funcdata(dict),  # 已结束
            # '4': NotBegun().funcdata(dict),  # 未开始
        }
        return distrdict.get(dict['type'])

# 选择时间
class Select(object):
    def funcdata(self, dict):
        try:
            total = OrgActivity.objects.exclude(robNum=0).filter(startRob__range=(dict['start'], dict['end']), startRob__isnull=False, stopRob__isnull=False, goodsAddr__isnull=False, activityId__isnull=False).count()
            activity = OrgActivity.objects.exclude(robNum=0).filter(startRob__range=(dict['start'], dict['end']), startRob__isnull=False, stopRob__isnull=False, goodsAddr__isnull=False, activityId__isnull=False).order_by('-startRob')[(int(dict['page']) - 1) * int(dict['num']):int(dict['page']) * int(dict['num'])]
        except OrgActivity.DoesNotExist:
            return HttpResponse(status=404)
        return Result().funcdata(activity, total)

class Select1(object):
    def funcdata(self, dict):
        try:
            # total = GoodsOrm.objects.values_list('name')
            # activity = GoodsOrm.objects.all().only('name')
            total = GoodsOrm.objects.all()
            activity = GoodsOrm.objects.all()
        except GoodsOrm.DoesNotExist:
            return HttpResponse(status=404)
        return Result().funcdata(activity, total)

# 全部活动
class Total(object):
    def funcdata(self, dict):
        try:
            total = OrgActivity.objects.exclude(robNum=0).filter(startRob__isnull=False, stopRob__isnull=False, goodsAddr__isnull=False, activityId__isnull=False).count()
            activity = OrgActivity.objects.exclude(robNum=0).filter(startRob__isnull=False, stopRob__isnull=False, goodsAddr__isnull=False, activityId__isnull=False).order_by('-startRob')[(int(dict['page']) - 1) * int(dict['num']):int(dict['page']) * int(dict['num'])]
        except OrgActivity.DoesNotExist:
            return HttpResponse(status=404)
        return Result().funcdata(activity, total)

# 进行中
class HaveHand(object):
    def funcdata(self, dict):
        try:
            total = OrgActivity.objects.exclude(robNum=0).filter(startRob__lt=datetime(int(dict['end'][0:4]), int(dict['end'][5:7]), int(dict['end'][8:10]), int(dict['end'][11:13]), int(dict['end'][14:16]), int(dict['end'][17:19])), stopRob__gt=datetime(int(dict['end'][0:4]), int(dict['end'][5:7]), int(dict['end'][8:10]),int(dict['end'][11:13]), int(dict['end'][14:16]), int(dict['end'][17:19])), startRob__isnull=False, stopRob__isnull=False, goodsAddr__isnull=False, activityId__isnull=False).count()

            activity = OrgActivity.objects.exclude(robNum=0).filter(stopRob__gt=datetime(int(dict['end'][0:4]), int(dict['end'][5:7]), int(dict['end'][8:10]),int(dict['end'][11:13]), int(dict['end'][14:16]), int(dict['end'][17:19])), startRob__lt=datetime(int(dict['end'][0:4]), int(dict['end'][5:7]), int(dict['end'][8:10]), int(dict['end'][11:13]), int(dict['end'][14:16]), int(dict['end'][17:19])), startRob__isnull=False, stopRob__isnull=False, goodsAddr__isnull=False, activityId__isnull=False).order_by('-startRob')[(int(dict['page']) - 1) * int(dict['num']):int(dict['page']) * int(dict['num'])]
        except OrgActivity.DoesNotExist:
            return HttpResponse(status=404)
        return Result().funcdata(activity, total)

# 已结束
class HasEnd(object):
    def funcdata(self, dict):
        try:
            total = OrgActivity.objects.exclude(robNum=0).filter(stopRob__lt=datetime(int(dict['end'][0:4]), int(dict['end'][5:7]), int(dict['end'][8:10]), int(dict['end'][11:13]), int(dict['end'][14:16]), int(dict['end'][17:19])), startRob__isnull=False, stopRob__isnull=False, goodsAddr__isnull=False, activityId__isnull=False).count()
            activity = OrgActivity.objects.exclude(robNum=0).filter(stopRob__lt=datetime(int(dict['end'][0:4]), int(dict['end'][5:7]), int(dict['end'][8:10]), int(dict['end'][11:13]), int(dict['end'][14:16]), int(dict['end'][17:19])), startRob__isnull=False, stopRob__isnull=False, goodsAddr__isnull=False, activityId__isnull=False).order_by('-startRob')[(int(dict['page']) - 1) * int(dict['num']):int(dict['page']) * int(dict['num'])]
        except OrgActivity.DoesNotExist:
            return HttpResponse(status=404)
        return Result().funcdata(activity, total)


class Result(object):
    def funcdata(self,  activity, total):
        cursor = connections['default'].cursor()
        open = []
        newopen = []
        newuserlist = []
        olduserlist = []
        datadict = []
        for info in activity:
            datadict.append({
                             "activiyy": info.id,  # 活动商品id
                             'orgaddr': info.orgAddr,  # 商家id
                             'goodsaddr': info.goodsAddr,  # 商品id
                             'start': func.default(info.startRob),
                             'end': func.default(info.stopRob),
                             'startime': func.str_time_stamp(info.startRob),  # 活动开始时间
                             'endtime': func.str_time_stamp(info.stopRob),  # 活动结束时间
                             'robnum': info.robNum,  # 活动商品数量
                             'debrisnum': info.debrisNum,  # 商品碎片数量
                             'times': info.times,  # 助力次数
                             'participants': info.participants,  # 活动属性
                             'returnRobNum': info.returnRobNum,  # 剩余商品数量
                             'open': 0,  # 打开总量
                             'newopen': 0,  # 打开新用户量
                             'olduser': 0,  # 参与用户量
                             'newuser': 0,  # 新用户量
                             })
        for info in datadict:
            # 新用户数
            try:
                cursor.execute(
                    "select count(DISTINCT toUserAddr),activityid,goodsAddr from rob_help where activityid = '" + info['activiyy'] + "' and toUserAddr in (select id from jld_user where create_time BETWEEN '" + userutc(info['start']) + "' and '" + userutc(info['end']) + "')"
                )
                new = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "新用户数", "errno": "4001"}), content_type="application/json")
            newuserlist.append(new)

            # 参与用户量
            try:
                cursor.execute(
                    "select count(DISTINCT toUserAddr),activityid,goodsAddr from rob_help where activityid = '" + info['activiyy'] + "' ")
                old = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "参与用户量", "errno": "4001"}), content_type="application/json")
            olduserlist.append(old)

            # 打开总量
            try:
                cursor.execute(
                    "select count(DISTINCT userAddr),activityid,goodsAddr from activity_user where activityid = '" + info['activiyy'] + "'"
                )
                opennum = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "打开总量", "errno": "4001"}), content_type="application/json")
            open.append(opennum)

            # 打开新用户总量
            try:
                cursor.execute(
                    "select count(DISTINCT userAddr),activityid,goodsAddr from activity_user where activityid = '" + info['activiyy'] + "' and userAddr in (select id from jld_user where create_time BETWEEN '" + userutc(info['start']) + "' and '" + userutc(info['end']) + "')"
                )
                opennumnew = cursor.fetchall()
            except:
                return HttpResponse(json.dumps({"errmsg": "打开新用户总量", "errno": "4001"}), content_type="application/json")
            newopen.append(opennumnew)



        for key, data in enumerate(datadict):
            for key2, info in enumerate(olduserlist):
                if data['activiyy'] == info[0][1]:
                    datadict[key]['olduser'] = int(olduserlist[key2][0][0]) + (int(data['robnum']) - int(data['returnRobNum']))
        for data in datadict:
            for info in newuserlist:
                if data['activiyy'] == info[0][1]:
                    data['newuser'] = info[0][0]
        for data in datadict:
            for info in open:
                if data['activiyy'] == info[0][1]:
                    data['open'] = info[0][0]
        for data in datadict:
            for info in newopen:
                if data['activiyy'] == info[0][1]:
                    data['newopen'] = info[0][0]
        for name in datadict:
            try:
                goodsname = GoodsOrm.objects.filter(id=name['goodsaddr'])
            except GoodsOrm.DoesNotExist:
                return HttpResponse(status=404)
            for goods in goodsname:
                name['goodaname'] = goods.name
            try:
                goodsname = ManageOrm.objects.filter(id=name['orgaddr'])
            except ManageOrm.DoesNotExist:
                return HttpResponse(status=404)
            for goods in goodsname:
                name['orgname'] = goods.name
        dict = {'data': {'data': datadict, 'total': total}, "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(dict), content_type="application/json")

