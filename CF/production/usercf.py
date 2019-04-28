import sys
sys.path.append('..')
import util.reader as reader
import math
import operator
def transfer_user_click(user_click):
    print('fuck')
    item_click_by_user = {}
    for user in user_click:
        item_list = user_click[user]
        for itemid in item_list:
            item_click_by_user.setdefault(itemid, [])
            item_click_by_user[itemid].append(user)
    return item_click_by_user

def base_contribution_score():
    return 1

def update_one_contribute_score(item_user_click_count):
    #item_user_click_count: how man user have clicked this item
    return 1 / math.log2(1 + item_click_by_user)

def update_two_contribution_score(useri_click_time, userj_click_time):
    delta = math.fabs(useri_click_time - userj_click_time)
    norm_num = 60 * 60 * 24
    delta = delta / norm_num #把时间戳转化为时间
    return 1 / (1 + delta)

def cal_user_sim(item_click_by_user, user_click_time):
    co_appear = {}
    user_click_times = {}
    for itemid, user_list in item_click_by_user.items():

        for user_i in range(0, len(user_list)):
            useri = user_list[user_i]
            user_click_times.setdefault(useri, 0)
            user_click_times[useri] += 1
            useri_click_time = user_click_time[useri + '_' + itemid]    #找出useri对itemi的点击时间
            for user_j in range(user_i+1,len(user_list)):

                userj = user_list[user_j]
                userj_click_time = user_click_time[userj + '_' + itemid]  # 找出userj对itemi的点击时间
                co_appear.setdefault(useri, {})
                co_appear[useri].setdefault(userj,0)
                # co_appear[useri][userj] += base_contribution_score()
                '''
                降低那些异常活跃的物品对用户相似度的贡献
                ua,ub:新华字典(热门物品)
                uc,ud:机器学习
                #co_appear[useri][userj] += update_one_contribution_score(len(user_lsit))
                '''
                # co_appear[useri][userj] += update_one_contribution_score(len(user_lsit))
                co_appear[useri][userj] += update_two_contribution_score(useri_click_time, userj_click_time)
                co_appear.setdefault(userj, {})
                co_appear[userj].setdefault(useri,0)
                # co_appear[userj][useri] += base_contribution_score()
                # co_appear[userj][useri] += uodate_one_contribution_score(len(user_lsit))
                co_appear[userj][useri] += update_two_contribution_score(userj_click_time, useri_click_time)
    user_sim_info = {}
    user_sim_info_sorted = {}
    for user_i,relate_user in co_appear.items():
        user_sim_info.setdefault(user_i, {})
        for user_j,cotime in relate_user.items():
            user_sim_info[user_i].setdefault(user_j, 0)
            user_sim_info[user_i][user_j] = cotime / math.sqrt(user_click_times[user_i] * user_click_times[user_j])

    for user in user_sim_info:
        user_sim_info_sorted[user] = sorted(user_sim_info[user].items(), key=operator.itemgetter(1), reverse=True)

    return user_sim_info_sorted

def cal_recom_result(user_click, user_sim,item_click_by_user):
    rec_result = {}
    topk_user = 3
    item_num = 5
    Rui = 1
    for userid,item_list in user_click.items():

        user_relate_list = user_sim[userid][:topk_user] #[(useri,score1), (userj,score2)]
        rec_result.setdefault(userid, {})
        for item in item_click_by_user:  #遍历所有物品
            if item in item_list:
                continue
            rec_result[userid].setdefault(item, 0)

            for relate_user in user_relate_list:
                if item not in user_click[relate_user[0]][:item_num]:
                    continue
                rec_result[userid].setdefault(item, 0)
                rec_result[userid][item] += relate_user[1] * Rui
    return rec_result

def debug_user_sim(user_sim):
    topk = 5
    fix_user = '1'
    if fix_user not in user_sim:
        print('invalid user')
        return
    for relate_user in user_sim[fix_user][:topk]:
        userid, score = relate_user
        print(fix_user + '\tuser_sim' + userid + '\t' + str(score))

def debug_rec_result(item_info, rec_result):
    fix_user = '1'
    if fix_user not in rec_result:
        print('invalid user for recoming result')
        return
    for itemid in rec_result[fix_user]:
        if itemid not in item_info:
            continue
        rec_score = rec_result[fix_user][itemid]
        print('rec_result' + ','.join(item_info[itemid]) + '\t' + str(rec_score))

if __name__ == '__main__':
    user_click, user_click_time = reader.get_user_like('../data/ratings.txt')
    item_info = reader.get_movie_info('../data/movies.txt')
    item_click_by_user = transfer_user_click(user_click)
    user_sim = cal_user_sim(item_click_by_user, user_click_time)
    print(item_info)
    # print('user_sim',user_sim)
    rec_result = cal_recom_result(user_click,user_sim,item_click_by_user)
    # print(rec_result['1'])
    debug_user_sim(user_sim)
    debug_rec_result(item_info, rec_result)




