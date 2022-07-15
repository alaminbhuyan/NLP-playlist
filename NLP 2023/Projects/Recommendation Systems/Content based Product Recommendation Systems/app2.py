import pandas as pd
import pickle
import json
import numpy as np
import string
import re

dict_df = pickle.load(file=open(file="updatedDf.pkl", mode="rb"))

df = pd.DataFrame(data=dict_df)

cv_similarity = pickle.load(file=open(file="CV_similarity.pkl", mode="rb"))

dic_category = {1: 'phone', 2: 'cosmetics', 3: 'computer accessories', 4: 'educational',
                5: 'jewelry', 6: 'wallet', 8: 'toys', 9: 'light', 10: 'cycle', 11: 'cloths',
                12: 'laptop', 13: 'watch', 14: 'chair', 15: 'television', 16: 'fan', 17: 'tools',
                18: 'musical instrument', 19: 'bag', 20: 'car', 21: 'house items', 22: 'electronics'}


def recommendationProduct(product_name: str):
    try:
        product_name = product_name.lower()
        product_index = df[df["name"] == product_name].index[0]
        distances = sorted(list(enumerate(cv_similarity[product_index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:]:
            productID, product_name = df.loc[i[0], ['id', 'name']]
            print(df.loc[i[0], 'name'], "--->", df.loc[i[0], 'categoryName'])
    except Exception as e:
        print(e.__class__)


def specific_product_recommender(product_name: str):
    try:
        product_name = product_name.lower()

        product_id = int(df[df['name'] == product_name]['product_category_id'].values[0])
        product_category_name = dic_category.get(product_id)

        product_index = df[df['name'] == product_name].index[0]
        distances = sorted(list(enumerate(cv_similarity[product_index])), reverse=True, key=lambda x: x[1])

        for i in distances[1:]:
            productID, product_name = df.loc[i[0], ['id', 'name']]
            category_id = int(df.loc[i[0], 'product_category_id'])
            if product_category_name == dic_category[category_id]:
                print(df.loc[i[0], 'name'], "---->", df.loc[i[0], 'categoryName'], ",", "productID: ", productID,
                    "--->", "categoryID: ", category_id)
            else:
                pass
            # print(dic_category[category_id])

    except Exception as e:
        print("Opps!", e.__class__, "occurred.")


def get_productid_categoryid(product_name: str):
    product_id_lis = []
    category_id_lis = set()
    product_info = {
        'product id': [],
        'category id': []
    }
    try:
        product_name = product_name.lower()

        product_id = int(df[df['name'] == product_name]['product_category_id'].values[0])
        product_category_name = dic_category.get(product_id)

        product_index = df[df['name'] == product_name].index[0]
        distances = sorted(list(enumerate(cv_similarity[product_index])), reverse=True, key=lambda x: x[1])

        for i in distances[1:]:
            productID, product_name = df.loc[i[0], ['id', 'name']]
            category_id = int(df.loc[i[0], 'product_category_id'])
            if product_category_name == dic_category[category_id]:
                product_id_lis.append(productID)
                category_id_lis.add(category_id)
            else:
                pass

    except Exception as e:
        print("Opps!", e.__class__, "occurred.")

    else:
        try:
            for i in product_id_lis:
                product_info['product id'].append(i)
                if category_id in product_info['category id']:
                    pass
                else:
                    product_info['category id'].append(category_id)
        except:
            print("something is wrong")
        else:
            result = tuple(zip(product_id_lis, category_id_lis))
            print(product_id_lis)
            print(category_id_lis)
            print(result)


if __name__ == "__main__":
    productName = input("Enter your product name: ")
    recommendationProduct(product_name=productName)
    print("*" * 100)
    specific_product_recommender(product_name=productName)
    print("*" * 100)
    get_productid_categoryid(product_name=productName)
