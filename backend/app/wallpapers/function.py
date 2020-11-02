import os
import time
import datetime
import requests
import configparser
from werkzeug.utils import secure_filename
try:
    from ..model.wallpapers_model import wallpapers as wallpapers_table
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.wallpapers_model import wallpapers as wallpapers_table

cf = configparser.ConfigParser()
cf.read('../homepage.config')
WALLPAPERS_PATH = cf.get('config', 'BASE_PATH') + 'wallpapers/'

base_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=2"
r = requests.get(base_url)
url = 'https://www.bing.com' + r.json()['images'][0]['url'].split('&')[0]
date_raw = str(r.json()['images'][0]['startdate'])
date = date_raw[:4] + '-' + date_raw[4:6] + '-' + date_raw[6:]
copyright = r.json()['images'][0]['copyright']
copyrightlink = r.json()['images'][0]['copyrightlink']

img_data = requests.get(url=url).content

folder_path = WALLPAPERS_PATH
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
filename = str(date) + '.jpg'
upload_path = os.path.join(folder_path, secure_filename(filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
with open(upload_path, 'wb') as fp:
    fp.write(img_data)
size = str(round(float(int(os.path.getsize(upload_path)) / 1000000), 2)) + 'MB'

wallpapers_table.create(date=date, url=url, size=size, copyright=copyright, copyrightlink=copyrightlink, update_time=datetime.datetime.now())
