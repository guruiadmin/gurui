from rest_framework import serializers

from public.models import OrgActivity


class ManageActivite(serializers.ModelSerializer):
    '''取商家活动数据'''

    # start = serializers.CharField(label='开始时间')
    # end = serializers.CharField(label='结束时间')
    # page = serializers.IntegerField(label='页数', min_value=1)
    # num = serializers.IntegerField(label='没页数量', min_value=1)
    # type = serializers.IntegerField(label='类型', max_value=3)

    class Meta:
        model = OrgActivity
        fields = ('id', 'orgAddr', 'goodsAddr', 'startRob', 'stopRob', 'robNum', 'debrisNum', 'times', 'participants', 'returnRobNum')