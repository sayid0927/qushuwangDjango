# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
import pymysql
import time
import oss2

from django.views.decorators.csrf import csrf_exempt


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

    if len(data) == 0:

        data = {"res": '00001', "data": data, 'currentTimes': time.time(), "message": "查询失败"}
    else:
        data = {"res": '00000', "data": data, 'currentTimes': time.time(), "message": "查询成功"}

    jsons = json.dumps(data, ensure_ascii=False, encoding='utf8')

    return HttpResponse(jsons, content_type="application/json")





def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
