#coding:utf8
#generate all feature , all item will be train and create a model

import utils
import traceback
import datetime
import pdb
import time

start = time.time()

store_code = 5

period = 14

period_rst = [4, 5, 6, 7, 8]
# period_rst = [0, 3, 4, 7, 8, 9, 10]
try:

    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select distinct(item_id) from config'
    cur.execute(sql)
    rst = cur.fetchall()
    start_date = datetime.datetime(2014, 10, 1)
    item_date = datetime.datetime(2015, 12, 27)
    tem_dct = {}
    result_lst = []
    for term_id in rst:
        term_id = term_id[0]
        # for num in range(5):
        for num in [4, 5, 6, 7, 8]:
            rst_ls = []
            if item_date - datetime.timedelta(num * period) < start_date:
                break
            e_date = (item_date - datetime.timedelta(num * period)).strftime('%Y%m%d')
            s_date = (item_date - datetime.timedelta((num + 1) * period)).strftime('%Y%m%d')
            sql_num = 'select sum(qty_alipay_njhs) from item_feature where \
                         date <= "%s" and date > "%s" and item_id = %d' % (e_date, s_date, term_id)
            cur.execute(sql_num)
            r_num = cur.fetchall()

            en_date = s_date
            st_date = (item_date - datetime.timedelta((num + 2) * period)).strftime('%Y%m%d')
            sql = 'select pv_ipv, pv_uv, cart_ipv, cart_uv, collect_uv, ss_pv_ipv, ss_pv_uv, qty_alipay_njhs, jhs_pv_ipv, jhs_pv_uv, \
                   qty_alipay - qty_alipay_njhs from item_feature where date > "%s" and date <= "%s" and item_id = %d'\
                   % (st_date, en_date, term_id)
            cur.execute(sql)
            f_rst = cur.fetchall()
#             pdb.set_trace()
            rst_ls.append(f_rst[0][0])
            rst_ls.append(f_rst[0][1])
            rst_ls.append(f_rst[0][2])
            rst_ls.append(f_rst[0][3])
            rst_ls.append(f_rst[0][4])
            rst_ls.append(f_rst[0][5])
            rst_ls.append(f_rst[0][6])
            rst_ls.append(f_rst[0][7])
            rst_ls.append(f_rst[0][8])
            rst_ls.append(f_rst[0][9])
            rst_ls.append(f_rst[0][10])
            rst_ls.append(r_num[0][0])
            rst_ls.append(term_id)
            rst_ls = [x or 0 for x in rst_ls]
            result_lst.append(','.join(map(lambda x:str(x), rst_ls)))

    conn.commit()
    conn.close()

    with open('d:/tianchi/model/train_store_jhs_per_all_%d.csv' % period, 'wb') as file:
        file.writelines('\n'.join(result_lst))

except Exception as e:
    traceback.print_exc()
    pdb.set_trace()
    conn.close()
    print e

end = time.time()

print (end - start)
