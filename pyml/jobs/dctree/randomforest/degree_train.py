#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
import time
reload(sys)
sys.setdefaultencoding('utf8')
import pdb
start = time.clock()
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select jb.degree, jb.age, jb.gender, jb.start_age, jb.bstart_year, jb.start_salary, wk.size, jb.major \
                                        from jobs_uinfo as jb left join workexperience as wk on \
                                        jb.userid = wk.userid and wk.num = 1'
    cur.execute(sql)
    file = open('d:/jobs/dctree/random/degree-train.csv', 'w+')
    useridlst = cur.fetchall()
    sq = 'select name from major where degreer0 >=0.6'
#     pdb.set_trace()
    cur.execute(sq)
    degreer0lst = cur.fetchall()
    degreer0dct = {}
    for degree in degreer0lst:
        degreer0dct[degree[0]] = 1
    sq1 = 'select name from major where degreer1 >=0.6'
    cur.execute(sq1)
    degreer1lst = cur.fetchall()
    degreer1dct = {}
    for degree in degreer1lst:
        degreer1dct[degree[0]] = 1
    sq2 = 'select name from major where degreer2 >=0.6'
    cur.execute(sq2)
    degreer2lst = cur.fetchall()
    degreer2dct = {}
    for degree in degreer2lst:
        degreer2dct[degree[0]] = 1
#     file.write('degree,age,start_age,bstart_year,gender,start_salary,start_size,major\n')
#     pdb.set_trace()
    for userid in useridlst:
        print userid
        userid = list(userid)
        if int(userid[1]) <= 20:
            userid[1] = '18'
        elif int(userid[1]) >= 60:
            userid[1] = '60'
        if degreer0dct.has_key(userid[7]):
            userid.pop(-1)
            userid.append(0)
        elif degreer1dct.has_key(userid[7]):
            userid.pop(-1)
            userid.append(1)
        elif degreer2dct.has_key(userid[7]):
            userid.pop(-1)
            userid.append(2)
        else:
            userid.pop(-1)
            userid.append(3)
        userlst = map(str, userid)
        strs = ','.join(userlst) + '\n'
        file.write(strs)
        
    conn.commit()
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
end = time.clock()
print (end - start)