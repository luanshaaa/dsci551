from collections import defaultdict
from PIL import Image
from sklearn.metrics import mean_squared_error as mse
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import pyrebase
import requests
import json
import pandas as pd
from pyspark.ml.feature import Interaction, VectorAssembler
from pyspark.ml.feature import ChiSqSelector
from pyspark.sql.session import SparkSession
from pyspark.ml.linalg import Vector, Vectors
from pyspark.sql import Row, functions
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, HashingTF, Tokenizer
import numpy as np

realdatabase = {"irisDataset":"-Mlx-NOWHDKC4_iutpXB"}
model = dict()
num_features = 0
mapp = {0:"Iris-setosa",1:"Iris-versicolor",2:"Iris-virginica"}
def getimagedata():

    data = Image.open('static/Iris_pic.jpg')
    #exifdata = data.getexif()
    #print(exifdata)
    data_size = data.size
    data_format = data.format
    data_mode = data.mode
    dic = {'size':data_size,'format':data_format, 'mode': data_mode}
    return dic
    #print(data)
    #data.read()
    #print(data)
config = {
    'apiKey': "AIzaSyAg3CB1z_DhCGgA6omQCDzl533ea_sAnpA",
    'authDomain': "iris-storage.firebaseapp.com",
    'databaseURL': "https://iris-storage-default-rtdb.firebaseio.com",
    'projectId': "iris-storage",
    'storageBucket': "iris-storage.appspot.com",
    'messagingSenderId': "1018483513024",
    'appId': "1:1018483513024:web:dede1cc256656e73dfff25",
    'measurementId': "G-0VZ3HEPFCT"
}

def access_cloud(get = False):
    config = {
        'apiKey': "AIzaSyAg3CB1z_DhCGgA6omQCDzl533ea_sAnpA",
        'authDomain': "iris-storage.firebaseapp.com",
        'databaseURL': "https://iris-storage-default-rtdb.firebaseio.com",
        'projectId': "iris-storage",
        'storageBucket': "iris-storage.appspot.com",
        'messagingSenderId': "1018483513024",
        'appId': "1:1018483513024:web:dede1cc256656e73dfff25",
        'measurementId': "G-0VZ3HEPFCT"
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    path_on_cloud = "images/trojan.jpg"
    path_on_local = "../media/Iris_pic.png"
    if get == False:
        storage.child(path_on_cloud).put(path_on_local)
    else:
        dic_info = dict()
        img_url = storage.child(path_on_cloud).get_url("af5dc0d5-31d4-48e3-aaad-35a3ed9c374b")
        print(img_url)
    return
access_cloud(True)
#access_cloud()
def get_database_data(): #从realtime database获取数据库
    dataset = []

    URL  = "https://iris-storage-default-rtdb.firebaseio.com/"

    '''for i in range(149):
        resp = requests.get(URL+str(i) + '.json')
        each = json.loads(resp.text)
        each.pop('Id')
        print(type(each))
        for key, val in each.items():
            if key != 'Species':
                each[key] = round(float(each[key]),3)
        dataset.append(each)'''

    resp = requests.get(URL+realdatabase['irisDataset']+'.json')
    #print(resp.text)
    dataset = resp.text
    #print(dataset)
    #return dataset #we have transferred the data to pandas dataframe
    return dataset

get_database_data()
def model_building(URL):
    global model

    resp = requests.get(URL)
    dataset = resp.text
    dataset = json.loads(dataset)
    df = pd.DataFrame(dataset)
    clf = QuadraticDiscriminantAnalysis()
    features = list(df)[1:]
    features = features[:-1]
    clf.fit(df[features], df['indexedLabel'])
    pred = clf.predict(df[features])
    MSE = mse(y_true=df['indexedLabel'], y_pred=pred)
    print(MSE)
    model['model'] = clf
    return MSE
def prediction(string):
    print(string)
    arr = string.split(" ")
    global mapp

    for i in range(len(arr)):
        arr[i] = float(arr[i])
    global model
    if not model:
        return 0
    else:
        clf = model['model']
        pred = clf.predict(np.array([arr]))
        return mapp[int(pred.tolist()[0])]


def gen_json_file():
    df = get_database_data()
    file_name = 'dataset.json'
    f2 = open(file_name, 'w')
    f2.write(df)
    f2.close()
    return file_name

def reconstruct_data(features,df):
    dataset = features.copy()
    dataset.append('Species')
    df = df[dataset]  # 重新构建选定的dataset
    return df


def features_selector(num_fetaures):
    df = get_database_data()
    global num_features
    num_features = num_fetaures
    f2 = open('dataset.json','w')
    f2.write(df)
    f2.close()
    #data = spark.sparkContext/

    spark = SparkSession \
        .builder \
        .appName("Iris_classification") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()

    df = spark.read.json('dataset.json')
    df = df.drop("Id")
    print("Start Creating Spark RDD, waiting...")
    def f(x):
        rel = {}
        rel['features'] = Vectors.dense(float(x[0]),float(x[1]),float(x[2]),float(x[3]),float(x[4]),float(x[5]),float(x[6]))
        rel['label'] = str(x[7])
        return rel
    vc_df = df.rdd.map(lambda p: Row(**f(p))).toDF()

    def ttl_divide_1(row):
        return (row.label,) + tuple(row.features.toArray().tolist())

    col_did = vc_df.rdd.map(ttl_divide_1).toDF(['label'])
    assembler1 = VectorAssembler(inputCols=["_2", "_3", "_4", "_5", "_6", "_7", "_8"], outputCol="vec1")
    assembled1 = assembler1.transform(col_did)
    assembler2 = VectorAssembler(inputCols=["_2", "_3", "_4", "_5", "_6", "_7", "_8"], outputCol="vec2")
    assembled2 = assembler2.transform(assembled1).select("label", "vec1", "vec2")
    interaction = Interaction(inputCols=["vec1", "vec2"], outputCol="interactedCol")

    interacted = interaction.transform(assembled2)

    def ttl_divide_2(row):
        return (row.label,) + tuple(row.vec1.toArray().tolist()) + tuple(row.interactedCol.toArray().tolist())

    col_did = interacted.rdd.map(ttl_divide_2).toDF(['label'])
    #col_did.show(truncate=True)
    print("Choosing Top best featrues...")
    arr = []
    for i in range(2, 58):
        arr.append("_" + str(i))
    assembler1 = VectorAssembler(inputCols=arr, outputCol="features")
    assembled1 = assembler1.transform(col_did)
    full_crossdt = assembled1.select("label", "features")
    labelIndexer = StringIndexer().setInputCol("label").setOutputCol("indexedLabel").fit(full_crossdt)
    # featureIndexer = VectorIndexer().setInputCol("features").setOutputCol("indexedFeatures").fit(vc_df)
    full_crossdt = labelIndexer.transform(full_crossdt)
    converter = IndexToString(inputCol="indexedLabel", outputCol="originalCategory")
    full_crossdt = converter.transform(full_crossdt)
    tmp_df = full_crossdt.select("features", "indexedLabel")
    selector = ChiSqSelector(numTopFeatures=int(num_features), featuresCol="features",
                             outputCol="selectedFeatures", labelCol="indexedLabel")
    result = selector.fit(tmp_df).transform(tmp_df)

    def extract(row):
        return (row.indexedLabel,) + tuple(row.selectedFeatures.toArray().tolist())

    col_did = result.rdd.map(extract).toDF(['indexedLabel'])
    print("ChiSqSelector output with top %d features selected" % selector.getNumTopFeatures())
    result.show()
    to_pd = col_did.select("*").toPandas()


    species_col = df.select('Species').toPandas()
    final_table = pd.concat([to_pd, species_col], axis=1)
    return final_table


def upload_user_table(final_table):
    print(final_table)
    global realdatabase
    js_file = final_table.to_json(orient = 'records')
    URL = "https://iris-storage-default-rtdb.firebaseio.com/.json"
    #a = json.load(file)
    r = requests.post(URL, json=json.loads(js_file))
    if r.status_code != 200:
        print("Response Error!")
        return False
    lc_name = r.text
    lc_name = json.loads(lc_name)
    print("Uploading to database...")
    if 'user_table.json' in realdatabase:
        realdatabase.pop('user_table.json')
    for key, val in lc_name.items():
        realdatabase['user_table.json'] = val
    print(realdatabase)
    return (True,realdatabase)
print(realdatabase)

#final_table = features_selector()
#upload_user_table(final_table)