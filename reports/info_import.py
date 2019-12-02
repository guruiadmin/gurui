import xlrd
import time
from xlrd import open_workbook # xlrd用于读取xld
import MySQLdb
import uuid

workbook = open_workbook(r'C:\Users\zl\Downloads\合颌科技(北京)有限公司-通讯录.xlsx')  # 打开xls文件
worksheet = xlrd.open_workbook(r'C:\Users\zl\Downloads\合颌科技(北京)有限公司-通讯录.xlsx')
sheet_names= worksheet.sheet_names()
sheet = workbook.sheet_by_index(0)  # 根据sheet索引读取sheet中的所有内容

db = MySQLdb.connect("47.104.159.115", "root", "Gurui190916", "dev", charset='utf8' )
cursor = db.cursor()
crate_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
sheet1= workbook.sheet_by_name('员工信息表1')  # 根据sheet名称读取sheet中的所有内容
# print(sheet.nrows)  # sheet的名称、行数、列数


for sheet_name in sheet_names:
    sheet2 = worksheet.sheet_by_name(sheet_name)
    for i in range(sheet.nrows):
        rows = sheet2.row_values(i) # 获取第四行内容

        if rows[3][-2:] == "医生":
            cursor.execute("select name from doctor WHERE docker_id = '"+rows[0]+"'")
            sql1 = cursor.fetchall()
            if not sql1:
                if len(rows[3].split('-')) > 2:
                    cursor.execute("select clinic_id from clinic WHERE name = '" + rows[3].split('-')[2] + "'")
                    data = cursor.fetchall()
                sql = "INSERT INTO doctor(docker_id, name, phone,create_time,clinic_id) VALUES ('{}','{}','{}','{}','{}')".format(rows[0], rows[1], rows[2][-11:], crate_time,data[0][0])
                cursor.execute(sql)
                db.commit()

        if rows[3][-2:] == "护士":
            cursor.execute("select name from nurse WHERE nurse_id = '" + rows[0] + "'")
            sql1 = cursor.fetchall()
            if not sql1:
                if len(rows[3].split('-')) > 2:
                    cursor.execute("select clinic_id from clinic WHERE name = '" + rows[3].split('-')[2] + "'")
                    data = cursor.fetchall()
                sql = "INSERT INTO nurse(nurse_id, name, phone,create_time,clinic_id) VALUES ('{}','{}','{}','{}','{}')".format(rows[0], rows[1], rows[2][-11:], crate_time,data[0][0])
                cursor.execute(sql)
                db.commit()

        if rows[3][-2:] == "助护":
            cursor.execute("select name from nurse WHERE assistance_id = '" + rows[0] + "'")
            sql1 = cursor.fetchall()
            if not sql1:
                if len(rows[3].split('-')) > 2:
                    cursor.execute("select clinic_id from clinic WHERE name = '" + rows[3].split('-')[2] + "'")
                    data = cursor.fetchall()
                sql = "INSERT INTO nurse(assistance_id, name, phone,create_time,clinic_id) VALUES ('{}','{}','{}','{}','{}')".format(rows[0], rows[1], rows[2][-11:], crate_time,data[0][0])
                cursor.execute(sql)
                db.commit()

        if rows[3][-2:] == "PM":
            cursor.execute("select name from reception_pm WHERE pm_id = '" + rows[0] + "'")
            sql1 = cursor.fetchall()
            if not sql1:
                if len(rows[3].split('-')) > 2:
                    cursor.execute("select clinic_id from clinic WHERE name = '" + rows[3].split('-')[2] + "'")
                    data = cursor.fetchall()
                sql = "INSERT INTO reception_pm(pm_id, name, phone,create_time,clinic_id) VALUES ('{}','{}','{}','{}','{}')".format(rows[0], rows[1], rows[2][-11:], crate_time,data[0][0])
                cursor.execute(sql)
                db.commit()

        if rows[3][-2:] == "前台":
            cursor.execute("select name from reception_pm WHERE reception_id = '" + rows[0] + "'")
            sql1 = cursor.fetchall()
            if not sql1:
                if len(rows[3].split('-')) > 2:
                    cursor.execute("select clinic_id from clinic WHERE name = '" + rows[3].split('-')[2] + "'")
                    data = cursor.fetchall()
                sql = "INSERT INTO reception_pm(reception_id, name, phone,create_time,clinic_id) VALUES ('{}','{}','{}','{}','{}')".format(rows[0], rows[1], rows[2][-11:], crate_time,data[0][0])
                cursor.execute(sql)
                db.commit()
# for sheet_name in sheet_names:
#     sheet2 = worksheet.sheet_by_name(sheet_name)
#     for i in range(sheet.nrows):
#         rows = sheet2.row_values(i)  # 获取第四行内容
        if len(rows[3].split('-')) > 2:
            cursor.execute("select name from clinic WHERE name = '" + rows[3].split('-')[2] + "'")
            data = cursor.fetchall()
            if not data:
                sql = "INSERT INTO clinic(clinic_id,group_name, name,create_time) VALUES ('{}','{}','{}','{}')".format(uuid.uuid1(),rows[3].split('-')[1], rows[3].split('-')[2], crate_time)
                cursor.execute(sql)
                db.commit()
        if not rows[1]:
            rows[1] = ''
            cursor.execute("select name from user WHERE name = '" + rows[0] + "'")
            sql1 = cursor.fetchall()
            if not sql1:
                cursor.execute("select docker_id from doctor WHERE name = '" + rows[4] + "'")
                docker_id = cursor.fetchall()
                if not docker_id:
                    docker_id = (('',),)
                cursor.execute("select pm_id from reception_pm WHERE name = '" + rows[3] + "'")
                pm_id = cursor.fetchall()
                if not pm_id:
                    pm_id = (('',),)

                sql = "INSERT INTO user(userid, name, create_time,docker_id,pm_id) VALUES ('{}','{}','{}','{}','{}')".format(rows[1], rows[0], func(rows[2]), docker_id[0][0],pm_id[0][0])
                cursor.execute(sql)
                db.commit()
        cursor.execute("select userid from user_therapy WHERE userid = '" + rows[0] + "'")
        sql1 = cursor.fetchall()
        if not sql1:
            if rows[6] == "c.洗牙":
                sql = "INSERT INTO user_therapy(userid, s_cxya) VALUES ('{}','{}')".format(rows[1], 1)
                cursor.execute(sql)
                db.commit()
            if rows[6] == "a种植":
                sql = "INSERT INTO user_therapy(userid, s_azzhi) VALUES ('{}','{}')".format(rows[1], 1)
                cursor.execute(sql)
                db.commit()
            if rows[6] == "a正畸":
                sql = "INSERT INTO user_therapy(userid, s_azji) VALUES ('{}','{}')".format(rows[1], 1)
                cursor.execute(sql)
                db.commit()
            if rows[6] == "b.牙周":
                sql = "INSERT INTO user_therapy(userid, s_byzhou) VALUES ('{}','{}')".format(rows[1], 1)
                cursor.execute(sql)
                db.commit()
            if rows[6] == "a美学贴面":
                sql = "INSERT INTO user_therapy(userid, s_amxue) VALUES ('{}','{}')".format(rows[1], 1)
                cursor.execute(sql)
                db.commit()
            if rows[6] == "c.儿牙":
                sql = "INSERT INTO user_therapy(userid, s_ceya) VALUES ('{}','{}')".format(rows[1], 1)
                cursor.execute(sql)
                db.commit()
            if rows[6] == "b.补牙":
                sql = "INSERT INTO user_therapy(userid, s_bbuya) VALUES ('{}','{}')".format(rows[1], 1)
                cursor.execute(sql)
                db.commit()


