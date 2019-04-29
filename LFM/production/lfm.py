import numpy as np
import sys
sys.path.append('..\\')
import util.reader as read
import operator

def init_model(vector_len):
    return np.random.randn(vector_len)   #标准正态分布

def model_predict(user_vector, item_vector):
    """
    user_vector and item_vector distance
    Args:
        user_vector: model produce user vector
        item_vector: model produce item vector
    Return:
         a num
    """
    res = np.dot(user_vector, item_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
    return res

def lfm_train(train_data, F, alpha, beta, step):
    #train_data: train_data for lfm
    #F:user latent vector len and item latent vector len
    #alpha:regularization factor
    #beta:learning rate
    #step:iteration num
    #return :
    ####dict key itemid, value:itemid_vector
    ####dict key userid, value:userid_vector

    user_vec = {}
    item_vec = {}
    for step_index in range(step):
        print(step_index)
        for data_instance in train_data:
            userid, itemid, label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F)
            if itemid not in item_vec:
                item_vec[itemid] = init_model(F)
            delta = label - model_predict(user_vec[userid], item_vec[itemid])  # 每一轮过程中，每个样本都进行更新
            for index in range(F):
                u_vector_index = user_vec[userid][index]
                i_vector_index = item_vec[itemid][index]
                user_vec[userid][index] += beta * (delta * i_vector_index - alpha * u_vector_index)
                item_vec[itemid][index] += beta * (delta * u_vector_index - alpha * i_vector_index)
        beta = beta * 0.9  # 学习率进行衰减
    return user_vec, item_vec

#产生推荐结果
def give_recom_result(user_vec, item_vec, userid):
    """
    use lfm model result give fix userid recom result
    Args:
        user_vec: lfm model result
        item_vec:lfm model result
        userid:fix userid
    Return:
        a list:[(itemid, score), (itemid1, score1)]
    """
    fix_num = 10
    if userid not in user_vec:
        return []
    record = {}
    recom_list = []
    user_vector = user_vec[userid]
    for itemid in item_vec:
        item_vector = item_vec[itemid]
        res = np.dot(user_vector, item_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
        record[itemid] = res
    for zuhe in sorted(record.items(), key= operator.itemgetter(1), reverse=True)[:fix_num]:
        itemid = zuhe[0]
        score = zuhe[1]
        recom_list.append((itemid, score))
    return recom_list

#分析推荐结果
def ana_recom_result(train_data, userid, recom_list):
    item_info = read.get_movies_info("../data/movies.txt")
    for data_instance in train_data:
        tmp_userid, itemid, label = data_instance
        if tmp_userid == userid and label == 1:
            print(item_info[itemid])
    print("recom result")
    for zuhe in recom_list:
        print(item_info[zuhe[0]])

def model_train_process():
    """
    test lfm model train
    """
    train_data=read.get_train_data("../data/ratings.txt")
    user_vec, item_vec = lfm_train(train_data, 50, 0.01, 0.1, 50) #F=50,正则化参数=0.01，学习率为0.1，迭代次数50
    for userid in user_vec:
        rec_list = give_recom_result(user_vec,item_vec, userid)
        ana_recom_result(train_data, userid, rec_list)


    # for userid in user_vec:
        # recom_result = give_recom_result(user_vec, item_vec, userid)
        #ana_recom_result(train_data, userid, recom_result)

if __name__ == '__main__':
    user_vec, item_vec = model_train_process()
    userid = '1'
    rec_list = give_recom_result(user_vec, item_vec, userid)
    print(rec_list)
    print('---')