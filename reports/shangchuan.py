# -*- coding:utf-8 -*-
import oss2
accessID = "LTAI4FvgoPWA1Sgiq348gmWJ"
accessKey = "6GS84UOhugMu8es6q2WJN6OZl55Vh5"
endpoint = "oss-cn-qingdao.aliyuncs.com"
bucketName = "idso-image"
from datetime import datetime
import requests
import json
import time
import MySQLdb
def func(data):
    date_ = datetime.strptime(data,"%Y-%m-%dT%H:%M:%S.%fZ")
    return date_

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



# 创建oss链接
auth = oss2.Auth(accessID, accessKey)
bucket = oss2.Bucket(auth, endpoint, bucketName)

conn = MySQLdb.connect(host="47.104.159.115", port=3306, user="root", passwd="Gurui190916", db="dev", charset="utf8")
cursor = conn.cursor()


def get_image(data):
    # 请求图片，获取返回的返回数据对象
    for key, url in enumerate(data['_widget_1566744478305']):
        print(1, data['_widget_1566744478305'])
        response = requests.get(url['url'])
        # 判断请求返回状态是否为200
        if response.status_code == 200:
            # 图片在oss上的保存路径
            file_path = data['_widget_1568908048667']+'intraoral' +str(key) + ".jpg"
            try:
                # 上传oss
                bucket.put_object(file_path, response)
            except Exception as e:
                print(e)
            # cursor.execute("select intraoral from user_therapy where userid = '"+data['_widget_1568908048667']+"'")
            # intraoral = cursor.fetchall()
            # if intraoral[0][0] is None:
            #     sql = "update user_therapy set intraoral = '" + file_path + "' where userid = '" + data[
            #         '_widget_1568908048667'] + "'"
            #
            #     try:
            #         cursor.execute(sql)
            #         conn.commit()
            #     except Exception as e:
            #         print("数据库插入失败,失败原因为:", e)
            #         print("失败语句为:", sql)
            #
            # # 写入oss成功后保存到mysql表
            # sql = "update user_therapy set intraoral=CONCAT('" + file_path + "',intraoral) where userid = '" + data['_widget_1568908048667'] + "'"
            # try:
            #     # 执行mysql插入语句
            #     cursor.execute(sql)
            #     # 提交事务
            #     conn.commit()
            # except Exception as e:
            #     print("数据库插入失败,失败原因为:", e)
            #     print("失败语句为:", sql)

    for key, url in enumerate(data['_widget_1566744478320']):
        print(2, data['_widget_1566744478320'])
        response = requests.get(url['url'])
        # 判断请求返回状态是否为200
        if response.status_code == 200:

            file_path = data['_widget_1568908048667'] + 'treatment_sheet' + str(key) + ".jpg"
            try:
                # 上传oss
                bucket.put_object(file_path, response)
            except Exception as e:
                print(e)
            # cursor.execute(
            #     "select treatment_sheet from user_therapy where userid = '" + data['_widget_1568908048667'] + "'")
            # intraoral = cursor.fetchall()
            # if intraoral[0][0] is None:
            #     sql = "update user_therapy set treatment_sheet = '" + file_path + "' where userid = '" + data[ '_widget_1568908048667'] + "'"
            #
            #     try:
            #         # 执行mysql插入语句
            #         cursor.execute(sql)
            #         # 提交事务
            #         conn.commit()
            #     except Exception as e:
            #         print("数据库插入失败,失败原因为:", e)
            #         print("失败语句为:", sql)
            #
            # # 写入oss成功后保存到mysql表
            # sql = "update user_therapy set treatment_sheet=CONCAT('" + file_path + "',treatment_sheet) where userid = '" +  data['_widget_1568908048667'] + "'"
            # try:
            #     # 执行mysql插入语句
            #     cursor.execute(sql)
            #     # 提交事务
            #     conn.commit()
            # except Exception as e:
            #     print("数据库插入失败,失败原因为:", e)
            #     print("失败语句为:", sql)

    for key, url in enumerate(data['_widget_1566744478170']):
        print(3, data['_widget_1566744478170'])
        response = requests.get(url['url'])
        # 判断请求返回状态是否为200
        if response.status_code == 200:

            file_path = data['_widget_1568908048667'] + 'x_rays' + str(key) + ".jpg"
            try:
                # 上传oss
                bucket.put_object(file_path, response)
            except Exception as e:
                print(e)
            # cursor.execute(
            #     "select x_rays from user_therapy where userid = '" + data['_widget_1568908048667'] + "'")
            # intraoral = cursor.fetchall()
            # if intraoral[0][0] is None:
            #     sql = "update user_therapy set x_rays = '" + file_path + "' where userid = '" + data[ '_widget_1568908048667'] + "'"
            #
            #     try:
            #         # 执行mysql插入语句
            #         cursor.execute(sql)
            #         # 提交事务
            #         conn.commit()
            #     except Exception as e:
            #         print("数据库插入失败,失败原因为:", e)
            #         print("失败语句为:", sql)
            #
            # # 写入oss成功后保存到mysql表
            # sql = "update user_therapy set x_rays=CONCAT('" + file_path + "',x_rays) where userid = '" + data['_widget_1568908048667'] + "'"
            # try:
            #     # 执行mysql插入语句
            #     cursor.execute(sql)
            #     # 提交事务
            #     conn.commit()
            # except Exception as e:
            #     print("数据库插入失败,失败原因为:", e)
            #     print("失败语句为:", sql)

if __name__ == '__main__':
    # 图片链接
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
        get_image(v)

