# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import json
import pymysql
import time
import oss2
import  os

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

    jsons = json.dumps(data ,ensure_ascii=False,encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")

@csrf_exempt
def book_name(resp):

     
    if resp.method=='GET':
        id = resp.GET.get('id')
        start_Page= resp.GET.get('start_Page')
        end_Page = resp.GET.get('end_Page')
    else:

        req = json.loads(resp.body)
        id = req.get('id')
        start_Page=req.get('start_Page')
        end_Page = req.get('end_Page')



    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='qushuwang', charset='utf8')
    cursor = conn.cursor()

    sql_content = 'SELECT * FROM book_name WHERE book_list_id = %s LIMIT %s,%s' %(id, start_Page, end_Page)
    count=cursor.execute(sql_content)
    print  count
    data = dictfetchall(cursor)


    if len(data) == 0:

         data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
         data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data ,ensure_ascii=False,encoding='utf8')

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
    auth = oss2.Auth('LTAI6KRnoV0ZfBJH', 'VKYiSOyfZJ7ojrJZpy3u5PrCLrKWHz')
    bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'sayid0924')
    bucket.get_object_to_file('Apk_Update_Path/app-debug.apk', 'AndroidApp.apk')

    fileSize = os.path.getsize('AndroidApp.apk')

    Update_Info= '更新内容\n ' + \
                 ' 1. 异常处理\n' + \
                 ' 2. 异常处理\n'

    Apk_Name = 'AndroidApp.apk'



    data ={'VersionCode':0, 'Apk_Update_Path':'Apk_Update_Path',"FileSize": fileSize,'Update_Info':Update_Info,'Apk_Name':Apk_Name}

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

    file = open('AndroidApp.apk', 'rb')
    response = FileResponse(file)

    # response['Apk-Length'] = fileSize
    # response['Content-Type'] = 'application/octet-stream'

    response['Content-Type'] = 'application/vnd.android.package-archive'
    response['Content-Disposition'] = 'attachment;filename="app-debug.apk"'

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

    jsons = json.dumps(data ,ensure_ascii=False,encoding='utf8')

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

    jsons = json.dumps(data ,ensure_ascii=False,encoding='utf8')

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

    jsons = json.dumps(data ,ensure_ascii=False,encoding='utf8')

    conn.close()

    return HttpResponse(jsons, content_type="application/json")




def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


