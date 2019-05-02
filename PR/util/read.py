import os
import operator
import mat_util as mat_util
from scipy.sparse.linalg import gmres
import numpy as np

def get_graph_from_data(input_file):
    """
    Args:
        input_file:user item rating file
    Return:
        a dict: {UserA:{itemb:1, itemc:1}, itemb:{UserA:1}}
    """
    if not os.path.exists(input_file):
        return {}
    graph = {}
    linenum = 0
    score_thr = 4.0
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 3:
            continue
        userid, itemid, rating = item[0], "item_" + item[1], item[2]
        if float(rating) < score_thr:
            continue
        if userid not in graph:
            graph[userid] ={}
        graph[userid][itemid] = 1
        if itemid not in graph:
            graph[itemid] = {}
        graph[itemid][userid] = 1
    fp.close()
    return graph


def get_item_info(input_file):
    """
    get item info:[title, genre]
    Args:
        input_file:item info file
    Return:
        a dict: key itemid, value:[title, genre]
    """
    if not os.path.exists(input_file):
        return {}
    item_info = {}
    linenum = 0
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemid, title, genre = item[0], item[1], item[2]
        elif len(item) > 3:
            itemid = item[0]
            genre = item[-1]
            title = ",".join(item[1:-1])
        item_info[itemid] = [title, genre]
    fp.close()
    return item_info

def personal_rank(graph, root, alpha, iter_num, rec_num=10):
    node_dict = {}
    node_dict = {node:0 for node in graph}
    update_dict = node_dict.copy()
    node_dict[root] = 1
    # print('update_dict', update_dict)
    # print('node_dict', node_dict)
    rec_result = {}

    for i in range(iter_num):
        for node in graph:
            for node_out in graph[node]:
                update_dict[node_out] += 1 / len(graph[node]) * node_dict[node] * alpha

        update_dict[root] += (1 - alpha)
        node_dict = update_dict.copy()
        update_dict = {node:0 for node in graph}

    right_num = 0
    for zuhe in sorted(node_dict.items(), key=operator.itemgetter(1), reverse=True):
        node, pr_score = zuhe[0], zuhe[1]
        if len(node.split('_')) != 2:  #判断是否为物品
            continue
        if node in graph[root]:        #判断物品是否在该用户的行为过的列表中
            continue
        rec_result[node] = pr_score
        right_num += 1
        if right_num > rec_num:
            break
    return rec_result

def personal_rank_mat(graph, root, alpha, recom_num = 10):
    """
    Args:
        graph:user item graph
        root:the fix user to recom
        alpha:the prob to random walk
        recom_num:recom item num
    Return:
        a dict, key: itemid, value: pr score
    A*r = r0
    """
    m, vertex, address_dict = mat_util.graph_to_m(graph)
    if root not in address_dict:
        return {}
    score_dict = {}
    recom_dict = {}
    mat_all = mat_util.mat_all_point(m, vertex, alpha)

    index = address_dict[root]
    initial_list = [[0] for row in range(len(vertex))]
    initial_list[index] = [1]
    r_zero = (1-alpha)*np.array(initial_list)
    res = gmres(mat_all, r_zero, tol=1e-8)[0]
    for index in range(len(res)):
        point = vertex[index]
        if len(point.strip().split("_")) < 2:
            continue
        if point in graph[root]:
            continue
        score_dict[point] = res[index]
    for zuhe in sorted(score_dict.items(), key = operator.itemgetter(1), reverse= True)[:recom_num]:
        point, score = zuhe[0], zuhe[1]
        recom_dict[point] = score
    print(recom_dict)
    return recom_dict

if __name__ == "__main__":
    user = '1'
    graph =  get_graph_from_data("../data/ratings.txt")
    rec_result = personal_rank(graph, user, alpha=0.6, iter_num=20,rec_num=100)
    rec_result_mat = personal_rank_mat(graph, user, alpha=0.6, recom_num=100)  #利用矩阵求解的
    item_info = get_item_info("../data/movies.txt")
    print('用户' + user + '喜欢的')
    for itemid in graph[user]:
        pure_itemid = itemid.split('_')[1]
        print(item_info[pure_itemid])
    print('推荐结果')
    for itemid in rec_result:
        pure_itemid = itemid.split('_')[1]
        print(item_info[pure_itemid], rec_result[itemid])
    print('矩阵求解的推荐结果')
    for itemid in rec_result_mat:
        pure_itemid = itemid.split('_')[1]
        print(item_info[pure_itemid], rec_result_mat[itemid])

    num = 0 #用于计算两种计算方法的推荐结果中有多少是相同的
    for ele in rec_result:
        if ele in rec_result_mat:
            num += 1
    print(num)


