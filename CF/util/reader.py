#-*-coding:utf8-*-
"""
author:xujian
date:2019****
"""
import os

#get all user favorite movies_id
#user_like      ->      user_id:movie_id
#user_rate_time  ->  user_id _movie_id  : rate_time
def get_user_like(rating_file):
    if not os.path.exists(rating_file):
        return {},{}
    read_row = 0
    from_row = 0
    user_like = {}
    user_rate_time = {}

    with open(rating_file, 'r') as f:
        for line in f:
            if(read_row == from_row):
                read_row += 1
                continue
            user_info = line.strip().split(',')
            if (len(user_info) < 3):
                continue
            [user_id, movie_id, rating, timestamp] = user_info
            if user_id + "_" + movie_id not in user_rate_time:
                user_rate_time[user_id + "_" + movie_id] = int(timestamp)
            if float(rating) < 3.0:
                continue
            if user_id not in user_like:
                user_like[user_id] = []
            user_like[user_id].append(movie_id)
    return user_like, user_rate_time

#get all movie_info
#movie_info_map   ->    movie_name:movie_genres
def get_movie_info(movie_info_file):
    if not os.path.exists(movie_info_file):
        return {}
    read_row = 0
    from_row = 0
    movie_info_map = {}
    with open(movie_info_file, 'r') as f:
        for line in f:
            if (read_row == from_row):
                read_row += 1
                continue

            movie_info = line.strip().split(',')

            if (len(movie_info) < 3):
                continue
            movie_id, genres = movie_info[0], movie_info[-1]    #-1 means the last value of the array
            if(len(movie_info) == 3):
                movie_name = movie_info[1]
            else:
                movie_name =  ",".join(movie_info[1:-1])     #if movie name includes the ","
            if movie_id not in movie_info_map:
                movie_info_map[movie_id] = [movie_name, genres]
    return movie_info_map

if __name__ == "__main__":
    user_like, user_rate_time = get_user_like("../data/ratings.txt")
    # print(len(user_like))
    # print(user_like["1"])
    # #print user_click["1"]
    # item_info= get_movie_info("../data/movies.txt")
    # print(item_info["11"])






