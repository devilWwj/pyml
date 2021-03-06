#test git
import os
import json
import re
import utils
import pdb
try:

    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    mode = re.compile(r'\d+')
    with open('d:/tianchi/music/mars_tianchi_songs.csv') as file:
        lines = file.readlines()
        for line in lines:
            items = line.split(',')
            sql = 'insert into songs(song_id, artist_id, publish_time, song_init_plays, launguage,\
                    gender) values ("%s", "%s", "%s", %d, %d, %d)' % (items[0], items[1], \
                                    items[2], int(items[3]), int(items[4]), int(items[5]))
            cur.execute(sql)
    conn.commit()
    conn.close()

except Exception as e:
    pdb.set_trace()
    conn.close()
    print e