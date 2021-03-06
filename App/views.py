# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.shortcuts import render
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
import json
import pymysql
import time
import oss2
import os

from django.views.decorators.csrf import csrf_exempt

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


@csrf_exempt
def book_list(resp):
    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='qushuwang', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select * from book_list")
    data = dictfetchall(cursor)

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def book_name(resp):
    if resp.method == 'GET':
        id = resp.GET.get('id')
        start_Page = resp.GET.get('start_Page')
        end_Page = resp.GET.get('end_Page')
    else:

        req = json.loads(resp.body)
        id = req.get('id')
        start_Page = req.get('start_Page')
        end_Page = req.get('end_Page')

    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='qushuwang', charset='utf8')
    cursor = conn.cursor()

    sql_content = 'SELECT * FROM book_name WHERE book_list_id = %s LIMIT %s,%s' % (id, start_Page, end_Page)
    count = cursor.execute(sql_content)
    print  count
    data = dictfetchall(cursor)

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def book_dir(resp):
    if resp.method == 'GET':
        book_name_id = resp.GET.get('book_name_id')
        start_Page = resp.GET.get('start_Page')
        end_Page = resp.GET.get('end_Page')
    else:

        req = json.loads(resp.body)
        book_name_id = req.get('book_name_id')
        start_Page = req.get('start_Page')
        end_Page = req.get('end_Page')

    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='qushuwang', charset='utf8')
    cursor = conn.cursor()

    sql_content = 'select * from book where book_name_id= %s order by book_number asc limit %s, %s' % (book_name_id, start_Page, end_Page)

    count = cursor.execute(sql_content)
    data = dictfetchall(cursor)

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def book_content(resp):
    if resp.method == 'GET':
        book_path = resp.GET.get('book_path')
    else:
        req = json.loads(resp.body)
        book_path = req.get('book_path')

    auth = oss2.Auth('LTAI6KRnoV0ZfBJH', 'VKYiSOyfZJ7ojrJZpy3u5PrCLrKWHz')
    bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'sayid0924')
    remote_stream = bucket.get_object(book_path)
    data = remote_stream.read()

    data = data.decode('utf-8', 'ignore')

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def apk_update(resp):
    # auth = oss2.Auth('LTAI6KRnoV0ZfBJH', 'VKYiSOyfZJ7ojrJZpy3u5PrCLrKWHz')
    # bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'sayid0924')
    # bucket.get_object_to_file('Apk_Update_Path/app-debug.apk', 'AndroidApp.apk')

    fileSize = os.path.getsize('app-release.apk')

    Update_Info = '更新内容\n ' + \
                  ' 1. 异常处理\n' + \
                  ' 2. 异常处理\n'

    Apk_Name = 'app-release.apk'

    data = {'VersionCode': 1, 'Apk_Update_Path': 'Apk_Update_Path', "FileSize": fileSize, 'Update_Info': Update_Info, 'Apk_Name': Apk_Name}

    data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def apk_update_path(resp):
    # auth = oss2.Auth('LTAI6KRnoV0ZfBJH', 'VKYiSOyfZJ7ojrJZpy3u5PrCLrKWHz')
    # bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'sayid0924')
    # bucket.get_object_to_file('Apk_Update_Path/app-debug.apk', 'app-debug.apk')

    # filePath = unicode('app-debug.apk', 'utf8')

    # fileSize = os.path.getsize('AndroidApp.apk')
    # fileSize = str(fileSize)

    file = open('app-release.apk', 'rb')
    # response = FileResponse(file)
    response = StreamingHttpResponse(file)
    # response['Apk-Length'] = fileSize
    # response['Content-Type'] = 'application/octet-stream'

    response['Content-Type'] = 'application/vnd.android.package-archive'
    response['Content-Disposition'] = 'attachment;filename="app-release.apk"'
    return response


@csrf_exempt
def manhun_list(resp):
    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='manhua', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select * from manhun_book_list")
    data = dictfetchall(cursor)

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def manhun_name_list(resp):
    if resp.method == 'GET':
        id = resp.GET.get('id')
        start_Page = resp.GET.get('start_Page')
        end_Page = resp.GET.get('end_Page')

    else:
        req = json.loads(resp.body)
        id = req.get('id')
        start_Page = req.get('start_Page')
        end_Page = req.get('end_Page')

    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='manhua', charset='utf8')
    cursor = conn.cursor()

    sql_content = 'SELECT * FROM manhun_book_name WHERE manhun_book_list_id = %s LIMIT %s,%s' % (id, start_Page, end_Page)
    count = cursor.execute(sql_content)
    data = dictfetchall(cursor)

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def meinvha_dir_list(resp):
    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='meinvha', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select * from dir")
    data = dictfetchall(cursor)

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def meinvha_title_list(resp):
    if resp.method == 'GET':
        id = resp.GET.get('id')
        start_Page = resp.GET.get('start_Page')
        end_Page = resp.GET.get('end_Page')

    else:
        req = json.loads(resp.body)
        id = req.get('id')
        start_Page = req.get('start_Page')
        end_Page = req.get('end_Page')

    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='meinvha', charset='utf8')
    cursor = conn.cursor()

    sql_content = 'SELECT * FROM title WHERE dir_id = %s LIMIT %s,%s' % (id, start_Page, end_Page)
    count = cursor.execute(sql_content)
    data = dictfetchall(cursor)
    list = []

    for id in data:

        title_id = id.get("id")

        sql_content = 'SELECT * FROM img_url WHERE title_id = %s ' % (title_id)

        count = cursor.execute(sql_content)
        img_url_data = dictfetchall(cursor)

        if len(img_url_data) != 0:
            img_url = random.sample(img_url_data, 1)[0]
            d3 = {}
            d3.update(img_url)
            d3.update(id)
            list.append(d3)

    if len(list) == 0:

        data = {"res": '00001', "data": list, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": list, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def meinvha_img_list(resp):
    if resp.method == 'GET':
        id = resp.GET.get('id')

    else:
        req = json.loads(resp.body)
        id = req.get('id')

    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='meinvha', charset='utf8')
    cursor = conn.cursor()

    sql_content = 'SELECT * FROM img_url WHERE title_id = %s ' % (id)
    count = cursor.execute(sql_content)
    data = dictfetchall(cursor)

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def App_Info(resp):
    if resp.method == 'GET':
        dates = resp.GET.get('date')
        AppPackageName = resp.GET.get('AppPackageName')
        AppName = resp.GET.get('AppName')
        AppVersionName = resp.GET.get('AppVersionName')
        AppVersionCode = resp.GET.get('AppVersionCode')
    else:
        req = json.loads(resp.body)
        dates = req.get('date')
        AppPackageName = req.get('AppPackageName')
        AppName = req.get('AppName')
        AppVersionName = req.get('AppVersionName')
        AppVersionCode = req.get('AppVersionCode')

    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='App', charset='utf8')
    cursor = conn.cursor()
    sql_insert = "insert into AppInfo(Appdates,AppPackageName,AppName,AppVersionName,AppVersionCode) values(%s,%s,%s,%s,%s)"
    params = (dates, AppPackageName, AppName, AppVersionName, AppVersionCode)
    count = cursor.execute(sql_insert, params)

    if count == 0:
        data = {"res": '00001', "data": count, 'currentTimes': time.time(), "message": "插入失败"}
    else:
        data = {"res": '00000', "data": count, 'currentTimes': time.time(), "message": "插入成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')
    return HttpResponse(jsons, content_type="application/json")


@csrf_exempt
def phone_info(resp):
    if resp.method == 'GET':
        isPhone = resp.GET.get('isPhone')
        PhoneNumber = resp.GET.get('PhoneNumber')
        IMEI = resp.GET.get('IMEI')
        IMSI = resp.GET.get('IMSI')
        PhoneType = resp.GET.get('PhoneType')
        IPAddress = resp.GET.get('IPAddress')
        NetworkOperatorName = resp.GET.get('NetworkOperatorName')
        Locality = resp.GET.get('Locality')
        SDKVersion = resp.GET.get('SDKVersion')
        AndroidID = resp.GET.get('AndroidID')
        MacAddress = resp.GET.get('MacAddress')
        Manufacturer = resp.GET.get('Manufacturer')
        Model = resp.GET.get('Model')
    else:
        req = json.loads(resp.body)
        isPhone = req.get('isPhone')
        PhoneNumber = req.get('PhoneNumber')
        IMEI = req.get('IMEI')
        IMSI = req.get('IMSI')
        PhoneType = req.get('PhoneType')
        IPAddress = req.get('IPAddress')
        NetworkOperatorName = req.get('NetworkOperatorName')
        Locality = req.get('Locality')
        SDKVersion = req.get('SDKVersion')
        AndroidID = req.get('AndroidID')
        MacAddress = req.get('MacAddress')
        Manufacturer = req.get('Manufacturer')
        Model = req.get('Model')

    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='App', charset='utf8')
    cursor = conn.cursor()
    sql_insert = "insert into PhoneInfo(isPhone,PhoneNumber,IMEI,IMSI,PhoneType,IPAddress,NetworkOperatorName,Locality,SDKVersion,AndroidID,MacAddress,Manufacturer,Model) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    params = (isPhone, PhoneNumber, IMEI, IMSI, PhoneType, IPAddress, NetworkOperatorName, Locality, SDKVersion, AndroidID, MacAddress, Manufacturer, Model)
    count = cursor.execute(sql_insert, params)


    if count == 0:
        data = {"res": '00001', "data": count, 'currentTimes': time.time(), "message": "插入失败"}
    else:
        data = {"res": '00000', "data": count, 'currentTimes': time.time(), "message": "插入成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')
    return HttpResponse(jsons, content_type="application/json")


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]



