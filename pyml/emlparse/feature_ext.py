#coding:utf8
import time
import sys
import email
import os
import jieba
import time
from parse1 import parse_eml
import argparse
import traceback
reload(sys)
import pdb
from email import utils
import jieba
import base64
import poplib
import utils as emlutils
from email.header import decode_header
sys.setdefaultencoding('utf8')

stop_words = ['面试', '邀请', '介绍', '加入', '公司', '有限', '机会', '职位', '推荐', '简介', '月薪', '工作',\
              '服务', '开发', '北京', '高级', '回复', '邀请函', '并', '查收', '工程师', '】', '来信', '您',\
              '请', '收到', '谢谢', '通知', '网络', '沟通', '邮件', '诚邀', '来自', '北京', '-', '技术',\
              '核心', '关于', '的', '—', '候选人', '有限公司', '软件', '（', '上海', '【', '资深', 'PHP',\
              '来自', '：', '招聘', '上市', '互联网', '金融']

filter_words = ['智联', '汇总', '奖品', '提醒', '在线考评', '薪水', '电影',\
                '会员', '注册', '51job', '已经有', '不合适', '最新职位', '手机',\
                '简历', '跳槽',  '猎头', '网易考拉', '互联网淘金', '已投', '安全问题', '机会'\
                '靠谱', '推荐', '微博']
mailst = ['service@steelport.zhaopin.com', 'service@51job.com']

def decode_nck(nick):
    try:
        nklst = nick.split('?')
        return base64.decodestring(nklst[3]).decode(nklst[1])
    except:
        return ''

start = time.time()
if __name__ == '__main__':
    user = 'nrall001@163.com'
    password = 'nr1531032'
    pop3_server = 'pop.163.com'

    server = poplib.POP3(pop3_server)
    print server.getwelcome()
    server.user(user)
    server.pass_(password)
    print 'Message: %s. Size: %s' % server.stat()
    resp, mails, octets = server.list()
    pdb.set_trace()
    index = len(mails)
    spam_csv = []
    ter_csv = []
    num = 0
    ter_nm = 0
    words = set()
    wordm = set()
    for v in range(index):
        try:
            # resp, lines, octets = server.retr(v+1)
            resp, lines, octets = server.top(v+1, 7)
            msg_content = '\r\n'.join(lines)
            msg = email.message_from_string(msg_content)
            fmail = msg.get('From')
            from_mail = utils.parseaddr(msg.get('From'))[1]
            nick = fmail.split(' ')[0]
            if '=' in nick:
                nick = decode_nck(nick)
            subject = msg.get('Subject')
            subject = decode_header(subject)[0][0].replace(' ', '')
            flag = 0
            try:
                subject = subject.decode('utf8').encode('utf8')
            except:
                try:
                    subject = subject.decode('gbk').encode('utf8')
                except:
                    subject = subject.decode('gb18030').encode('utf8')
            for word in filter_words:
                if word in subject:
                    flag = 1
                    break
            if not flag:
                subject = subject.replace(',', '')
                seglst = jieba.cut(subject, cut_all=False)
                for seg in seglst:
                    wordm.add(seg)
                    words.add(seg)
                ter_csv.append('|'.join([subject, nick]))
                ter_nm += 1
            else:
                num += 1
                subject = subject.replace(',', '')
                print '=========================================='
                spam_csv.append('|'.join([subject, nick]))
                seglst = jieba.cut(subject, cut_all=False)
                for seg in seglst:
                    words.add(seg)
                ncklst = jieba.cut(nick, cut_all=False)
                for nk in ncklst:
                    words.add(nk)
                print '------------------------------------------'
        except:
            pass
    print ter_nm
    print len(wordm)
    print num
    print len(words)
    with open('d:/naren/spam.csv', 'wb') as file:
        file.writelines('\n'.join(spam_csv).encode('utf8'))
    with open('d:/naren/ter.csv', 'wb') as file:
        file.writelines('\n'.join(ter_csv).encode('utf8'))
    server.quit()
end = time.time()

print (end - start)
