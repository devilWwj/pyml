#coding:utf8
import os
import sys
import re
import MySQLdb
import time
import jieba
from jobs import utils
import pdb
from logging import getLevelName
reload(sys)
import codecs
sys.setdefaultencoding('utf8')
start = time.clock()

def get_position_meta():
    position_dct = {}
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            position_dct[uline] = '1'
    return position_dct

def read_tree(filename):
    '''
    '''
    import pickle
    reader = open(filename,'rU')
    return pickle.load(reader)

def get_letter_dct(position_dct):
    letter_dct = {}
    for position in position_dct.keys():
        letter_dct[position] = [[], []]
    
    return letter_dct
        
try:
    pdb.set_trace()
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select position_name from work_size'
    cur.execute(sql)
    position_dct = get_position_meta()
#     file = open('d:/jobs/dctree/majortest.csv', 'w+')
    positionlst = cur.fetchall()
    i = 0
    letterdct = {}
    letter_dct = get_letter_dct(position_dct)
    
    for j in xrange(70000):
        poslst = positionlst[j:j+3]
        if not position_dct.has_key(poslst[1][0]):
            continue
        seg_lst = jieba.cut(poslst[0][0])
        for term in seg_lst:
            if len(term) > 1:
                letter_dct[poslst[1][0]][0].append(term)
            if not letterdct.has_key(term):
                letterdct[term] = 1
            else:
                letterdct[term] += 1
        seg_lst = jieba.cut(poslst[2][0])
        for term in seg_lst:
            if len(term) > 1:
                letter_dct[poslst[1][0]][1].append(term)
            if not letterdct.has_key(term):
                letterdct[term] = 1
            else:
                letterdct[term] += 1

    positions = letterdct.keys()
    positions_num = []
#     for letter in positions:
#         print letter
#         if letter == '\\':
#             continue
#         sq = 'insert into letter(name, type, num, stopped) values ("%s", "%s", %d, 0)' % (letter, 'work_size', letterdct[letter])
#         print sq
#         cur.execute(sq)
    utils.store_rst(letter_dct, 'letterdct')
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)