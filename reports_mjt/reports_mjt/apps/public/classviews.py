'''
/**
* Copyright ©2017-2019 Beijing HeXinHuiTong Co.,Ltd
* All Rights Reserved.
*
* 2017-2019 北京和信汇通科技开发有限公司 版权所有
*
*/
'''
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import UserSerializers, ManageSerializers, GoodsSerializers
from .models import UserData, ManageOrm, GoodsOrm


#接收rest-framework对象
class ManageData(ReadOnlyModelViewSet):
    global true
    true = True
    global null
    null = ''
    global false
    false = False
    @action(methods=['POST'], detail=False)
    def publico(self, request):
        distrdict = {
            '0': UserSerialiZers().funcdata(request),
            '1': ManageSerialiZers().funcdata(request),
            '2': AllManageSerialiZers().funcdata(request),
            '3': GoodsSerialiZers().funcdata(request),
        }
        return distrdict.get(request.data.get('type'), UserSerialiZers().funcdata(request))

#模糊查询用户名
class UserSerialiZers(ReadOnlyModelViewSet):
    serializer_class = UserSerializers
    queryset = UserData.objects.all()
    def funcdata(self, request):
        username = request.data.get('username', ['zhaomemgqiqizai'])
        user = UserData.objects.filter(name__contains=username)
        serializer = UserSerializers(user, context={'request': request}, many=True)
        return Response(serializer.data)

#模糊查询商家名
class ManageSerialiZers(ReadOnlyModelViewSet):
    serializer_class = ManageSerializers
    queryset = ManageOrm.objects.all()
    def funcdata(self, request):
        orgname = request.data.get('orgname', ['zhaomemgqiqizai'])
        org = ManageOrm.objects.filter(name__contains=orgname)
        serializer = ManageSerializers(org, context={'request': request}, many=True)
        return Response(serializer.data)

#产讯所有商家
class AllManageSerialiZers(ReadOnlyModelViewSet):
    serializer_class = ManageSerializers
    queryset = ManageOrm.objects.all()
    def funcdata(self, request):
        allorg = ManageOrm.objects.filter(name__isnull=False)
        serializer = ManageSerializers(allorg, context={'request': request}, many=True)
        return Response(serializer.data)

#查询商家所有商品
class GoodsSerialiZers(ReadOnlyModelViewSet):
    serializer_class = GoodsSerializers
    queryset = GoodsOrm.objects.all()
    def funcdata(self, request):
        foreign_key = request.data.get('foreign_key', ['zhaomemgqiqizai'])
        goods = GoodsOrm.objects.filter(foreign_key=foreign_key, name__isnull=False)
        serializer = GoodsSerializers(goods, context={'request': request}, many=True)
        return Response(serializer.data)



