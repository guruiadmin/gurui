'''
/**
* Copyright ©2017-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 北京和信汇通科技开发有限公司 版权所有
*
*/
'''
import copy
from datetime import date, timedelta
import json
from django.http import HttpResponse
import time
import calendar
from django.utils import timezone as datetime
from public.models import ManageOrm
from public.models import UserData
from reports_mjt.utils.decime import to_string
import datetime


day_now = time.localtime()
day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)

def ormdate():
    ormyesday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
    ormtomorrow = (date.today() + timedelta(days=+1)).strftime("%Y-%m-%d %H:%M:%S")
    ormtoday = (date.today()).strftime("%Y-%m-%d %H:%M:%S")
    ormweekdate = (date.today() + timedelta(days=-6)).strftime("%Y-%m-%d %H:%M:%S")
    ormonthday = (date.today() + timedelta(days=-29)).strftime("%Y-%m-%d %H:%M:%S")
    ormonthsday = (date.today() + timedelta(days=-89)).strftime("%Y-%m-%d %H:%M:%S")
    agodate = (date.today() + timedelta(days=-30))
    timetoday = datetime.date.today()
    timeyesterday = timetoday - datetime.timedelta(days=1)
    yesterday_start_time = int(time.mktime(time.strptime(str(timeyesterday), '%Y-%m-%d'))) - 28800
    yesterday_end_time = (int(time.mktime(time.strptime(str(timetoday), '%Y-%m-%d'))) - 1) - 28800
    ormdatedict = {
        'month': ormonthday,
        'week': [ormweekdate, ormtoday],
        'total': ['2018-11-26', ormtoday],
        'today': ormtoday,
        'yesday': ormyesday,
        'months': ormonthsday,
        'day_begin': [day_begin, day_begin],
        'day_end': [day_end, day_end],
        'tomorow': ormtomorrow,
        'agodate': agodate,
        'startstamp': yesterday_start_time,
        'endstamo': yesterday_end_time,
         }
    return ormdatedict

def merchant():
    indextoday = datetime.date.today()
    indexyesday = int(time.mktime(time.strptime(str(indextoday - datetime.timedelta(days=1)), '%Y-%m-%d')))
    #select * from manager ORDER BY convert(name using gbk) ASC
    try:
        managename = ManageOrm.objects.filter(name__isnull=False)
    except UserData.DoesNotExist:
        return HttpResponse(status=404)
    splilist2 = []
    for info in managename:
        dict = {
            'id': info.id,
            'date': indexyesday,
            'orgName': info.name,
            'purchase': 0,
            'total': 0,
            'tabkegoods': 0,
        }
        splilist2.append(dict)
    return splilist2


class OrmFunctionObject(object):
    # 转换时间类型拼接字典
    def timedict(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime
        datestart = datetime.datetime.strptime(self.startTime, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(self.endTime, '%Y-%m-%d')
        date_list = []
        datestart = datestart - datetime.timedelta(days=1)
        while datestart < dateend:
            datestart += datetime.timedelta(days=1)
            qu = datestart.strftime('%Y-%m-%d')
            date_list.append(qu)
        total_list = [0 for _ in range(len(date_list))]
        dict = {
            'date': date_list,
            'number': copy.deepcopy(total_list),
        }
        return dict

    def buytake(self, takeorder, buyorder, splilist, pages, numberbars):
        self.takeorder = takeorder
        self.buyorder = buyorder
        self.splilist = splilist
        self.pages = pages
        self.numberbars = numberbars
        for takekey, take in enumerate(self.takeorder):
            for key, id in enumerate(self.splilist):
                if take['manager_id'] == id['id']:
                    self.splilist[key]['tabkegoods'] = self.takeorder[takekey].get('count')
        for buykey, take in enumerate(self.buyorder):
            for key, id in enumerate(self.splilist):
                if take['manager_id'] == id['id']:
                    self.splilist[key]['purchase'] = self.buyorder[buykey].get('count')
                    self.splilist[key]['total'] = to_string(self.buyorder[buykey].get('money'))
        dict = {'data': self.splilist[(self.pages - 1) * self.numberbars:self.pages * self.numberbars]}
        totalnum = len(self.splilist)
        dict['totalnum'] = totalnum
        return {'data': dict, "errmsg": "成功", "errno": "0"}

    def startend(self, start_day, end_day):
        self.start_day = start_day
        self.end_day = end_day
        s_time = time.mktime(time.strptime(self.start_day, "%Y-%m-%d"))
        e_time = time.mktime(time.strptime(self.end_day, "%Y-%m-%d"))
        if (float(s_time) > float(e_time)):
            return HttpResponse(json.dumps({"errmsg": "订单统计时间顺序不对", "errno": "4001"}), content_type="application/json")
        startday = start_day + ' 00:00:00'
        endday = end_day + ' 23:59:59'
        return startday, endday

