import pandas as pd
import importlib as lib

offlib = lib.import_module('offlinelib')

books = pd.read_csv('BX-Books.csv', error_bad_lines=False, encoding="ISO-8859-1", sep=';', warn_bad_lines=False, low_memory=False)
users = pd.read_csv('BX-Users.csv', encoding="ISO-8859-1", sep=';')
ratings = pd.read_csv("BX-Book-Ratings.csv", encoding="ISO-8859-1", sep=';')

"""Remove all the implicit ratings, the Users who have rated less than 8 items and the Items which have been rated less
 than 7 times."""
ratings = ratings[ratings['Book-Rating'] != 0]
lis_us = (ratings['User-ID'].value_counts()).index[ratings['User-ID'].value_counts() > 7]
lis_bk = (ratings['ISBN'].value_counts()).index[ratings['ISBN'].value_counts() > 6]
ratings = ratings[ratings['User-ID'].isin(lis_us)]
ratings = ratings[ratings['ISBN'].isin(lis_bk)]

ratings.to_csv('new_ratings.csv')

"""Create nested dictionary that represent the utility matrix."""
dic_item = offlib.ratings_matrix_item(ratings)
dic_user = offlib.ratings_matrix_user(ratings)

"""Compute the Item-Item similarity."""
similar_item = offlib.similarity_item(dic_item, dic_user, 'itemsimilarity.csv')

"""Compute the User-User similarity"""
similar_user = offlib.similarity_user(dic_user, 'usersimilarity.csv')
