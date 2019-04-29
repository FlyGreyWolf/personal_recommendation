import sys
sys.path.append('..')
import util.reader as reader
import math
import operator

def base_contribute_score():
    return 1

def update_one_contribute_score(user_total_click_num):
    return 1/math.log2(1+user_total_click_num)

def update_two_contribute_score(click_time_i, click_time_j):
    delata_time = abs(click_time_j - click_time_i)
    total_sec = 60*60*24
    delata_time = delata_time / total_sec
    return 1/(1+delata_time)

def cal_item_sim(user_like):
    co_appear = {}
    item_click_times = {}
    for user, item_list in user_like.items():
        for i in range(0, len(item_list)):
            item_i = item_list[i]
            item_click_times.setdefault(item_i, 0)  #if item_click_times not includes the item , set 0,else go on
            item_click_times[item_i] += 1
            co_appear.setdefault(item_i,{})
            for j in range(i+1, len(item_list)):
                item_j = item_list[j]
                co_appear[item_i].setdefault(item_j, 0)
                co_appear[item_i][item_j] += base_contribute_score()
                # co_appear[item_i][item_j] += update_one_contribute_score(len(itemlist))

                co_appear.setdefault(item_j, {})
                co_appear[item_j].setdefault(item_i, 0)
                co_appear[item_j][item_i] += base_contribute_score()
                # co_appear[item_j][item_i] += update_one_base_contribute_score(len(itemlist))


    item_sim_score = {}
    item_sim_score_sorted = {}
    for item_i, relate_item in co_appear.items():
        for item_j ,co_time in relate_item.items():
            sim_score = co_time / math.sqrt(item_click_times[item_i]*item_click_times[item_j])
            item_sim_score.setdefault(item_i, {})
            item_sim_score[item_i].setdefault(item_j, 0)
            item_sim_score[item_i][item_j] = sim_score

    #相似度按从大到小排列
    for item_i in item_sim_score:
        item_sim_score_sorted[item_i] = sorted(item_sim_score[item_i].items(), key=operator.itemgetter(1), reverse=True)

    return item_sim_score_sorted

def cal_rec_result(user_like, sim_info):
    recent_like = 3 #choose the user recent like
    rec_info = {} #recommendation result
    topk = 5
    rencent_like = 3
    Rui = 1  #user u   item i   loving degree
    for userid in user_like:
        like_list = user_like[userid][:rencent_like] #get user recent 3 favorite movies
        rec_info.setdefault(userid, {})

        for item_j in sim_info:
            if item_j in like_list:     #reoommend the movie that not in user's recent 3 favorite movies for the user
                continue
            for item_i in sim_info[item_j][:topk]:  #item[0]:item_id,  item[1]:sim
                if item_i[0] in like_list:
                    rec_info[userid].setdefault(item_j, 0)
                    rec_info[userid][item_j] += item_i[1] * Rui
    return rec_info

if __name__ == '__main__':
    user_like, user_rate_time = reader.get_user_like("../data/ratings.txt")
    sim_info = cal_item_sim(user_like)
    rec_result = cal_rec_result(user_like,sim_info)
    print(rec_result["1"])
    print(sim_info['1356'])
    print(sim_info['968'])
    print(sim_info['1343'])



