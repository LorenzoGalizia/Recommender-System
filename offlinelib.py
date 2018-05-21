import csv
import numpy as np
from scipy import spatial


def ratings_matrix_item(dataframe):
    """Create the nested dict for the Item-User matrix. Takes in input the ratings data frame. """
    map = {}
    for row in dataframe.itertuples():
        if row[2] not in map.keys():
            map[row[2]] = {}
            map[row[2]][row[1]] = row[3]
        else:
            map[row[2]][row[1]] = row[3]
    return map

def ratings_matrix_user(dataframe):
    """Create the nested dict for the User-Item matrix. Takes in input the ratings data frame"""
    map = {}
    for row in dataframe.itertuples():
        if row[1] not in map.keys():
            map[row[1]] = {}
            map[row[1]][row[2]] = row[3]
        else:
            map[row[1]][row[2]] = row[3]
    return map

def intersect(dic, key1, key2):
    """Takes in input a nested dict and two keys and returns the intersection between the keys of the internal dicts of
    these keys."""
    k1 = set(dic[key1].keys())
    k2 = set(dic[key2].keys())
    return k1.intersection(k2)

def dict_to_csv(dict, f):
    """Save a nested dict into a CSV file"""
    with open(f , 'w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter='\t')
        for key1 in dict:
            for key2 in dict[key1]:
                csvwriter.writerow([key1, key2, dict[key1][key2]])
    return

def ratings_avg(dic):
    """Return a dictionary with users as keys and ratings' means of each user as values."""
    averages = {}
    for user, rating in dic.items():
        averages[user] = float(sum(rating.values())) / len(rating.values())
    return averages

def adjust_cosine(vote1, vote2, inters, avg):
    """Calculates the adjust cosine between two Items. Takes in input the list of users who have rated both
    Items (inter), the lists of each Item's ratings received from users in common (vote1, vote2) and the dictionary with
    the ratings' average."""
    num = 0
    d1 = 0
    d2 = 0
    for i in range(len(inters)):
        num += (vote1[i] - avg[inters[i]]) * (vote2[i] - avg[inters[i]])
        d1 += (vote1[i] - avg[inters[i]]) ** 2
        d2 += (vote2[i] - avg[inters[i]]) ** 2
    return num / (np.sqrt(d1) * np.sqrt(d2))

def similarity_item(dic, dic_user, f):
    """Create the Items' similarity as a dictionary and save it on a CSV file. Takes in input the two utility matrices,
    and the name of the CSV file."""
    avg = ratings_avg(dic_user)
    sim = {}
    keys = list(dic.keys())
    for k in range(len(keys)):
        for j in range(len(keys)):
            inter = list(intersect(dic, keys[k], keys[j]))
            if keys[j] in sim.keys():
                if keys[k] in sim[keys[j]].keys():
                    if keys[k] not in sim:
                        sim[keys[k]] = {}
                        sim[keys[k]][keys[j]] = sim[keys[j]][keys[k]]
                    else:
                        sim[keys[k]][keys[j]] = sim[keys[j]][keys[k]]
            elif len(inter) <= 1 or k == j:
                pass
            else:
                l = []
                m = []
                for u in inter:
                    l.append(dic[keys[k]][u])
                    m.append(dic[keys[j]][u])
                cos_sim = adjust_cosine(l, m, inter, avg)
                if keys[k] not in sim:
                    sim[keys[k]] = {}
                    sim[keys[k]][keys[j]] = cos_sim
                else:
                    sim[keys[k]][keys[j]] = cos_sim
        dict_to_csv(sim, f)
    return sim


def similarity_user(dic_user, f):
    """Create the Users' similarity as a dictionary and save it on a CSV file. Takes in input the User utility matrix
    and the name of the CSV file."""
    sim = {}
    keys = list(dic_user.keys())
    for k in range(len(keys)):
        for j in range(len(keys)):
            inter = list(intersect(dic_user, keys[k], keys[j]))
            if keys[j] in sim.keys():
                if keys[k] in sim[keys[j]].keys():
                    if keys[k] not in sim:
                        sim[keys[k]] = {}
                        sim[keys[k]][keys[j]] = sim[keys[j]][keys[k]]
                    else:
                        sim[keys[k]][keys[j]] = sim[keys[j]][keys[k]]
            elif len(inter) <= 1 or k == j:
                pass
            else:
                l = []
                m = []
                for item in inter:
                    l.append(dic_user[keys[k]][item])
                    m.append(dic_user[keys[j]][item])
                cos_sim = 1 - spatial.distance.cosine(l, m)
                if keys[k] not in sim:
                    sim[keys[k]] = {}
                    sim[keys[k]][keys[j]] = cos_sim
                else:
                    sim[keys[k]][keys[j]] = cos_sim
        dict_to_csv(sim, f)
    return sim


def split(dic_item,list_Keys):
    """Create a new dictionary from dic_item using only the keys in list_Keys. Takes in input a nested dict and the list
    of keys."""
    dic_tt = {}
    for k  in list(list_Keys):
        dic_tt[k] = dic_item[k]
    return(dic_tt)


def RMSE(real_rat, prev_rat):
    """Calculate the Root Mean Squared Error to evaluate the prevision. Takes in input the two nested dict
    (test and prevision)"""
    real = []
    prev = []
    num = 0
    keys = list(set(real_rat.keys()).intersection(set(prev_rat.keys())))
    for i in keys:
        for j in prev_rat[i].keys():
            if prev_rat[i][j] != 0:
                prev.append(prev_rat[i][j])
                real.append(real_rat[i][j])
    for k in range(len(prev)):
        num += (real[k] - prev[k]) ** 2
    den = len(prev)
    rmse = np.sqrt(num/den)
    return rmse

