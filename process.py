# -*- coding: utf-8 -*-
import time

# 73947987|18249513856|502855139
# userid|phone number|movie=id
favoriates = open('/Volumes/DataDisk/Migu/favorites.csv').readlines()

#197141748|615780287|1454336138274
# useid|movieid|timestamp
playhistories = open('/Volumes/DataDisk/Migu/playhistory.csv').readlines()

#userid|movieid|score|comment
comments = open('/Volumes/DataDisk/Migu/comment.csv').readlines()

#0::21::1
favoriate_rating = 10
rating_all = open('/Volumes/DataDisk/Migu/rating_all_1.txt', 'w')
count = 0

users = set()
movies = set()
actions = []
ratings = 0
comment_count = 0
bad_comments = ['不好','不好看','浪费','垃圾','无语','难看','变态','浮夸','无聊']
good_comments = ['好看','不错','可爱','喜欢','经典','期待','棒','酷','出色','好','非常好', '爽', '精彩','支持','帅']


#user_file = open('/Volumes/DataDisk/Migu/users.csv', 'w')
#movie_file = open('/Volumes/DataDisk/Migu/movies.csv', 'w')
action_file = open('/Volumes/DataDisk/Migu/migu.csv', 'w')

def rate_comment(comment):
    for item in bad_comments:
        if item in comment:
            return 0
    for item in good_comments:
        if ''.join(['不', item]) in comment:
            return 0
    for item in good_comments:
        if item in comment:
            return 10
    return -1

action_count = 0
action_file.write('userId,movieId,rating,timestamp\n')

def process(userid, movieid, score):
    if userid == '\N' or userid == '' :
        return
#   if int(userid) % 100 ==1:
    users.add(userid)
    if movieid == '\N' or movieid == '':
        return

    if not movieid in movie_matches:
        return
#    if int(movieid) % 100 == 1:
    movies.add(movieid)
#    if int(movieid) % 100 == 1 and int(userid) % 100 ==1:

    action_file.write(','.join([userid,movieid, score, str(int(time.time()))]))
    action_file.write('\n')
    global action_count
    action_count += 1
    if action_count % 10000 == 0:
        print ('action_count', action_count)


movie_matches =[]
def load_movie_matches():
    movie_matches_file = open('./migu_lookup.csv')
    for line in movie_matches_file.readlines():
        parts = line.split(',')
        movie_matches.append(parts[1])

load_movie_matches()


favoriate_count = 0
for favoriate in favoriates:
    parts = favoriate.strip().split('|')
    userid = parts[0]
    movieid = parts[2]
    process(userid , movieid, '4')
    favoriate_count += 1
    if favoriate_count % 10000 == 0:
        print ('favorite_count', favoriate_count)

play_count = 0
for playhistory in playhistories:
    parts = playhistory.strip().split('|')
    userid = parts[0]
    movieid = parts[1]
    process(userid, movieid, '4')
    play_count += 1
    if play_count % 10000 == 0:
        print ('play_count', play_count)

"""
user_file.write('id')
user_file.write('\n')
for user in users:
  #  if (int(user) % 100 == 1):
    user_file.write(user)
    user_file.write('\n')

movie_file.write('id')
movie_file.write('\n')
for movie in movies:
    movie_file.write(movie)
    movie_file.write('\n')

"""


print 'finished processing'


"""
for comment in comments:
    parts = comment.strip().split('|')
    if len(parts)!=4:
        continue
    userid = parts[0]
    movieid = parts[1]
    users[userid] = users.get(userid, 0) + 1
    movies[movieid] = movies.get(movieid, 0) + 1

    score = int(parts[2])
    if score != 0:
        write_rating(userid, movieid, score)
        continue
    score = rate_comment(comment)
    if score != -1:
        write_rating(userid, movieid, score)
        comment_count += 1
"""
