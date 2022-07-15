import pandas as pd
import pickle
import json
import numpy as np
import string
import re


# For handling the typeError: Object of type int64 is not JSON serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


# Load the preprocessed pickle Dataset
dict_df = pickle.load(file=open(file="updatedDf.pkl", mode="rb"))

# Make dict to pandas DataFrame
df = pd.DataFrame(data=dict_df)

# Load the model
cv_similarity = pickle.load(file=open(file="CV_similarity.pkl", mode="rb"))

# category dictionary to tract the category number
dic_category = {1: 'phone', 2: 'cosmetics', 3: 'computer accessories', 4: 'educational',
                5: 'jewelry', 6: 'wallet', 8: 'toys', 9: 'light', 10: 'cycle', 11: 'cloths',
                12: 'laptop', 13: 'watch', 14: 'chair', 15: 'television', 16: 'fan', 17: 'tools',
                18: 'musical instrument', 19: 'bag', 20: 'car', 21: 'house items', 22: 'electronics'}


# Our product recommended function
def get_productid_categoryid(product_name: str) -> int | dict[str, list]:
    global category_id
    product_id_list = []
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
            pid, product_name = df.loc[i[0], ['id', 'name']]
            category_id = int(df.loc[i[0], 'product_category_id'])
            if product_category_name == dic_category[category_id]:
                product_id_list.append(pid)
            else:
                pass

    except:
        return False

    else:
        try:
            for i in product_id_list:
                product_info['product id'].append(i)
                if category_id in product_info['category id']:
                    pass
                else:
                    product_info['category id'].append(category_id)
        except:
            return False
        else:
            json_data = json.dumps(obj=product_info, cls=NpEncoder)
            return json_data


# Our main function
if __name__ == "__main__":
    productName = input("Enter your product name: ")
    response = get_productid_categoryid(product_name=productName)

    if response:
        print("Recommended product: ", response)
        print(type(response))
    else:
        print("Opps!! Something is wrong!!")
