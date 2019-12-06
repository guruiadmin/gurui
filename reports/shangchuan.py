# -*- coding:utf-8 -*-

import requests
import oss2
import MySQLdb

accessID = "LTAI4FvgoPWA1Sgiq348gmWJ"
accessKey = "6GS84UOhugMu8es6q2WJN6OZl55Vh5"
# endpoint = "oss-cn-qingdao-internal.aliyuncs.com"
endpoint = "oss-cn-qingdao.aliyuncs.com"
bucketName = "idso"

# 创建oss链接
# auth = oss2.Auth(accessID, accessKey)
# bucket = oss2.Bucket(auth, endpoint, bucketName)

# 创建mysql链接
conn = MySQLdb.connect(host="47.104.159.115", port=3306, user="root", passwd="Gurui190916", db="dev", charset="utf8")
cur = conn.cursor()


def get_image():
    # 请求图片，获取返回的返回数据对象
    input = requests.get("https://files.jiandaoyun.com/FmMZTnsRcwwNg9TKXBF14LXw6sfv?attname=FmMZTnsRcwwNg9TKXBF14LXw6sfv.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:x-_Ko8QOBSjr2d0MMMypfr4AlcM=")
    auth = oss2.Auth("LTAI4FvgoPWA1Sgiq348gmWJ", "6GS84UOhugMu8es6q2WJN6OZl55Vh5")
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, "oss-cn-qingdao.aliyuncs.com", "idso")

    # requests.get返回的是一个可迭代对象（Iterable），此时Python SDK会通过Chunked Encoding方式上传。
    mm = bucket.put_object("idso", input)
    print(mm, auth, bucket)

if __name__ == '__main__':
    # 图片链接
    image_url = {'creator': {'username': '24523448511179376', '_id': '5c96e4b6c9c631ec08cce1e6', 'name': '郭爽'}, 'updater': {'username': '2719686300890108', '_id': '5d7aa3fd15f6766502990a82', 'name': '汪琦'}, 'deleter': None, 'createTime': '2019-12-02T07:11:07.714Z', 'updateTime': '2019-12-02T14:08:22.834Z', 'deleteTime': None, '_widget_1566487961449': '武治远', '_widget_1568908048667': '105419120202428', '_widget_1566487961562': '2019-12-02T07:10:33.000Z', '_widget_1569164862538': {'username': '2934611409677431', '_id': '5d6872f1cad69f210db91479', 'name': '刘敏'}, '_widget_1569164862566': {'username': '2719686300890108', '_id': '5d7aa3fd15f6766502990a82', 'name': '汪琦'}, '_widget_1566898495167': '105419120202428武治远20191202', '_widget_1566560693539': 'c.洗牙', '_widget_1566901073003': ['C洗牙', 'B补牙'], '_widget_1566744478305': [{'name': 'FmMZTnsRcwwNg9TKXBF14LXw6sfv.jpeg', 'size': 445471, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/FmMZTnsRcwwNg9TKXBF14LXw6sfv?attname=FmMZTnsRcwwNg9TKXBF14LXw6sfv.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:x-_Ko8QOBSjr2d0MMMypfr4AlcM='}, {'name': 'FpCy3QHY_oZZTdtetZxlFGGN2IgK.jpeg', 'size': 205129, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/FpCy3QHY_oZZTdtetZxlFGGN2IgK?attname=FpCy3QHY_oZZTdtetZxlFGGN2IgK.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:Id-kbH6PpnP-6aWptQdqSNOVWQc='}, {'name': 'FgzBkp8b2xFRI2QpCn5iMKwiVJ4H.jpeg', 'size': 322342, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/FgzBkp8b2xFRI2QpCn5iMKwiVJ4H?attname=FgzBkp8b2xFRI2QpCn5iMKwiVJ4H.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:vSSv_nwVpEf5bsvpQ81ZdU0_mm4='}, {'name': 'Fo-k4LbYOBdSUtHdaBp3jVvOeDXM.jpeg', 'size': 320736, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/Fo-k4LbYOBdSUtHdaBp3jVvOeDXM?attname=Fo-k4LbYOBdSUtHdaBp3jVvOeDXM.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:F2GTu4w7lg8Zb7dm66NGE9L1hf8='}, {'name': 'FgOCGHCDfMTkpfDzNmlKwA6suIIu.jpeg', 'size': 546238, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/FgOCGHCDfMTkpfDzNmlKwA6suIIu?attname=FgOCGHCDfMTkpfDzNmlKwA6suIIu.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:ZR_kn2dsdZykgS-ce2bUy1uAtXA='}, {'name': 'FueKo7g821Wc1560sP7CWupHepLr.jpeg', 'size': 538569, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/FueKo7g821Wc1560sP7CWupHepLr?attname=FueKo7g821Wc1560sP7CWupHepLr.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:Jhnfr308-XJJjIIX1fzRfxWoOMs='}], '_widget_1566744478170': [{'name': 'wuzhiyuan.jpg', 'size': 54308, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/FnX4Vk07HS44apor87D5U8D9ASP3?attname=wuzhiyuan.jpg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:99nXhSF6-pJOrBlab_LMHY3GrqU='}], '_widget_1566744478320': [{'name': 'FvxzsEmMeC3OIsF9q6FX-Vb1Sn_G.jpeg', 'size': 2901277, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/FvxzsEmMeC3OIsF9q6FX-Vb1Sn_G?attname=FvxzsEmMeC3OIsF9q6FX-Vb1Sn_G.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:usfMvr3i1B6xvrsmZMEWPWTOg-s='}, {'name': 'FnPb7P0jVK7QHDQP4XtRNj7TW5qw.jpeg', 'size': 2462245, 'mime': 'image/jpeg', 'url': 'https://files.jiandaoyun.com/FnPb7P0jVK7QHDQP4XtRNj7TW5qw?attname=FnPb7P0jVK7QHDQP4XtRNj7TW5qw.jpeg&e=1576108799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:IOpnQsmhRuxyMNhDHFz61EzJ3w8='}], '_widget_1575297682464': [], '_widget_1566745430087': '是', '_widget_1568778846799': '', '_widget_1566745430108': '是', '_widget_1568783041304': '', '_widget_1575267956902': '2019-12-08T16:00:00.000Z', '_widget_1575267956914': 'C洗牙', '_widget_1575267956886': [], '_widget_1575267957196': [], '_widget_1569027533229': '', '_id': '5de4b90b4ae0ed00068cff0d', 'appId': '5d35065db27c520aed699da7', 'entryId': '5d5eb5477d036e7eb5c2a99d'}
    get_image()

