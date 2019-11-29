import xlrd
import time
from xlrd import open_workbook # xlrd用于读取xld
import MySQLdb
import uuid

workbook = open_workbook(r'C:\Users\zl\Downloads\初诊挂号（前台）_20191129170823.xlsx')  # 打开xls文件
worksheet = xlrd.open_workbook(r'C:\Users\zl\Downloads\初诊挂号（前台）_20191129170823.xlsx')
sheet_names= worksheet.sheet_names()
sheet = workbook.sheet_by_index(0)  # 根据sheet索引读取sheet中的所有内容

db = MySQLdb.connect("47.104.159.115", "root", "Gurui190916", "dev", charset='utf8' )
cursor = db.cursor()
crate_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# print(sheet.nrows)  # sheet的名称、行数、列数

for sheet_name in sheet_names:
    sheet2 = worksheet.sheet_by_name(sheet_name)
    for i in range(sheet.nrows):
        rows = sheet2.row_values(i) # 获取第四行内容
        print(rows)



