'''
/**
* Copyright ©2019-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 合颌科技（北京）有限公司 版权所有
*
*/
'''
from django.db import connections
from django.http import HttpResponse
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reports.utils.response_code import RET


class GuRui(APIView):

    def get(self, request):
        # name = request.GET.get('user')
        name = 'BOSS'
        cursor = connections['default'].cursor()
        # 模糊查询返回用户地址，名字
        try:
            cursor.execute(
                "select name,id from jld_user where name LIKE '%" + name + "%'"
            )
            receive = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": RET.MDBERR, "errno": RET.DBERR}))
        if receive:
            list = []
            for info in receive:
                dict = {
                    'name': info[0],
                    'useraddr': info[1],
                }
                list.append(dict)
            data = {'data': list, "errmsg": RET.MDBERR, "errno": status.HTTP_200_OK}
            return HttpResponse(json.dumps(data))

class GuRui1(APIView):

    def post(self, request):
        name = request.POST.get('user')
        cursor = connections['default'].cursor()
        print(request.data)
        # 模糊查询返回用户地址，名字
        try:
            cursor.execute(
                "select name,id from jld_user where name LIKE '%" + name + "%'"
            )
            receive = cursor.fetchall()
        except:
            return HttpResponse(json.dumps({"errmsg": RET.MDBERR, "errno": RET.DBERR}))
        if receive:
            list = []
            for info in receive:
                dict = {
                    'name': info[0],
                    'useraddr': info[1],
                }
                list.append(dict)
            data = {'data': list, "errmsg": RET.MDBERR, "errno": status.HTTP_200_OK}
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps({'9':0}))
