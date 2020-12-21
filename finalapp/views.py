from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import random
import pandas

import pymysql
# 서버에 연결한 뒤 데이터를
# 딕셔너리 커서 객체로 생성
print("qqqqqqq")
def makedata():
    conn = pymysql.connect(host='smart-factory-multicampus.cmgy7ik68xka.us-east-1.rds.amazonaws.com',
                             port=3306,
                             user='admin',
                             passwd='leelimparkleejo',
                             db='smart_factory',
                             charset='utf8',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        cur = conn.cursor() # 커서 객체 생성
        print("-----------------------")
        sql = 'SELECT * FROM SENSOR' # SQL 함수 부분  #
        cur.execute(sql) # SQL 명령 실행
        result = cur.fetchall() # 모두 불러오기
        print(result)
        print("----------------------------------------------")
    finally:
        conn.close()


    df=pandas.DataFrame(result)
    energy=df["electrical_energy"].tolist()
    time = df["time"].map(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S'))
    return time, energy


# time=df["time"].map(lambda x : str(x.hour) + ":"+ str(x.minute) +":"+str(x.second))
# print(time)
# print(type(time[0]))

def dg(request) :
    print("dg")
    return render(request, 'test.html', None)

j=10
def dgdata(request) :
    global j
    print("dg2")
    time,energy =makedata()  #count 변수를 써서 # 첨에 기동될때 makedata하고: makedata호출을 밑에 전역코드로 따로 둠 함수 안이 아니라,/ , 요청했을때
    data = []
    type = request.GET.get('type')
    if type == 'initial':
        for i in range(10): # range(len(df)) ##??? #쿼리를 계속 받게,,,?
            data.append({"x": time[i], "y": energy[i]})
    else:
        data.append({"x": time[j], "y": energy[j]})
        j+=1
        if j ==1000: #len(df) #imsi ##??? #j ==1000개아니고
            j=0

    return JsonResponse(data, safe=False)


# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# import random
#
# def dg(request) :
#     return render(request, 'test.html', None)
#
# def dgdata(request) :
# 	data = []
# 	type = request.GET.get('type')
# 	if type == 'initial':
# 		for i in range(1, 11):
# 			data.append({"x": i, "y": random.randint(1, 20)})
# 	else:
# 		data.append({"y": random.randint(1, 20)})
# 	return JsonResponse(data,  safe=False)
#
# conn = pymysql.connect(host='smart-factory-multicampus.cmgy7ik68xka.us-east-1.rds.amazonaws.com',
#                              port=3306,
#                              user='admin',
#                              passwd='leelimparkleejo',
#                              db='smart_factory',
#                              charset='utf8',
#                              autocommit=True,
#                              cursorclass=pymysql.cursors.DictCursor)
#
#
# cur = conn.cursor() # 커서 객체 생성
# print("-----------------------")
# sql = 'SELECT * FROM SENSOR' # SQL 함수 부분
# cur.execute(sql) # SQL 명령 실행
# result = cur.fetchall() # 모두 불러오기
# print(result)
# print("----------------------------------------------")
# a= pandas.DataFrame(result)
# print(a)