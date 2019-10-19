from django_redis import get_redis_connection

from reports_mjt.utils.data_select import localutc
from reports_mjt.utils.ormdate import ormdate


class APIAuthParameter(object):

    def __init__(self, request):
        global null
        null = ''
        global false
        false = False
        global true
        true = True
        self.request = request
        self.start = request.GET.get('start', ormdate()['startstamp'])
        self.end = request.GET.get('end', ormdate()['endstamo'])
        self.foreign_key = request.GET.get('foreign_key')
        self.goodsid = request.GET.get('goodsid')
        self.manager_id = request.GET.get('manager_id', 'manager_id')
        self.type = request.GET.get('type')
        self.useraddr = request.GET.get('useraddr')
        self.data = request.GET.get('param')
        self.pages = int(request.GET.get('page', 1))
        self.numberbars = int(request.GET.get('numberbars', 10))
        self.state = request.GET.get('state', 'undefined')
        if self.data:
            self.zytype = eval(self.data)['type']
    def getRedis(self):
        tokendata = eval(get_redis_connection('default').get(eval(self.data)['token']))
        token_active_data = get_redis_connection('default').get('peesell:peesellGoods')
        datadict = {
            'userid': tokendata['id'],
            'pageno': eval(self.data).get('pageNo', '1'),
            'pagesize': eval(self.data).get('pageSize', '10'),
            'type': eval(self.data).get('type'),
            'token_active_data': token_active_data,
        }

        return datadict

    def manage(self):

        return {'type': self.type,
                'startTime': localutc(float(self.start)),
                'endTime': localutc(float(self.end)),
                'manager_id': self.manager_id,
                'pages': self.pages,
                'numberbars': self.numberbars,
                'start': self.start,
                'end': self.end,
                'state': self.state,
                }


    def reports(self):

        return {'type': self.type,
                'startTime': localutc(float(self.start)),
                'endTime': localutc(float(self.end)),
                'manager_id': self.manager_id,
                'pages': self.pages,
                'numberbars': self.numberbars,
                'start': self.start,
                'end': self.end,
                'foreign_key': self.foreign_key,
                'goodsid': self.goodsid,
                'useraddr': self.useraddr,
                }

    def finance(self):

        return {
                'startTime': localutc(float(self.start)),
                'endTime': localutc(float(self.end)),
                'pages': self.pages,
                'numberbars': self.numberbars,
                'date': self.start,
                'userid': self.useraddr,
                }