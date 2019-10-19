from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer

from public.search_indexes import SKUIndex
from .models import UserData, ManageOrm, GoodsOrm, EleUserData


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'name']

class UserSerializers(serializers.Serializer):
    name = serializers.CharField(label='名字', max_length=64)
    id = serializers.CharField(label='名字', max_length=255)


class ManageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageOrm
        fields = ['id', 'foreign_key', 'name', 'business_license', 'short_name']

class ManageSerializers(serializers.Serializer):
    name = serializers.CharField(label='名字', max_length=64)
    short_name = serializers.CharField(label='名字', max_length=64)
    id = serializers.CharField(label='名字', max_length=255)
    foreign_key = serializers.CharField(label='名字', max_length=255)
    business_license = serializers.CharField(label='名字', max_length=255)


class GoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsOrm
        fields = ['id', 'name']

class GoodsSerializers(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)




class SKUSerializer(serializers.ModelSerializer):
    """
    SKU序列化器
    """

    class Meta:
        model = EleUserData
        fields = ['id', 'name', 'city']


class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """
    object = SKUSerializer(read_only=True)

    class Meta:
        index_classes = [SKUIndex]
        fields = ('text', 'object')