import configparser
import logging

# 配置文件管理
confLoad = configparser.ConfigParser()
confLoad.read('spider_king.conf')

# 日志管理
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(confLoad.get('logger','position')+'spider_king_error.log')
fh.setLevel(logging.ERROR)

ch = logging.StreamHandler()
ch.setLevel(int(confLoad.get('logger','console_level')))

formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)