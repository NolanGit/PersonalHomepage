import os
import time
import requests
import configparser
from werkzeug.utils import secure_filename

cf = configparser.ConfigParser()
cf.read('app/homepage.config')
BING_WALLPAPERS_PATH = cf.get('config', 'BING_WALLPAPERS_PATH')

result = {}
base_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=2"
r = requests.get(base_url)
url = 'https://www.bing.com/' + r.json()['images'][0]['url'].split('&')[0]
result['url'] = url
result['date'] = r.json()['images'][0]['startdate']
result['copyright'] = r.json()['images'][0]['copyright']
result['copyrightlink'] = r.json()['images'][0]['copyrightlink']

img_data = requests.get(url=result['url']).content

folder_path = BING_WALLPAPERS_PATH
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
filename = str(result['date']) + '.jpg'
upload_path = os.path.join(folder_path, secure_filename(filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
with open(upload_path, 'wb') as fp:
    fp.write(img_data)
fsize = str(round(float(int(os.path.getsize(upload_path)) / 1000000), 2)) + 'MB'