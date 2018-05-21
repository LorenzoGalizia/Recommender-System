import webbrowser
import pandas as pd
import importlib as lib
import copy
import re

offlib = lib.import_module('offlinelib')
onlib = lib.import_module('onlinelib')

ratings = pd.read_csv('new_ratings.csv', index_col=0)
books = pd.read_csv('BX-Books.csv', error_bad_lines=False, encoding="ISO-8859-1", sep=';', warn_bad_lines=False, low_memory=False)

simil =pd.read_csv('itemsimilarity.csv', sep = '\t', header=None)
simil.columns = ['ISBN1', 'ISBN2', 'Similarity']

sim = offlib.ratings_matrix_user(simil)
dic_item = offlib.ratings_matrix_item(ratings)
dic_user = offlib.ratings_matrix_user(ratings)

q = input("Type of Recommender System:\n A) Item-Based \n B) User-Based\n")


def online(sim_mat, dic, dic_user, t, df_books, q):
    """Online procedure for recommendation. Takes in input the similarity dictionary, the Item-User dictionary, the
    User-Item dictionary, a threshold and the books' data frame and the procedure."""
    num = input('How many books have you rated?\n')
    n = int(input('How many books do you want? '))
    print('\n')
    print("Loading your Recommendation...\n")
    onlib.new_user(sim_mat, int(num))
    rat_user = pd.read_csv('new_user.csv', sep=';', dtype={'ITEM': object})
    dic_rat_user = offlib.ratings_matrix_user(rat_user)
    if q == 'A':
        dic_tot = {}
        items = list(dic_rat_user[0].keys())
        for item in items:
            ds = onlib.n_sim(sim_mat, item, t, q)
            for k, v in ds.items():
                if k not in dic_tot.keys():
                    dic_tot[k] = v
                elif k in dic_tot.keys() and v < dic_tot[k]:
                    pass
                else:
                    dic_tot[k] = v
        nest_dic = onlib.nested_dict(dic_tot)
        new_dic_user = copy.deepcopy(dic_user)
        new_dic_user.update(dic_rat_user)
        prev = onlib.prevision(sim_mat, dic, nest_dic, new_dic_user, t, q)
        item_rec = sorted(prev.keys(), key=lambda x: prev[x][0], reverse=True)
    else:
        new_dic_user = copy.deepcopy(dic_user)
        new_dic_user.update(dic_rat_user)
        sim_nu = onlib.similarity_user_online(new_dic_user)
        if sim_nu == {}:
            print('Sorry no match found!')
        else:
            newu = 0
            ds = onlib.n_sim(sim_nu, newu, t, q)
            us_sim = ds.keys()
            l_item = []
            for u in us_sim:
                if l_item == []:
                    l_item = list(new_dic_user[u].keys())
                else:
                    l_item += list(new_dic_user[u].keys())
            user_zero = {}
            k = 0
            for item in l_item:
                if user_zero == {}:
                    user_zero[0] = {}
                    user_zero[0][item] = 0
                else:
                    user_zero[0][item] = 0
            for item in list(user_zero[0].keys()):
                prev = 0
                numer = 0
                denom = 0
                for user in us_sim:
                    if user in list(dic_item[item].keys()):
                        numer += ds[user] * dic_item[item][user]
                        denom += ds[user]
                    else:
                        pass
                prev = numer / denom
                user_zero[0][item] = prev
            item_rec = sorted(user_zero[0].keys(), key=lambda x: user_zero[0][x], reverse=True)
    k = 0
    print('\n')
    for item in item_rec:
        if item in list(df_books['ISBN'].values):
            print(k + 1, ') ', df_books[df_books['ISBN'] == item]['Book-Title'].values[0], ' - ',
                  df_books[df_books['ISBN'] == item]['Book-Author'].values[0], ' - ',
                  item)
        else:
            print(k + 1, ') Sorry! No information for this book: ', item)
        k += 1
        if k == n:
            break
    if k < n:
        print("\n")
        print("Sorry! I don't have enough information to suggest you %d items." % n)
    print('\n')
    print(
        "Would you like to:\n A) Buy a book.\n B) Get informations on the book's author.\n C) Get the plot.\n D) Exit")
    q1 = input()
    if q1 == 'A':
        q2 = input('Please insert the ISBN: ')
        webbrowser.open("https://www.bookgoodies.com/a/%s" % q2)
    elif q1 == 'B':
        q2 = input('Please insert the ISBN: ')
        author = df_books[df_books['ISBN'] == q2]['Book-Author'].values[0]
        author = author.lower()
        author = author.title()
        author = author.replace(' ', '_')
        webbrowser.open("https://en.wikipedia.org/wiki/%s" % author)
    elif q1 == 'C':
        q2 = input('Please insert the ISBN: ')
        name = df_books[df_books['ISBN'] == q2]['Book-Title'].values[0]
        sep1 = '('
        sep2 = ':'
        name = name.split(sep1, 1)[0]
        name = name.split(sep2, 1)[0]
        name = name.lower()
        name = name.replace('&amp;', "&")
        name = re.sub(r"\b(?<!')[a-z]", lambda m: m.group().upper(), name)
        name = name.replace('\\', '')
        name = name.replace('"', "")
        name = name.replace(" ", "_")
        webbrowser.open("https://en.wikipedia.org/wiki/%s#Plot" % name)
    return



online(sim, dic_item, dic_user, 5, books, q)
