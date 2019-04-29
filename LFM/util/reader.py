#-*-coding:utf8-*-
"""
author:xujian
date:2019****
"""
import os
import operator

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
def get_train_data(input_file):
    if not os.path.exists(input_file):
        return []
    score_dict = get_ave_score(input_file)
    neg_dict = {}
    pos_dict = {}
    train_data = []
    linenum = 0
    score_thr = 4.0
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if userid not in pos_dict:
            pos_dict[userid] = []
        if userid not in neg_dict:
            neg_dict[userid] = []
        if rating >= score_thr:
            pos_dict[userid].append((itemid, 1))
        else:
            score = score_dict.get(itemid, 0)
            neg_dict[userid].append((itemid, score))
    fp.close()
    for userid in pos_dict:
        data_num = min(len(pos_dict[userid]), len(neg_dict.get(userid, [])))
        if data_num > 0:
            train_data += [(userid, zuhe[0], zuhe[1]) for zuhe in pos_dict[userid]][:data_num]
        else:
            continue
        #负采样，平均分由高到低进行排序，是为了采到那些平均分高的，但是该用户打分低的，更能反映出该用户不喜欢该物品
        sorted_neg_list = sorted(neg_dict[userid], key= operator.itemgetter(1), reverse=True)[:data_num]
        train_data += [(userid, zuhe[0], 0) for zuhe in sorted_neg_list]
        # debug ============== userid = '1'
        # if userid == '1':
        #     print(len(pos_dict[userid]))
        #     print(len(neg_dict[userid]))
        #     print(sorted_neg_list)
        # debug ================
    return train_data

if __name__ == "__main__":
    # item_info = get_movie_info("../data/movies.txt")
    #
    # print(len(item_info))
    # print(item_info['1'])
    # print(item_info['11'])
    # score_dict = get_ave_score('../data/ratings.txt')
    train_data = get_train_data('../data/ratings.txt')
    print(len(train_data))
    print(train_data[:20])
    # print(len(score_dict))
    # print(score_dict['31'])





