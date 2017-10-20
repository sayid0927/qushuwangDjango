# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
import pymysql
# Create your views here.


def book_list(resp):
    conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='qushuwang', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select * from book_list")
    data = dictfetchall(cursor)

    if resp.method == 'POST':

        if len(data) == 0:
            jsons = json.dumps({"res": '00001', "msg": data})
        else:
            jsons = json.dumps({"res": '00000', "msg": data})
    else:
        jsons = json.dumps({"res": '00001', "msg": data})

    conn.close()
    return HttpResponse(jsons, content_type="application/json")







def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]