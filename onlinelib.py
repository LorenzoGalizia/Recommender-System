from collections import OrderedDict
import random
import numpy as np
import pandas as pd
from scipy import spatial
import importlib as lib

offlib = lib.import_module('offlinelib')


def n_sim(similarity, item, t, q):
    """Returns a dictionary with the similest Items to 'item' as keys and the respective similarities as values. Takes
    in input the dictionary with the similarities, a fixed item and a threshold and the procedure."""
    sim = OrderedDict(sorted(similarity[item].items(), reverse=True, key=lambda x: x[1]))
    dic_sim = {}
    l = list(sim.items())
    if q == "A":
        for k,v in l:
            if v > 0:
                dic_sim[k] = v
            elif len(dic_sim) == t:
                break
    else:
        for k,v in l:
            if v > 0.9:
                dic_sim[k] = v
            elif len(dic_sim) == t:
                break
    return dic_sim

def prevision(similarity, dic_rat, dic_prev, dic_user, t, q):
    """Returns dictionary with the items as keys and the respective predicted ratings as values. Takes in input the
    similarities dict, the train and the test dictionaries and an integer as threshold."""
    test_c = {}
    keys = list(set(dic_prev.keys()).intersection(similarity.keys()))
    for k in keys:
        num = 0
        den = 0
        x = n_sim(similarity, k, t, q)
        l = set(x.keys())
        m = set(dic_rat.keys())
        sim_in_train = m.intersection(l)
        users = list((dic_prev[k].keys()))
        for u in users:
            similbyu = set(dic_user[u].keys()).intersection(sim_in_train)
            if list(similbyu) == []:
                if k not in test_c.keys():
                    test_c[k] = {}
                    test_c[k][u] = 0
                else:
                    test_c[k][u] = 0
            else:
                for j in similbyu:
                    num += similarity[k][j] * dic_user[u][j]
                    den += abs(similarity[k][j])
                if k not in test_c.keys():
                    test_c[k] = {}
                    test_c[k][u] = num / den
                else:
                    test_c[k][u] = num / den
    return test_c


def similarity_user_online(dic_user):
    """Compute the similarity between the user 0 and the other user in the data set. Takes in input the Users' utility
    dictionary."""
    sim = {}
    keys = list(dic_user.keys())
    k = 0
    for j in range(1, len(keys)):
        inter = list(offlib.intersect(dic_user, 0, keys[j]))
        if len(inter) <= 1:
            pass
        else:
            l = []
            m = []
            for item in inter:
                l.append(dic_user[keys[k]][item])
                m.append(dic_user[keys[j]][item])
            cos_sim = 1 - spatial.distance.cosine(l, m)
            if keys[k] not in sim:
                sim[k] = {}
                sim[keys[k]][keys[j]] = cos_sim
            else:
                sim[keys[k]][keys[j]] = cos_sim
    return sim

def new_user(sim, num):
    """Creates a new file CSV which contains the random Items and the respective random ratings for a new User. Takes
    in input the similarity dictionary and an integer."""
    random_rat=[random.randrange(1,10,1) for i in range(int(num))]
    random_item = sorted(random.sample(sim.keys(), int(num)))
    user_x = [0] * int(num)
    df = pd.DataFrame({'A' : user_x ,'ITEM' : random_item,'RATING' :random_rat})
    df.to_csv('new_user.csv', sep = ';', index = False)
    return

def nested_dict(dic):
    """Creates a nested dict for the 0.0 user. Takes in input a dict."""
    nest_dic = {}
    for key, value in dic.items():
        nest_dic[key] = {}
        nest_dic[key][0] = 0
    return nest_dic


