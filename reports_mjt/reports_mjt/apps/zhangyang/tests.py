from django.http import HttpResponse
from django.test import TestCase

# Create your tests here.
from abc import ABCMeta, abstractmethod
import json
from django_redis import get_redis_connection


class Payment(metaclass=ABCMeta):
    # 抽象产品
    @abstractmethod
    def funcdata(self, money):
        pass

class PaymentFactory(metaclass=ABCMeta):
    # 抽象工厂
    @abstractmethod
    def create_payment(self, datacursor):
        global null
        null = ''
        global false
        false = False
        global true
        true = True


        try:
            tokendata = eval(get_redis_connection('default').get(datacursor['token']))
        except:
            return HttpResponse(json.dumps({"errmsg": "token已过期", "errno": "401"}), content_type="application/json")
        datadict = {
            'userid': tokendata['id'],
            'pageNo': datacursor.get('pageNo', '1'),
            'pageSize': datacursor.get('pageSize', '10'),
            'type': datacursor.get('type'),
        }
        return datadict
