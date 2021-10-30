import sys
from lxml import etree
import time

if(len(sys.argv)==1):
    print("missing actor's name")
    exit()
else:
    actor = sys.argv[1]

actor=actor.upper().split()
tree=etree.parse(open('main.xml'))
if(len(actor)==0):
    print("No results found.")
    exit()
actor_ids=tree.xpath('/root/actor_table/actor[first_name/text()="'+actor[0]+'" and last_name/text()="'+actor[1]+'"]/@actor_id')
if(len(actor_ids)==0):
    print("No results found.")
    exit()

film_ids=[]
film_ids_hash={}
for actor_id in actor_ids:
    cur_film_ids=tree.xpath('/root/film_actor_table/film_actor[@actor_id="'+actor_id+'"]/film_id/text()')
    film_ids=film_ids+cur_film_ids
    for i in cur_film_ids:
        film_ids_hash[i]=actor_id

kes=[]
for film_id in film_ids:
    title=tree.xpath('/root/film_table/film[@film_id="'+film_id+'"]/title/text()')
    release_year=tree.xpath('/root/film_table/film[@film_id="'+film_id+'"]/release_year/text()')
    actor_id=film_ids_hash[film_id]
    kes.append((actor_id,title[0],release_year[0]))
kes.sort(key=lambda x:(x[0],x[1]))
for i in kes:
    print((i[1],i[2]))


