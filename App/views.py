# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
import pymysql
import time


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


def book_name(resp):

    id = resp.GET.get('id')
    start_Page= resp.GET.get('start_Page')
    end_Page = resp.GET.get('end_Page')

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




def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]