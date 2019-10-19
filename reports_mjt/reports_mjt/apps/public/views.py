'''
/**
* Copyright ©2017-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 北京和信汇通科技开发有限公司 版权所有
*
*/
'''
import json

from django.db.models import Q
from django.db import connections
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import View
#虎为百兽尊，罔敢触其怒。惟有父子情，一步一回顾。
from drf_haystack.viewsets import HaystackViewSet

from public.models import UserData, ManageOrm, GoodsOrm, EleUserData

#index页面
from public.serializers import SKUIndexSerializer


class ManageData(View):

    def get(self, request):

        foreign_key = request.GET.get('foreign_key')
        name = request.GET.get('name')
        type = request.GET.get('type')
        if not type:
            return HttpResponse(json.dumps({"errmsg": "type参数缺失","errno": "4103"}), content_type="application/json")

        # 商家查询
        if type == '0':
            try:
                managename = ManageOrm.objects.filter(name__isnull=False)
            except UserData.DoesNotExist:
                return HttpResponse(status=404)
            managenamelist = []
            for name in managename:
                data = {
                    'orgname': name.name,
                    'id': name.id,
                    'foreign_key': name.foreign_key,
                }
                managenamelist.append(data)
            return JsonResponse({'data': managenamelist, "errmsg": "成功", "errno": "0"}, safe=False)
        # 商户名下所有商品
        elif type == '1':
            if not foreign_key:
                return HttpResponse(json.dumps({"errmsg": "商户名下所有商品", "errno": "4103"}), content_type="application/json")
            try:
                goodsname = GoodsOrm.objects.filter(Q(foreign_key=foreign_key) & Q(name__isnull=False))
            except UserData.DoesNotExist:
                return HttpResponse(status=404)
            goodsnamelist = []
            for name in goodsname:
                data = {
                    'goodsname': name.name,
                    'id': name.id,
                    'foreign_key': name.foreign_key,
                }
                goodsnamelist.append(data)
            return JsonResponse({'data': goodsnamelist, "errmsg": "成功", "errno": "0"}, safe=False)
        # 商家模糊查询
        elif type == '2':
            if not name:
                return HttpResponse(json.dumps({"errmsg": "cc", "errno": "4103"}), content_type="application/json")
            try:
                managename = ManageOrm.objects.filter(name__contains=name)
            except UserData.DoesNotExist:
                return HttpResponse(status=404)
            managenamelist = []
            for name in managename:
                data = {
                    'orgname': name.name,
                    'id': name.id,
                    'foreign_key': name.foreign_key,
                }
                managenamelist.append(data)
            return JsonResponse({'data': managenamelist, "errmsg": "成功", "errno": "0"}, safe=False)
        # 用户名模糊查询
        elif type == '3':
            if not name:
                return HttpResponse(json.dumps({"errmsg": "用户名模糊查询", "errno": "4103"}), content_type="application/json")
            try:
                username = UserData.objects.filter(name__contains=name)
            except UserData.DoesNotExist:
                return HttpResponse(status=404)
            usernamelist = []
            for name in username:
                data = {
                    'username': name.name,
                    'id': name.id,
                }
                usernamelist.append(data)
            return JsonResponse({'data': usernamelist, "errmsg": "成功", "errno": "0"}, safe=False)


        else:
            return HttpResponse(json.dumps({"errmsg": "type参数错误", "errno": "4001"}), content_type="application/json")

class SKUSearchViewSet(HaystackViewSet):  # HaystackViewSet继承了RetrieveModelMixin, ListModelMixin, ViewSetMixin, HaystackGenericAPIView，所以可以查一条或多条数据
    """
    SKU搜索
    HaystackViewSet： 查一条，查多条
    """
    index_models = [EleUserData]
    serializer_class = SKUIndexSerializer

