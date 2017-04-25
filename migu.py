# coding=utf8
#!flask/bin/python
from flask import Flask
from flask import request
from random import randint
from flask import jsonify
from random import seed
import unicodecsv
import io
import traceback
import codecs
import textwrap


"""
ID 0
内容编号 1 *
媒资编号 2
节目编号 3
内容简称 4
状态 5
播控状态 6
发布状态 7
内容标题 8 *
内容说明 9 *
是否二次编辑
关键字
推荐标签
明细描述
版权编号
版权对象编号
版权类型
版权归属CP
版权授权日期
版权到期日期
版权地域范围
是否首发
版权完整度
版权稀缺性
版权授权范围
版权是否可输出
资费类型
版权分值
编剧
导演
评分
语言
主演
出品方
播出年代
播出平台
电影形式
豆瓣评分
内容类型
内容形态
上映时间
所属片名
字幕语言
国家及地区"""
rec_dict = {}

app = Flask(__name__)

@app.route('/')
def index():
    return "欢迎使用咪咕推荐系统"


def get_limit():
    limit = (request.args.get('limit'))
    if (limit is None) or (not limit.isdigit()) or int(limit) > 10:
        return 10
    return int(limit)


def print_movie(movie_rec):
    movie = movie_details.get(movie_rec['movie_id'], {'movie_id': movie_rec['movie_id']})
    print movie_rec['movie_id']
    print movie_rec['score']
    print movie.get('title', 'no title')
  #  print movie.get('description', 'no description')
    print  textwrap.fill(movie.get('description', 'no description'), width=201)

    return movie


recommendation_count = 0

@app.route('/migu/api/v1.0/movies/<string:movie_id>/recommendations', methods=['GET'])
def get_movies_recommendations(movie_id):
    limit = get_limit()
    if not movie_id.isdigit():
        response = {
            'status': 'failure',
            'message': 'invalid movie id'
        }
        return jsonify(response)
    recommendations = []
    recs = rec_dict.get(movie_id, [])

    if len(recs) > 0:
        print
        print '=============================================================='
        print_movie(movie_id)
        print '=============================================================='

        print
        for i in range(0, min(limit, len(recs))):
            recommendations.append(print_movie(recs[i]))
            print
        global recommendation_count
        recommendation_count += 1

    response = {
        'status': 'success',
        'method': 'recommend by movies',
        'movie_id': movie_id,
        'limit': limit,
        'recommendations':recommendations,
    }

    return jsonify(response)

@app.route('/migu/api/v1.0/users/<string:user_id>/recommendations', methods=['GET'])
def get_users_recommendations(user_id):
    limit = get_limit()
    recommendations = []
    if not user_id.isdigit():
        response = {
            'status': 'failure',
            'message': 'invalid user id'
        }
        return jsonify(response)

    seed(10000 + int(user_id))
    for i in range(0, limit):
        id = randint(0, 10000)
        recommendations.append(id)
    response = {
        'status': 'success',
        'method': 'recommend by users',
        'user_id': user_id,
        'limit': limit,
        'recommendations':recommendations
    }
    return jsonify(response)

movie_matches = []

movie_for_user = []
def load_recs():
    data_file = open('./movie_for_user')
    recs = data_file.readlines()
    for rec in recs:
        parts = rec.split('\t')
        rec_dict[parts[0]] = []
        rec_pairs = parts[1].split(':')
        for rec_pair in rec_pairs:
            rec_parts = rec_pair.split(',')
            if (len(rec_parts) == 2):
                rec_dict[parts[0]].append({
                    'movie_id':rec_parts[0],
                    'score': rec_parts[1]
                })


def load_recommendations():
    movie_file = open('./movie_matches.csv', 'w')
    data_file = open('./movie_for_movie.csv')
    recommendations  = data_file.readlines()
    found_count = 0
    total_count = 0
    for recommendation in recommendations:
        total_count += 1
        parts = recommendation.split(',')
        if movie_details.has_key(parts[0]):
          #  print movie_details[parts[0]]['title']
            movie_file.write(parts[0])
            movie_file.write(',')
            movie_file.write(movie_details[parts[0]]['title'])
            movie_file.write('\n')
            found_count += 1
            movie_matches.append(parts[0])
        rec_dict[parts[0]] = []
        if len(parts) > 1:
            for i in range(1, len(parts)):
                if parts[i].isdigit() and parts[i] != parts[0] :
                    rec_dict[parts[0]].append(parts[i])

    print total_count
    print found_count

def load_movie_matches():
    movie_matches_file = open('./movie_matches.csv', 'r')
    for movie_match in movie_matches_file.readlines():
        movie_matches.append(movie_match.split(',')[0])


header = []
movie_details = {}
def load_movie_details():
    is_header = True
    details = open("./migu_utf8.csv").readlines()
    for line in details:
        parts = line.split(',')
        if len(parts) > 10:
            movie_id = lookup_dict.get(parts[1], 0)
            if (movie_id != 0):
                movie_details[lookup_dict[parts[1]]] = {
                    'movie_id': movie_id,
                    'title': parts[8],
                    'description': parts[9]
                }
  #  print movie_details


lookup_dict = {}
def load_lookup():
    lookups = open("./migu_lookup_utf8.csv").readlines()

    for line in lookups:
        parts = line.split(',', 2)
        lookup_dict[parts[0]] = parts[1]

if __name__ == '__main__':
    load_lookup()
    load_movie_details()
#    print movie_details['503725068']
#    load_recommendations()
    load_movie_matches()
    load_recs()
    c = app.test_client()
    response = c.get('/test/url')
   """ for movie_id in movie_matches:
        print movie_id
        # print '===================================' + movie_id
        #print_movie(movie_id)
        try:
            response =  c.get('/migu/api/v1.0/movies/' + movie_id + '/recommendations')

        except:
            pass """
    response = c.get('/migu/api/v1.0/movies/' + movie_id + '/recommendations')

    print recommendation_count
    print 'http://127.0.0.1:5000/migu/api/v1.0/movies/503165045/recommendations?limit=10'
    print 'http://127.0.0.1:5000/migu/api/v1.0/users/1/recommendations?limit=10'
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
