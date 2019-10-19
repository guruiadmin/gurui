import copy
import json
from django.http import HttpResponse
import time
import calendar
import datetime

from reports_mjt.utils.decime import to_string

def utc(local_st):
    utc_st = time.localtime(local_st - 28800)
    result = time.strftime("%Y-%m-%d %H:%M:%S", utc_st)
    return result
day_now = time.localtime()
day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)


#获取各种时间戳
tday = datetime.date.today()
yesterday = tday - datetime.timedelta(days=1)
tomorrow = tday + datetime.timedelta(days=1)
weekday = tday - datetime.timedelta(days=6)
month = tday - datetime.timedelta(days=29)
months = tday - datetime.timedelta(days=89)
yesterday_start = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
yesterday_end = int(time.mktime(time.strptime(str(tday), '%Y-%m-%d'))) - 1
weekday_start = int(time.mktime(time.strptime(str(weekday), '%Y-%m-%d')))
month_start = int(time.mktime(time.strptime(str(month), '%Y-%m-%d')))
months_start = int(time.mktime(time.strptime(str(months), '%Y-%m-%d')))
today_start = yesterday_end + 1
today_end = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
datedict = {
    'month': [utc(month_start), utc(today_end)],
    'week': [utc(weekday_start), utc(today_end)],
    'total': ['2018-11-25', utc(today_end)],
    'today': [utc(today_start), utc(today_end)],
    'yesday': [utc(yesterday_start), utc(yesterday_end)],
    'months': [utc(months_start), utc(today_end)],
    'day_begin': [day_begin, day_begin],
    'day_end': [day_end, day_end],
     }

def time_stamp():
    # 获取各种时间戳
    tday = datetime.date.today()
    yesterday = tday - datetime.timedelta(days=1)
    tomorrow = tday + datetime.timedelta(days=1)
    weekday = tday - datetime.timedelta(days=6)
    month = tday - datetime.timedelta(days=29)
    months = tday - datetime.timedelta(days=89)
    yesterday_start = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
    yesterday_end = int(time.mktime(time.strptime(str(tday), '%Y-%m-%d'))) - 1
    weekday_start = int(time.mktime(time.strptime(str(weekday), '%Y-%m-%d')))
    month_start = int(time.mktime(time.strptime(str(month), '%Y-%m-%d')))
    months_start = int(time.mktime(time.strptime(str(months), '%Y-%m-%d')))
    today_start = yesterday_end + 1
    today_end = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
    datedict = {
        'month': [utc(month_start), utc(today_end)],
        'week': [utc(weekday_start), utc(today_end)],
        'total': ['2018-11-25', utc(today_end)],
        'today': [utc(today_start), utc(today_end)],
        'yesday': [utc(yesterday_start), utc(yesterday_end)],
        'months': [utc(months_start), utc(today_end)],
        'day_begin': [day_begin, day_begin],
        'day_end': [day_end, day_end],
    }
    return datedict

class FunctionObject(object):
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
                if take[0] == id['id']:
                    self.splilist[key]['tabkegoods'] = self.takeorder[takekey][1]
                    break
        for buykey, take in enumerate(self.buyorder):
            for key, id in enumerate(self.splilist):
                if take[0] == id['id']:
                    self.splilist[key]['purchase'] = self.buyorder[buykey][1]
                    self.splilist[key]['total'] = to_string(self.buyorder[buykey][2])
                    break
        dict = {'data': self.splilist[(self.pages - 1) * self.numberbars:self.pages * self.numberbars]}
        totalnum = len(self.splilist)
        dict['totalnum'] = totalnum
        data = {'data': dict, "errmsg": "成功", "errno": "0"}
        return data

    def startend(self, start_day, end_day):
        self.start_day = start_day
        self.end_day = end_day
        s_time = time.mktime(time.strptime(self.start_day, '%Y-%m-%d'))
        e_time = time.mktime(time.strptime(self.end_day, '%Y-%m-%d'))
        if (float(s_time) > float(e_time)):
            return HttpResponse(json.dumps({"errmsg": "订单统计时间顺序不对", "errno": "4001"}), content_type="application/json")
        return self.start_day, self.end_day


#时间戳转日期
def localutc(local_st):
    utc_st = time.localtime(local_st)
    result = time.strftime("%Y-%m-%d %H:%M:%S", utc_st)
    return result

#时间戳转日期
def yearmonthday(local_st):
    utc_st = time.localtime(local_st)
    result = time.strftime("%Y-%m-%d", utc_st)
    return result

#时间戳转日期
def monthtime(local_st):
    utc_st = time.localtime(local_st)
    result = time.strftime("%Y-%m", utc_st)
    return result

#时间戳转日期
def yeartime(local_st):
    utc_st = time.localtime(local_st)
    result = time.strftime("%Y", utc_st)
    return result

#时间戳转日期减去3小时
def userutc(local_st):
    usertime = datetime.datetime.strptime(local_st, "%Y-%m-%d %H:%M:%S")
    data = time.mktime(usertime.timetuple())-10800
    utc_st = time.localtime(data)
    result = time.strftime("%Y-%m-%d %H:%M:%S", utc_st)
    return result


#29100   633600
#代言券 已入账时间设置
def commission_price(local_st):
    utc_st = time.localtime(local_st - 633600)
    result = time.strftime("%Y-%m-%d %H:%M:%S", utc_st)
    return result

#字符串转时间戳
def str_time_stamp(data):
    timeArray = time.strptime(data, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


#字符串转时间戳
def str_time_stamp_date(data):
    timeArray = time.strptime(data, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp



