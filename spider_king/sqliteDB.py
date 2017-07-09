import sqlite3
from spider_king.utils import confLoad
from spider_king.utils import logger
import traceback

class sqliteDB:

    conn = None

    def __init__(self):
        try:
            self.conn = sqlite3.connect(confLoad.get('path', 'root_path') + 'toutiao.db')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS toutiao (URL          CHAR(200)    );''')
        except:
            logger.error(traceback.format_exc())

    def insert(self,url):
        try:
            self.conn.execute("INSERT INTO toutiao (URL) \
                        VALUES ('" + url + "')")
            self.conn.commit()
        except:
            logger.error(traceback.format_exc())

    def query(self,url):
        try:
            cursor = self.conn.execute("SELECT count(*)  from toutiao where URL='" + url + "/'")
            result = cursor.fetchall()
            if result[0][0] > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback,format())

    def close(self):
        self.conn.close()



