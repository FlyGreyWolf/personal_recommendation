#-*-coding:utf8-*-
"""
author:xujian
date:2019****
"""
import os


def get_ave_score(input_file):
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}
    score_dict = {}
    with open(input_file, 'r') as f:
        for line in f:
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userid, itemid, rating = item[0], item[1], item[2]
            if itemid not in record_dict:
                record_dict[itemid] = [0, 0.0]
            record_dict[itemid][0] += 1  #某item的点击次数
            record_dict[itemid][1] += float(rating) #某item的总分

    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1] / record_dict[itemid][0], 3)
    return score_dict

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
    # item_info = get_movie_info("../data/movies.txt")
    #
    # print(len(item_info))
    # print(item_info['1'])
    # print(item_info['11'])

    score_dict = get_ave_score('../data/ratings.txt')
    print(len(score_dict))
    print(score_dict['31'])






