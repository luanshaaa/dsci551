import requests
import csv
import json
import sys


def transforming_data(input_file):
        # read the file
        with open(input_file, "r", encoding='utf-8') as f:
            rows = f.readlines()
        rows = [row.strip() for row in rows]
        attributes = rows[0].split(';')
        num = 1
        all = len(rows)

        # store data
        result = []
        while num < all:
            value = rows[num].split(";")
            result.append(dict(zip(attributes, value)))
            num = num + 1
        # turn python into json
        json_string = json.dumps(result)  # indent=4
        # remove \",\\N,\n ,which are not useful
        answer = json_string.replace(r'\"', '').replace(r'\\N', '').replace(r'\n', '')
        # create a name for the new file
        output_file = input_file.replace("csv", "json")
        # write data into the new file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(answer)
        return [answer,output_file]

def merge_file_db1():
    input_file="category.json"
    category_data=open(input_file,'r')
    category_data=json.load(category_data)
    #print(category_data)

    categories={}
    for item in category_data:
        categories[item["name"]]=item["category_id"]
    #print(categories)

    id_data=json.load(open("film_category.json",'r'))
    #print(id_data)

    id_ctof={}
    for item in category_data:
        category_id=item["category_id"]
        id_ctof[category_id]=[]

    for item in id_data:
        film_id=item["film_id"]
        category_id=item["category_id"]
        id_ctof[category_id].append(film_id)


    #在category中找到所有的种类，然后每个种类对应一个categoryid，然后在file——category中找到filmid，然后在film——id中存答案
    #
    film_data=json.load(open("film.json",'r'))
    films={}
    for item in film_data:
        dictii={}
        dictii["title"]=item["title"]
        dictii["release_year"]=item["release_year"]
        dictii["rating"]=item["rating"]
        dictii["rental_rate"]=item["rental_rate"]
        dictii["rental_duration"]=item["rental_duration"]
        films[item["film_id"]]=dictii

    ans={}
    for item in category_data:
        category_name=item["name"]
        ans[category_name]={}

    for category_name in categories:
        category_id=categories[category_name]
        for film_id in id_ctof[category_id]:
            ans[category_name][film_id]=films[film_id]
    r=requests.patch("https://test-9165e-default-rtdb.firebaseio.com/film_db1.json",json=ans)


def merge_file_db2():
    input_file="actor.json"
    actor_data=open(input_file,'r')
    actor_data=json.load(actor_data)
    #print(actor_data)


    id_data=json.load(open("film_actor.json",'r'))
    #print(id_data)

    id_atof={}
    for item in actor_data:
        actor_id=item["actor_id"]
        id_atof[actor_id]=[]



    for item in id_data:
        film_id=item["film_id"]
        actor_id=item["actor_id"]
        id_atof[actor_id].append(film_id)


    #在actor中找到所有的种类，然后每个种类对应一个actor_id，然后在film_actor中找到film_id，然后在film_id中存答案
    #
    film_data=json.load(open("film.json",'r'))
    films={}
    for item in film_data:
        dictii={}
        dictii["title"]=item["title"]
        dictii["release_year"]=item["release_year"]
        films[item["film_id"]]=dictii


    ans={}

    for item in actor_data:
        ans[item["actor_id"]]={}

    for item in actor_data:
        actor_id=item["actor_id"]
        for film_id in id_atof[actor_id]:
            ans[actor_id][film_id]=films[film_id]

    act_name_id={}
    for item in actor_data:
        actor_name=item["first_name"]+" "+item["last_name"]
        act_name_id[actor_name]=[]
    for item in actor_data:
        actor_name = item["first_name"] + " " + item["last_name"]
        act_name_id[actor_name].append(item["actor_id"])
    #print(act_name_id)

    res={}
    for actor_name in act_name_id:
        res[actor_name]={}
    for actor_name in act_name_id:
        ids=act_name_id[actor_name]
        for id in ids:
            res[actor_name][id]=ans[id]

    r=requests.patch("https://test-9165e-default-rtdb.firebaseio.com/film_db2.json",json=res)





infile_lists=["actor.csv","film.csv","category.csv","film_actor.csv","film_category.csv"]
for i in range(5):
    s=transforming_data(infile_lists[i])
    answer,output_file=s[0],s[1]
    t=open(output_file,'r')
    t=json.load(t)
    r=requests.put("https://test-9165e-default-rtdb.firebaseio.com/"+output_file,json=t)

merge_file_db1()
merge_file_db2()