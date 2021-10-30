import json
import requests
import sys


if(len(sys.argv)==1):
    print("missing actor's name")
    exit()
else:
    actor = sys.argv[1]


actor=actor.upper()
url='https://test-9165e-default-rtdb.firebaseio.com/film_db2/'+actor+'.json?OrderBy="$title"'
r=requests.get(url)

data = json.loads(r.text)


ans=[]
if(data==None):
    print("No results found")
else:
    cnt=0
    for item in data:
        values=data[item]
        res=()
        for id in values:
            film=values[id]
            res = (item,film["title"], film["release_year"])
            ans.append(res)

ans=sorted(ans,key=lambda x:(x[0],x[1]))
for i in ans:
    res=(i[1],i[2])
    print(res)
