import json
from datetime import date
import decimal
import time
from datetime import datetime


def to_string(obj):
    # if isinstance(obj, datetime.datetime):
    #     return obj.strftime('%Y-%m-%d %H:%M:%S')
    # elif isinstance(obj, datetime.date):
    #     return obj.strftime('%Y-%m-%d')
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj

def to_int(obj):
    # if isinstance(obj, datetime.datetime):
    #     return obj.strftime('%Y-%m-%d %H:%M:%S')
    # elif isinstance(obj, datetime.date):
    #     return obj.strftime('%Y-%m-%d')
    if isinstance(obj, decimal.Decimal):
        return int(obj)
    return obj


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

    def str_time_stamp(self, obj):
        if isinstance(obj, datetime):
            return time.mktime(obj.timetuple())
        elif isinstance(obj, date):
            return time.mktime(obj.timetuple())
        else:
            return json.JSONEncoder.default(self, obj)


def strinter(data):
    datetime_object = datetime.strptime(data)
    return datetime_object.date()

# def utclocal(utc_st):
#     """UTC时间转本地时间（+8: 00）"""
#     now_stamp = time.time()
#     local_time = datetime.datetime.fromtimestamp(now_stamp)
#     utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
#     offset = local_time - utc_time
#     local_st = utc_st + offset
#     return local_st



def date_sort1(x):
    ls=list(x)
#用了冒泡排序来排序，其他方法效果一样
    for j in range(len(ls)-1):
        for i in range(len(ls)-j-1):
            lower=ls[i][0].split('-')
            upper=ls[i+1][0].split('-')
            for s in range(3):
                if int(lower[s])<int(upper[s]):
                    ls[i],ls[i+1]=ls[i+1],ls[i]
                    break
                elif int(lower[s])>int(upper[s]):
                    break
    return ls


def date_quicksort(array):
    less = []
    greater = []
    if len(array) <= 1:
        return array
    pivot = array.pop()
    for x in array:
        if x[1] >= pivot[1]:
            less.append(x)
        else:
            greater.append(x)
    return date_quicksort(less) + [pivot] + date_quicksort(greater)
