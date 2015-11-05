#encoding:utf8
import os
import json
import sys
import re
import MySQLdb
import time
import codecs
from jobs import utils
from jobs.majorposition import get_position
reload(sys)
start = time.clock()
sys.setdefaultencoding('utf8')
postdct = get_position.get_pos()
        
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    #sql = 'select userid from jobs_uinfotest'
    import pdb
    pdb.set_trace()
    position_dct = {}
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            position_dct[uline] = '1'
    sql = 'select position_name from work_sizetest'
    cur.execute(sql)
    positionlst = cur.fetchall()
    positions = []
    result = []
    flag = False
    i = 0
    p = 0
    l = 0
    for position in positionlst:
        if len(positions) < 2:
            positions.append(position[0])
        else:
            if position_dct.has_key(positions[0]):
                result.append(positions[0])
                flag = True
                p += 1
            elif position_dct.has_key(positions[1]):
                result.append(positions[1])
                flag = True
                p += 1
            else:
                for key in postdct.keys():   
                    if key in positions[0]:
                        if u'总监' in positions[0] or u'主管' in positions[0]:
                            result.append(postdct[key][2])
                        elif u'经理' in positions[0] or u'主任' in positions[0]:
                            result.append(postdct[key][1])
                        else:
                            result.append(postdct[key][0])
                        flag = True
                        i += 1
                        break
                    elif key in positions[1]:
                        if u'总监' in positions[1] or u'主管' in positions[1]:
                            result.append(postdct[key][2])
                        elif u'经理' in positions[1] or u'主任' in positions[1]:
                            result.append(postdct[key][1])
                        else:
                            result.append(postdct[key][0])
                        flag = True
                        i += 1
                        break
                if not flag:
                    result.append('test')
                    l += 1
            flag = False
            positions = [position[0]]
    if position_dct.has_key(positions[0]):
        result.append(positions[0])
    elif position_dct.has_key(positions[1]):
        result.append(positions[1])
    else:
        result.append('test')
        
    print i
    print p
    print len(result)
    utils.store_rst(result, 'position.txt')
    print l
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    