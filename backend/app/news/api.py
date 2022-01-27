import os
import time
import json
import requests
import datetime
import traceback
from threading import Thread
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from app.model.news_model import news as news_table
from app.limiter import limiter
from app.common_func import CommonFunc
from app.login.login_funtion import User
from app.config_helper import ConfigHelper
from app.response import Response as MyResponse
from app.privilege.privilege_control import privilegeFunction
from app.privilege.privilege_control import permission_required
from app.news.get_news import parse_baidu, parse_toutiao, parse_ifanr, parse_dgtle, parse_sspai, parse_zhihu_hot, parse_weibo, parse_v2ex, parse_36kr, parse_chouti, parse_jandan, parse_zhihu_daily, parse_hacpai, parse_douban, parse_guokr, parse_huxiu, parse_cnbeta, parse_zaobao, parse_weixin, parse_thepaper, parse_nytimes, parse_solidot, parse_bilibili, parse_sinatech, parse_bjnews, parse_smzdm_article, parse_zhihu_good

from . import news

rsp = MyResponse()
NEWS_JSON_PATH = ConfigHelper().get('BASE_PATH') + '/backend/app/news/json'
DOMAIN_NAME = ConfigHelper().get('DOMAIN_NAME')
LIMITER_FREQUENCY_NEWS_GET = '10/minute'  # 接口限制的新闻获取访问频次
LIMITER_FREQUENCY_NEWS_FLUSH = '10/hour'  # 接口限制的新闻刷新访问频次


class MyThread(Thread):

    def __init__(self, target, args=()):
        super(MyThread, self).__init__()
        self.target = target
        self.args = args

    def run(self):
        self.result = self.target(*self.args)


@news.route('/get', methods=['POST'])
@limiter.limit(LIMITER_FREQUENCY_NEWS_GET)
def get():
    try:
        if not request.referrer.startswith(DOMAIN_NAME):
            return rsp.refuse(), 403
        csrf_token_send = request.get_json()['token']
        csrf_token = request.cookies.get('csrf_token')
        if csrf_token != csrf_token_send:
            return rsp.refuse(), 403

        temp = {}
        r = []
        files = os.listdir(NEWS_JSON_PATH)
        for file in files:
            file_path = os.path.join(NEWS_JSON_PATH, file)
            temp[file] = json.load(open(file_path))
        r.append({'title': '什么值得买', 'data': [temp.pop('smzdm_article_today.json'), temp.pop('smzdm_article_week.json'), temp.pop('smzdm_article_month.json')]})
        r.append({'title': '知乎', 'data': [temp.pop('zhihu_daily.json'), temp.pop('zhihu_good.json'), temp.pop('zhihu_hot.json')]})
        r.append({'title': '微信', 'data': [temp.pop('weixin_hot.json'), temp.pop('weixin.json')]})
        r.append({'title': '36Kr', 'data': [temp.pop('36kr_hot.json'), temp.pop('36kr_article.json')]})
        r.append({'title': '新京报', 'data': [temp.pop('bjnews_suggestion.json'), temp.pop('bjnews_ranking.json'), temp.pop('bjnews_comment_ranking.json')]})
        r.append({'title': '黑客派', 'data': [temp.pop('hacpai_hot.json'), temp.pop('hacpai_play.json')]})

        for key in temp:
            r.append({'title': temp[key]['title'], 'data': [temp[key]]})

        return rsp.success(r)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@news.route('/flush', methods=['POST'])
@limiter.limit(LIMITER_FREQUENCY_NEWS_FLUSH)
def flush():
    try:
        if not request.referrer.startswith(DOMAIN_NAME):
            return rsp.refuse(), 403
        csrf_token_send = request.get_json()['token']
        csrf_token = request.cookies.get('csrf_token')
        if csrf_token != csrf_token_send:
            return rsp.refuse(), 403

        target = request.get_json()['target']
        if target == 'smzdm_article':
            threads = [MyThread(target=parse_smzdm_article, args=("today", )), MyThread(target=parse_smzdm_article, args=("week", )), MyThread(target=parse_smzdm_article, args=("month", ))]
            file_path = ['smzdm_article_today.json', 'smzdm_article_week.json', 'smzdm_article_month.json']
        elif target == 'zhihu':
            threads = [MyThread(target=parse_zhihu_hot), MyThread(target=parse_zhihu_good), MyThread(target=parse_zhihu_daily)]
            file_path = ['zhihu_daily.json', 'zhihu_good.json', 'zhihu_hot.json']
        elif target == 'weixin':
            threads = [MyThread(target=parse_weixin)]
            file_path = ['weixin_hot.json', 'weixin.json']
        elif target == '36kr':
            threads = [MyThread(target=parse_36kr)]
            file_path = ['36kr_hot.json', '36kr_article.json']
        elif target == 'bjnews':
            threads = [MyThread(target=parse_bjnews)]
            file_path = ['bjnews_suggestion.json', 'bjnews_ranking.json', 'bjnews_comment_ranking.json']
        elif target == 'hacpai':
            threads = [MyThread(target=parse_hacpai, args=("play", )), MyThread(target=parse_hacpai, args=("hot", ))]
            file_path = ['hacpai_hot.json', 'hacpai_play.json']
        else:
            news_dict = {
                'baidu': {'parse_thread':[MyThread(target=parse_baidu)],'file_path':['baidu.json']},
                'toutiao': {'parse_thread':[MyThread(target=parse_toutiao)],'file_path':['toutiao.json']},
                'sspai': {'parse_thread':[MyThread(target=parse_sspai)],'file_path':['sspai.json']},
                'dgtle': {'parse_thread':[MyThread(target=parse_dgtle)],'file_path':['dgtle.json']},
                'ifanr': {'parse_thread':[MyThread(target=parse_ifanr)],'file_path':['ifanr.json']},
                '36kr': {'parse_thread':[MyThread(target=parse_36kr)],'file_path':['36kr.json']},
                'v2ex': {'parse_thread':[MyThread(target=parse_v2ex)],'file_path':['v2ex.json']},
                'huxiu': {'parse_thread':[MyThread(target=parse_huxiu)],'file_path':['huxiu.json']},
                'guokr': {'parse_thread':[MyThread(target=parse_guokr)],'file_path':['guokr.json']},
                'weibo': {'parse_thread':[MyThread(target=parse_weibo)],'file_path':['weibo.json']},
                'zaobao': {'parse_thread':[MyThread(target=parse_zaobao)],'file_path':['zaobao.json']},
                'cnbeta': {'parse_thread':[MyThread(target=parse_cnbeta)],'file_path':['cnbeta.json']},
                'douban': {'parse_thread':[MyThread(target=parse_douban)],'file_path':['douban.json']},
                'jandan': {'parse_thread':[MyThread(target=parse_jandan)],'file_path':['jandan.json']},
                'chouti': {'parse_thread':[MyThread(target=parse_chouti)],'file_path':['chouti.json']},
                'solidot': {'parse_thread':[MyThread(target=parse_solidot)],'file_path':['solidot.json']},
                'nytimes': {'parse_thread':[MyThread(target=parse_nytimes)],'file_path':['nytimes.json']},
                'bilibili': {'parse_thread':[MyThread(target=parse_bilibili)],'file_path':['bilibili.json']},
                'sinatech': {'parse_thread':[MyThread(target=parse_sinatech)],'file_path':['sinatech.json']},
                'thepaper': {'parse_thread':[MyThread(target=parse_thepaper)],'file_path':['thepaper.json']},
            }
            threads = news_dict[target]['parse_thread']
            file_path = news_dict[target]['file_path']
        result = []
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        for file in file_path:
            file_path = os.path.join(NEWS_JSON_PATH, file)
            result.append(json.load(open(file_path)))
        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500

@news.route('/search', methods=['POST'])
@limiter.limit(LIMITER_FREQUENCY_NEWS_GET)
def search():
    try:
        data = request.get_json()
        if not request.referrer.startswith(DOMAIN_NAME):
            return rsp.refuse(), 403
        csrf_token_send = data['token']
        csrf_token = request.cookies.get('csrf_token')
        if csrf_token != csrf_token_send:
            return rsp.refuse(), 403

        keyword = data['keyword']
        start_time = data['start_date'] + ' 00:00:00'
        end_time = data['end_date'] + '59:59:59'

        _ = news_table.select().where((news_table.create_time >= start_time) & (news_table.create_time <= end_time)).where(news_table.content.contains(keyword)).dicts()
        r = [{'website': __['website'], 'category': __['category'], 'content': __['content'], 'create_time': __['create_time'], } for __ in _]
        return rsp.success(r)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500