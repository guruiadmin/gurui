from datetime import datetime

import requests
import json
import time
import xlrd
import time
from xlrd import open_workbook # xlrd用于读取xld
import MySQLdb
def func(data):
    date_ = datetime.strptime(data,"%Y-%m-%dT%H:%M:%S.%fZ")
    return date_

# workbook = open_workbook(r'C:\Users\zl\Downloads\合颌科技(北京)有限公司-通讯录.xlsx')  # 打开xls文件
# worksheet = xlrd.open_workbook(r'C:\Users\zl\Downloads\合颌科技(北京)有限公司-通讯录.xlsx')
# sheet_names= worksheet.sheet_names()
# sheet = workbook.sheet_by_index(0)  # 根据sheet索引读取sheet中的所有内容

db = MySQLdb.connect("47.104.159.115", "root", "Gurui190916", "dev", charset='utf8' )
cursor = db.cursor()

class APIUtils:

    WEBSITE = "https://www.jiandaoyun.com"
    RETRY_IF_LIMITED = True

    # 构造函数
    def __init__(self, appId, entryId, api_key):
        self.url_get_widgets = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/widgets'
        self.url_get_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data'
        self.url_retrieve_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_retrieve'
        self.url_update_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_update'
        self.url_create_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_create'
        self.url_delete_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_delete'
        self.api_key = api_key

    # 带有认证信息的请求头
    def get_req_header(self):
        return {
            'Authorization': 'Bearer ' + self.api_key,
            'Content-Type': 'application/json;charset=utf-8'
        }

    # 发送http请求
    def send_request(self, method, request_url, data):
        headers = self.get_req_header()
        if method == 'GET':
            res = requests.get(request_url, params=data, headers=headers, verify=False)
        if method == 'POST':
            res = requests.post(request_url, data=json.dumps(data), headers=headers, verify=False)
        result = res.json()
        if res.status_code >= 400:
            if result['code'] == 8303 and APIUtils.RETRY_IF_LIMITED:
                # 5s后重试
                time.sleep(5)
                return self.send_request(method, request_url, data)
            else:
                raise Exception('请求错误！', result)
        else:
            return result

    # 获取表单字段
    def get_form_widgets(self):
        result = self.send_request('POST', self.url_get_widgets, {})
        return result['widgets']

    # 根据条件获取表单中的数据
    def get_form_data(self, dataId, limit, fields, data_filter):
        result = self.send_request('POST', self.url_get_data, {
            'data_id': dataId,
            'limit': limit,
            'fields': fields,
            'filter': data_filter
        })
        return result['data']

    # 获取表单中满足条件的所有数据
    def get_all_data(self, fields, data_filter):
        form_data = []

        # 递归取下一页数据
        def get_next_page(dataId):
            data = self.get_form_data(dataId, 100, fields, data_filter)
            if data:
                for v in data:
                    form_data.append(v)
                dataId = data[len(data) - 1]['_id']
                get_next_page(dataId)
        get_next_page('')
        return form_data

if __name__ == '__main__':
    appId = '5d35065db27c520aed699da7'
    entryId = '5d5eb5477d036e7eb5c2a99d'
    api_key = 'RqJ6Lk3p5bdim1p6XdSYeqaolxNvP4Ah'
    api = APIUtils(appId, entryId, api_key)

    # 按条件获取表单数据
    data = api.get_form_data('', 100, ['_widget_1528252846720', '_widget_1528252846801'], {
        'rel': 'and',
        'cond': [{
            'field': '_widget_1528252846720',
            'type': 'text',
            'method': 'empty'
        }]
    })

    # 获取所有表单数据
    form_data = api.get_all_data([], {})
    for v in form_data:
        print(v)
        # cursor.execute("select name from user WHERE userid = '" + v['_widget_1568908048667'] + "'")
        # sql1 = cursor.fetchall()
        # if not sql1:
        #     cursor.execute("select docker_id from doctor WHERE name = '" + v['_widget_1569164862566']['name'] + "'")
        #     docker_id = cursor.fetchall()
        #     if not docker_id:
        #         docker_id = (('',),)
        #     cursor.execute("select pm_id from reception_pm WHERE name = '" + v['_widget_1569164862538']['name'] + "'")
        #     pm_id = cursor.fetchall()
        #     if not pm_id:
        #         pm_id = (('',),)
        #     sql = "INSERT INTO user(userid, name, create_time,docker_id,pm_id) VALUES ('{}','{}','{}','{}','{}')".format(v['_widget_1568908048667'],v['_widget_1566487961449'], func(v['_widget_1566487961562']), v['_widget_1569164862566']['name'], v['_widget_1569164862538']['name'])

        # cursor.execute("select userid from user_therapy WHERE userid = '" + v['_widget_1568908048667'] + "'")
        # sql1 = cursor.fetchall()
        # if not sql1:
        #     sql = "INSERT INTO user_therapy(userid) VALUES ('{}')".format(v['_widget_1568908048667'])
        #     cursor.execute(sql)
        #     # 提交事务
        #     db.commit()
