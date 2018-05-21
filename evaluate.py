import pandas as pd
import importlib as lib
import random
import numpy as np


offlib = lib.import_module('offlinelib')
onlib = lib.import_module('onlinelib')

ratings = pd.read_csv('new_ratings.csv', index_col=0)

q = input("Evaluating Recommender System:\n A) Item-Based \n B) User-Based\n")
print('\n')
print("Evaluating...\n")
print('\n')
if q == "A":
    simil =pd.read_csv('itemsimilarity.csv', sep = '\t', header=None)
    simil.columns = ['ISBN1', 'ISBN2', 'Similarity']

    """Create nested dict for similarity, Item utility matrix and User utility matrix."""
    sim = offlib.ratings_matrix_user(simil)
    dic_item = offlib.ratings_matrix_item(ratings)
    dic_user = offlib.ratings_matrix_user(ratings)

    """For five times calculate the RMSE for test and train randomly chosen."""
    rmse_list = []
    for i in range(5):
        k = len(dic_item.keys()) * 80 // 100
        elements = random.sample(list(dic_item.keys()), k)
        train_l = [x for x in elements]
        test_l = [x for x in list(dic_item.keys()) if x not in elements]
        train = offlib.split(dic_item, train_l)
        test = offlib.split(dic_item, test_l)
        prev = onlib.prevision(sim, train, test, dic_user, 5, q)
        rmse_list.append(offlib.RMSE(test, prev))
    RMSE = np.mean(rmse_list)
    print(RMSE)

elif q == 'B':
    simil = pd.read_csv('usersimilarity.csv', sep='\t', header=None)
    simil.columns = ['USER1', 'USER2', 'Similarity']

    """Create nested dict for similarity, Item utility matrix and User utility matrix."""
    sim = offlib.ratings_matrix_user(simil)
    dic_item = offlib.ratings_matrix_item(ratings)
    dic_user = offlib.ratings_matrix_user(ratings)

    """For five times calculate the RMSE for test and train randomly chosen."""
    rmse_list = []
    for i in range(5):
        k = len(dic_user.keys()) * 80 // 100
        elements = random.sample(list(dic_user.keys()), k)
        train_l = [x for x in elements]
        test_l = [x for x in list(dic_user.keys()) if x not in elements]
        train = offlib.split(dic_user, train_l)
        test = offlib.split(dic_user, test_l)
        prev = onlib.prevision(sim, train, test, dic_item, 5, q)
        rmse_list.append(offlib.RMSE(test, prev))
    RMSE = np.mean(rmse_list)
    print(RMSE)

else:
    print('Wrong Input!')