# -*- coding:utf-8 -*-
import os
import re
import sys
import time
import json
import base64
import datetime
import requests
import traceback
from lxml import etree
from threading import Thread
from bs4 import BeautifulSoup

#理论python和前端js会自动转义，但如果采集名称因引号或其它需转义的字符报错，请将相应采集名修改如下
#hot_name = .replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").replace("\"", "").replace("\'", "").strip()

#采集数据保存目录,为了安全请修改本程序名字,或移动到其他目录,并修改以下路径,默认与程序同目录
dir = os.path.dirname(os.path.abspath(__file__)) + "/json/"

try:
    os.mkdir(dir)
except Exception as e:
    traceback.print_exc()
    print("json文件夹创建失败(已存在或无写入权限)")


#UTC时间转本地时间（+8:00）
def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


#百度
def parse_baidu(name):
    try:
        jsondict = {}
        jsondict['website'] = 'baidu'
        if name == 'now':
            jsondict["title"] = "实时"
            url = "http://top.baidu.com/buzz?b=1"
        if name == 'today':
            jsondict["title"] = "今日"
            url = "http://top.baidu.com/buzz?b=341"
        if name == 'week':
            jsondict["title"] = "七日"
            url = "http://top.baidu.com/buzz?b=42"
        fname = dir + "baidu_" + name + ".json"
        r = requests.get(url, timeout=(5, 10))
        r.encoding = 'gb2312'
        soup = etree.HTML(r.text.replace("<tr >", "<tr class=\"hideline\">"))
        list = []
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        for soup_a in soup.xpath("//tr[@class='hideline']"):
            blist = {}
            hot_name = soup_a.xpath("./td[2]/a[1]/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.xpath("./td[2]/a[1]/@href")[0]
            hot_num = soup_a.xpath("./td[@class='last']/span/text()")[0]
            group = name
            blist["name"] = hot_name
            blist["url"] = hot_url
            blist["num"] = hot_num
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "(" + name + ")" + "采集错误，请及时更新规则！")


#黑客派-好玩
def parse_hacpai(name):
    try:
        jsondict = {}
        jsondict['website'] = 'hacpai'
        if name == "play":
            jsondict["title"] = "好玩"
            group = "hacpai_play"
            url = "https://hacpai.com/domain/play"
        if name == "hot":
            jsondict["title"] = "热议"
            group = "hacpai_hot"
            url = "https://hacpai.com/recent/hot"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Referer': 'https://hacpai.com/'}
        fname = dir + "hacpai_" + name + ".json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        soup = etree.HTML(r.text)
        list = []
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        for soup_a in soup.xpath("//h2[@class='article-list__title article-list__title--view fn__flex-1']/a[@data-id]"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.get('href')
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "(" + name + ")" + "采集错误，请及时更新规则！")


#什么值得买-今日热门文章
def parse_smzdm_article(name):
    try:
        jsondict = {}
        jsondict['website'] = 'smzdm_article'
        if name == "today":
            id = "1"
            jsondict["title"] = "日榜"
        if name == "week":
            id = "7"
            jsondict["title"] = "周榜"
        if name == "month":
            id = "30"
            jsondict["title"] = "月榜"
        url = "https://post.smzdm.com/rank/json_more/?unit=" + id + "&p=1"
        url2 = "https://post.smzdm.com/rank/json_more/?unit=" + id + "&p=2"
        headers = {'Referer': 'https://post.smzdm.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "smzdm_article_" + name + ".json"
        r = requests.get(url, headers=headers, timeout=(5, 10)).text
        data = json.loads(r)
        r2 = requests.get(url2, headers=headers, timeout=(5, 10)).text
        data2 = json.loads(r2)
        list = []
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        for n in data['data']:
            blist = {}
            hot_url = n['article_url']
            hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            group = "smzdm_article"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        for n in data2['data']:
            blist = {}
            hot_url = n['article_url']
            hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            group = "smzdm_article"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "(" + name + ")" + "采集错误，请及时更新规则！")


#36Kr
def parse_36kr():
    try:
        url = "https://36kr.com/"
        headers = {
            'Referer': 'https://36kr.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        r = requests.get(url, headers=headers, timeout=(5, 10))
        soup = BeautifulSoup(r.text, 'html.parser')
        jsondict = {}
        jsondict['website'] = '36kr'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time

        def hot_class_filter(class_text):
            return (class_text is not None) and (('hotlist-item-other-title' in class_text) or ('hotlist-item-toptwo-title' in class_text))

        list = []
        for soup_a in soup.find_all(class_=hot_class_filter):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = 'https://36kr.com' + soup_a.get('href')
            group = "36Kr"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["title"] = "热门"
        jsondict["data"] = list
        fname = dir + "36kr_hot.json"
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)

        def article_class_filter(class_text):
            return (class_text is not None) and ('article-item-title' in class_text)

        list = []
        for soup_a in soup.find_all(class_=article_class_filter):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = 'https://36kr.com' + soup_a.get('href')
            group = "36Kr"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["title"] = "最新"
        jsondict["data"] = list
        fname = dir + "36kr_article.json"
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)

    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#新京报
def parse_bjnews():
    try:
        url = "http://www.bjnews.com.cn/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=(5, 10))
        soup = BeautifulSoup(r.text, 'html.parser')
        jsondict = {}
        jsondict['website'] = 'bjnews'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time

        list = []
        for soup_a in soup.find_all('div', 'pin_demo'):
            blist = {}
            hot_name = soup_a.find('a').find('div').text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.find('a').get('href')
            group = "bjnews"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["title"] = "推荐"
        jsondict["data"] = list
        fname = dir + "bjnews_suggestion.json"
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)

        list = []
        ranking = soup.find('div', 'ranking')
        ranking['class'] = 'processed'
        for soup_a in ranking.find_all('a', 'link'):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()[2:]
            hot_url = soup_a.get('href')
            group = "bjnews"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["title"] = "热榜"
        jsondict["data"] = list
        fname = dir + "bjnews_ranking.json"
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)

        list = []
        ranking = soup.find('div', 'hotComment')
        for soup_a in ranking.find_all('a', 'link'):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()[2:]
            hot_url = soup_a.get('href')
            group = "bjnews"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["title"] = "热评"
        jsondict["data"] = list
        fname = dir + "bjnews_comment_ranking.json"
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)

    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#知乎热榜
def parse_zhihu_hot():
    try:
        fname = dir + "zhihu_hot.json"
        zhihu_all = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Host': 'www.zhihu.com'
        }
        r = requests.get(zhihu_all, headers=headers, timeout=(5, 10)).text
        data = json.loads(r)
        news = data['data']
        list = []
        jsondict = {}
        jsondict['website'] = 'zhihu'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "热榜"
        for n in news:
            blist = {}
            hot_name = n['target']['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = n['target']['url'].replace("api.zhihu.com/questions/", "www.zhihu.com/question/")
            group = "zhihu_hot"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#知乎每日精选-编辑推荐
def parse_zhihu_good():
    try:
        url = "https://www.zhihu.com/node/ExploreRecommendListV2"
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'authority': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/explore/recommendations',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        d = {'method': 'next', 'params': '{"limit":40,"offset":0}'}
        fname = dir + "zhihu_good.json"
        r = requests.post(url, data=d, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        json_data = ""
        list = []
        jsondict = {}
        jsondict['website'] = 'zhihu'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "推荐"
        for json_d in json.loads(r.text)['msg']:
            json_data = json_data + json_d
        soup = etree.HTML(json_data)
        for soup_a in soup.xpath("//div[@class='zm-item']/h2/a"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.get('href').replace("/question/", "https://www.zhihu.com/question/")
            group = "zhihu_good"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#知乎日报
def parse_zhihu_daily():
    try:
        url = "https://daily.zhihu.com/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Referer': 'https://daily.zhihu.com/'}
        fname = dir + "zhihu_daily.json"
        r = requests.get(url, headers=headers, timeout=(5, 10)).text.replace(" class=\"home\"", "")
        soup = etree.HTML(r)
        list = []
        jsondict = {}
        jsondict['website'] = 'zhihu'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "知乎日报"
        for soup_a in soup.xpath("//div[@class='box']/a"):
            blist = {}
            hot_name = soup_a.xpath('./span/text()')[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = "https://daily.zhihu.com" + soup_a.get('href')
            group = "zhihu_daily"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#微信公众号热门文章
def parse_weixin():
    try:
        url = "https://weixin.sogou.com/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "weixin.json"
        fname2 = dir + "weixin_hot.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        list = []
        jsondict = {}
        jsondict['website'] = 'weixin'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "搜索热词"
        hot_news = soup.find('ol', 'hot-news')
        for soup_a in hot_news.find_all('li'):
            blist = {}
            hot_name = soup_a.find("a").get('title').replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.find("a").get('href')
            group = "weixin"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
        list = []
        jsondict["time"] = list_time
        jsondict["title"] = "热门文章"
        for soup_a in soup.find('ul', 'news-list').find_all("div", "txt-box"):
            blist = {}
            hot_name = soup_a.find("h3").find("a").text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.find("h3").find("a").get('href').replace('×tamp','&timestamp')
            group = "weixin"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname2, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#微博热点排行榜
def parse_weibo():
    try:
        fname = dir + "weibo.json"
        weibo_ssrd = "https://s.weibo.com/top/summary?cate=realtimehot"
        weibo = "https://s.weibo.com"
        r = requests.get(weibo_ssrd, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = etree.HTML(r.text)
        list = []
        jsondict = {}
        jsondict['website'] = 'weibo'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "微博热点排行榜"
        for soup_a in soup.xpath("//td[@class='td-02']"):
            blist = {}
            hot_name = soup_a.xpath("./a/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = weibo + soup_a.xpath("./a/@href")[0]
            try:
                hot_num = soup_a.xpath("./span/text()")[0]
            except IndexError:
                hot_num = ''
#            hot_num = None #与''皆是赋值空
            if "javascript:void(0)" in hot_url:  #过滤微博的广告，做个判断
                str_list = ""
            else:
                group = "weibo"
                blist["name"] = hot_name
                blist["url"] = hot_url
                if hot_num:
                    blist["num"] = hot_num
                list.append(blist)
                jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#V2EX热帖
def parse_v2ex():
    try:
        url = "https://www.v2ex.com/?tab=hot"
        fname = dir + "v2ex.json"
        r = requests.get(url, timeout=(5, 10))
        soup = etree.HTML(r.text)
        list = []
        jsondict = {}
        jsondict['website'] = 'v2ex'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "V2EX热帖"
        for soup_a in soup.xpath("//span[@class='item_title']/a"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = "https://www.v2ex.com" + soup_a.get('href')
            group = "v2ex"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#抽屉新热榜
def parse_chouti():
    try:
        url = "https://dig.chouti.com/link/hot"
        headers = {
            'Referer': 'https://dig.chouti.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        fname = dir + "chouti.json"
        r = requests.get(url, headers=headers, timeout=(5, 10)).text
        data = json.loads(r)
        news = data['data']
        list = []
        jsondict = {}
        jsondict['website'] = 'chouti'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(str(data['data'][0]['time_into_pool'])[0:10])))
        jsondict["time"] = list_time
        jsondict["title"] = "抽屉新热榜"
        for n in news:
            blist = {}
            hot_url = n['originalUrl']
            if 'chouti.com' not in hot_url:
                hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
                group = "chouti"
                blist["name"] = hot_name
                blist["url"] = hot_url
                list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#煎蛋网
def parse_jandan():
    try:
        url = "https://jandan.net/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Referer': 'https://jandan.net/'}
        fname = dir + "jandan.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        soup = etree.HTML(r.text)
        list = []
        jsondict = {}
        jsondict['website'] = 'jandan'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "煎蛋网"
        for soup_a in soup.xpath("//div[@class='post f list-post']/div[@class='indexs']/h2/a"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.get('href')
            group = "jandan"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#豆瓣
def parse_douban():
    try:
        url = "https://www.douban.com/group/explore"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "douban.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        list = []
        jsondict = {}
        jsondict['website'] = 'douban'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "豆瓣热帖"
        for soup_a in soup.find_all("div", "channel-item"):
            blist = {}
            hot_name = soup_a.find('h3').find('a').text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.find('h3').find('a').get('href')
            group = "mop"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#果壳-科学人
def parse_guokr():
    try:
        url = "https://www.guokr.com/scientific/"
        url2 = "https://www.guokr.com/beta/proxy/science_api/articles?retrieve_type=by_category&page=1"
        url3 = "https://www.guokr.com/beta/proxy/science_api/articles?retrieve_type=by_category&page=2"
        headers = {'Referer': 'https://www.guokr.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "guokr.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = etree.HTML(r.text.replace("<span class=\"split\">|</span>", ""))
        r2 = requests.get(url2, headers=headers, timeout=(5, 10)).text
        data2 = json.loads(r2)
        r3 = requests.get(url3, headers=headers, timeout=(5, 10)).text
        data3 = json.loads(r3)
        list = []
        jsondict = {}
        jsondict['website'] = 'guokr'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "果壳-科学人"
        for soup_a in soup.xpath("//a[@class='article-title']"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.get('href')
            group = "guokr"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        for n in data2:
            blist = {}
            hot_url = "https://www.guokr.com/article/" + str(n['id']) + "/"
            hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            group = "guokr"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        for n in data3:
            blist = {}
            hot_url = "https://www.guokr.com/article/" + str(n['id']) + "/"
            hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            group = "guokr"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#虎嗅
def parse_huxiu():
    try:
        url = "https://www.huxiu.com/article/"
        headers = {'Referer': 'https://news.cctv.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "huxiu.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        soup = BeautifulSoup(r.text, 'html.parser')
        list = []
        jsondict = {}
        jsondict['website'] = 'huxiu'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "虎嗅"

        def class_filter(class_text):
            return (class_text is not None) and ((class_text == "article-item--large") or ('article-item--normal' in class_text))

        for soup_a in soup.find_all(class_=class_filter):
            blist = {}
            hot_name = soup_a.find('h5').text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.find('a').get('href')
            if not hot_url.startswith('https://www.huxiu.com'):
                hot_url = 'https://www.huxiu.com' + hot_url
            group = "huxiu"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#cnBeta
def parse_cnbeta():
    try:
        url = "https://www.cnbeta.com/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "cnbeta.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = etree.HTML(r.text)
        list = []
        jsondict = {}
        jsondict['website'] = 'cnbeta'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "cnBeta"
        for soup_a in soup.xpath("//div[@class='items-area']/div/dl/dt/a"):
            blist = {}
            hot_name = soup_a.xpath("./span/text()")
            if hot_name:
                hot_name = hot_name[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            else:
                hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.get('href').replace("//hot", "https://hot").strip()
            group = "cnbeta"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#联合早报-中港台
def parse_zaobao():
    try:
        url = "https://www.zaobao.com.sg/realtime/china"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "zaobao.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = etree.HTML(r.text)
        list = []
        jsondict = {}
        jsondict['website'] = 'zaobao'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "联合早报-中港台"
        for soup_a in soup.xpath("//a[@target='_self']"):
            blist = {}
            hot_name = soup_a.xpath("./div/span/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = "https://www.zaobao.com.sg" + soup_a.get('href').strip()
            group = "zaobao"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#澎湃新闻
def parse_thepaper():
    try:
        url = "https://www.thepaper.cn/load_chosen.jsp"
        headers = {'Referer': 'https://www.thepaper.cn/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "thepaper.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = etree.HTML(r.text)
        list = []
        jsondict = {}
        jsondict['website'] = 'thepaper'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "澎湃新闻"
        for soup_a in soup.xpath("//div[@class='news_li']/h2/a"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = "https://www.thepaper.cn/" + soup_a.get('href')
            group = "thepaper"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#纽约时报中文网-国际简报
def parse_nytimes():
    try:
        url = "https://m.cn.nytimes.com/world"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "nytimes.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = etree.HTML(r.text)
        list = []
        jsondict = {}
        jsondict['website'] = 'nytimes'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "纽约时报中文网-国际简报"
        for soup_a in soup.xpath("//li[@class='regular-item']/a"):
            blist = {}
            hot_name = soup_a.get('title').replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.get('href')
            group = "nytimes"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#solidot
def parse_solidot():
    try:
        url = "https://www.solidot.org/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "solidot.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = etree.HTML(r.text)
        list = []
        jsondict = {}
        jsondict['website'] = 'solidot'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "solidot"
        for soup_a in soup.xpath("//div[@class='bg_htit']/h2/a"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = "https://www.solidot.org" + soup_a.get('href')
            group = "solidot"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#bilibili
def parse_bilibili():
    try:
        from bs4 import BeautifulSoup
        url = "https://www.bilibili.com/v/popular/rank/all"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        fname = dir + "bilibili.json"
        r = requests.get(url, headers=headers, timeout=(5, 10))
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        list = []
        jsondict = {}
        jsondict['website'] = 'bilibili'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "Bilibili"
        for soup_a in soup.find_all("a", "title"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = soup_a.get('href')
            group = "Bilibili"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#新浪科技
def parse_sinatech():
    try:
        url = "https://feed.mix.sina.com.cn/api/roll/get?pageid=372&lid=2431&k=&num=50&page=1"
        headers = {
            'Referer': 'http://tech.sina.com.cn/roll/rollnews.shtml#pageid=372&lid=2431&k=&num=50&page=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        fname = dir + "sinatech.json"
        r = requests.get(url, headers=headers, timeout=(5, 10)).text
        data = json.loads(r)
        list = []
        jsondict = {}
        jsondict['website'] = 'sinatech'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data['result']['data'][0]['ctime'])))
        jsondict["time"] = list_time
        jsondict["title"] = "新浪科技"
        for n in data['result']['data']:
            blist = {}
            hot_url = n['url']
            hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            group = "sinatech"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#全球主机交流论坛
def parse_hostloc():
    try:
        url = "https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        cookies = {
            'hkCM_2132_saltkey': 'YUW6N18j',
            'hkCM_2132_lastvisit': '1565188564',
            'hkCM_2132_visitedfid': '45',
            'L7DFW': 'f64d0d1c0e4afb6b8913e5cf1d39cbf2',
            'hkCM_2132_sid': 'svW2eC',
            'hkCM_2132_st_t': '0%7C1565195462%7Cc9e8fe0fa2043784ed064e22c9180fb3',
            'hkCM_2132_forum_lastvisit': 'D_45_1565195462',
            'hkCM_2132_lastact': '1565195463%09home.php%09misc',
            'hkCM_2132_sendmail': '1'
        }
        fname = dir + "hostloc.json"
        r = requests.get(url, headers=headers, cookies=cookies, timeout=(5, 10)).text.replace("<th class=\"lock\">", "<abc>")
        soup = etree.HTML(r)
        list = []
        jsondict = {}
        jsondict['website'] = 'hostloc'
        list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jsondict["time"] = list_time
        jsondict["title"] = "全球主机交流论坛"
        for soup_a in soup.xpath("//th/a[@onclick='atarget(this)']"):
            blist = {}
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            hot_url = "https://www.hostloc.com/" + soup_a.get('href')
            group = "hostloc"
            blist["name"] = hot_name
            blist["url"] = hot_url
            list.append(blist)
        jsondict["data"] = list
        content = json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',', ':'))
        with open(fname, "w+", encoding='utf-8') as f:
            f.write(content)
    except:
        traceback.print_exc()
        print(sys._getframe().f_code.co_name + "采集错误，请及时更新规则！")


#多线程抓取
def multi_run():
    print("多线程采集开始", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    t1 = time.time()
    threads = []
    threads.append(Thread(target=parse_bilibili))
    threads.append(Thread(target=parse_bjnews))
    threads.append(Thread(target=parse_sinatech))
    threads.append(Thread(target=parse_solidot))
    threads.append(Thread(target=parse_nytimes))
    threads.append(Thread(target=parse_thepaper))
    threads.append(Thread(target=parse_weixin))
    threads.append(Thread(target=parse_zaobao))
    threads.append(Thread(target=parse_cnbeta))
    threads.append(Thread(target=parse_huxiu))
    threads.append(Thread(target=parse_guokr))
    threads.append(Thread(target=parse_douban))
    threads.append(Thread(target=parse_hacpai, args=("play", )))
    threads.append(Thread(target=parse_hacpai, args=("hot", )))
    threads.append(Thread(target=parse_zhihu_daily))
    threads.append(Thread(target=parse_jandan))
    threads.append(Thread(target=parse_chouti))
    threads.append(Thread(target=parse_36kr))
    threads.append(Thread(target=parse_v2ex))
    threads.append(Thread(target=parse_weibo))
    threads.append(Thread(target=parse_baidu, args=("now", )))
    threads.append(Thread(target=parse_baidu, args=("today", )))
    threads.append(Thread(target=parse_baidu, args=("week", )))
    threads.append(Thread(target=parse_zhihu_hot))
    threads.append(Thread(target=parse_zhihu_good))
    threads.append(Thread(target=parse_smzdm_article, args=("today", )))
    threads.append(Thread(target=parse_smzdm_article, args=("week", )))
    threads.append(Thread(target=parse_smzdm_article, args=("month", )))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("多线程采集完成", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("耗时:", time.time() - t1)


if __name__ == "__main__":
    multi_run()
