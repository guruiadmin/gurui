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
from django_redis import get_redis_connection
import urllib.parse
import urllib.request

from public.models import Jlduser_Source
urldata = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx516f09ef989c1298&secret=a84cbe0a9cc547332352e0ea4f3fff2d'


class LogisticsApi(View):
    def get(self, request):
        global null
        null = ''
        global false
        false = False
        # 获取搜索类型
        token = request.GET.get('token')
        order_id = request.GET.get('order_id')
        redis_conn = get_redis_connection('default')
        try:
            tokendata = eval(redis_conn.get(token))
        except:
            return HttpResponse(json.dumps({"errmsg": "token已过期", "errno": "4001"}), content_type="application/json")
        userid = tokendata['unionid']
        try:
            data = Jlduser_Source.objects.filter(user_union_id=userid, openid_source=1)
        except Jlduser_Source.DoesNotExist:
            return HttpResponse(status=404)
        openid = None
        for info in data:
            openid = info.user_open_id
        getdict = urllib.parse.urlencode({'grant_type': 'client_credential', 'appid': 'wx516f09ef989c1298', 'secret': 'a84cbe0a9cc547332352e0ea4f3fff2d'})
        """发送get请求"""
        response = urllib.request.urlopen('https://api.weixin.qq.com/cgi-bin/token?%s' % getdict)
        html =eval(response.read())
        print(html)
        # """发送post请求"""
        posturl = 'https://api.weixin.qq.com/cgi-bin/express/business/path/get?access_token=' + html['access_token']
        print(posturl)
        values = {"order_id": "6376204118901", "openid": "oKoCW5J1aCMErYzrFX_qImGOaP4w", "delivery_id": "YUNDA", "waybill_id": "3906571451266"}
        print(values)
        data = urllib.parse.urlencode(values).encode('utf-8')
        req = urllib.request.Request(posturl, data)
        result = urllib.request.urlopen(req).read()
        data = {'data': eval(result), "errmsg": "成功", "errno": "0"}
        return HttpResponse(json.dumps(data), content_type="application/json")




