import json
import requests
import sys


if(len(sys.argv)==1):
    print("missing category name")
    exit()
else:
    category=sys.argv[1]

category=category.title()
url='https://test-9165e-default-rtdb.firebaseio.com/film_db1/'+category+'.json?OrderBy="$title"'
r=requests.get(url)

data=json.loads(r.text)
if(data==None):
    print("No results found")
else:
    data=sorted(data.items(),key=lambda x:x[1]["title"])
    for item in data:
        value=item[1]
        res=()
        res+=(value["title"],value["release_year"],value["rating"],value["rental_rate"],value["rental_duration"])
        print(res)