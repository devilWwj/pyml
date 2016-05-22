import utils
import traceback
import os
import time
import pdb

start = time.time()
try:
    path = 'D:/ditech/citydata/season_1/test_set_1/weather_data'
    conn = utils.persist.connection()
    cur = conn.cursor()
    num = 0
    for pl in os.listdir(path):
        if not '.' in pl:
            with open(path + '/' + pl) as file:
                lines = file.readlines()
                for line in lines:
                    lst = line.split('\t')
                    for tline in lst[1:-1]:
                        sql = 'insert into weather_test values("%s", %d, %f, %f)' % (lst[0], int(lst[1]), float(lst[2]), float(lst[3]))
                    
                        cur.execute(sql)
                    
    conn.commit()
    conn.close()
except:
    traceback.print_exc()
    print sql
    conn.commit()
    conn.close()
end = time.time()
print end - start