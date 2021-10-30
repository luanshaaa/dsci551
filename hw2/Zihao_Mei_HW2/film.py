import sys
from lxml import etree
import time
if(len(sys.argv)==1):
    print("missing category name")
    exit()
else:
    category=sys.argv[1]

category=category.title()


tree=etree.parse(open('main.xml'))

category_ids=tree.xpath('/root/category_table/category[name/text()="'+category+'"]/@category_id')
if(len(category_ids)==0):
    print("No results found.")
    exit()
film_ids=tree.xpath('/root/film_category_table/film_category[category_id/text()='+category_ids[0]+']/@film_id')
kes=[]
for film_id in film_ids:
    title=tree.xpath('/root/film_table/film[@film_id="'+film_id+'"]/title/text()')
    release_year=tree.xpath('/root/film_table/film[@film_id="'+film_id+'"]/release_year/text()')
    rating = tree.xpath('/root/film_table/film[@film_id="'+film_id+'"]/rating/text()')
    rental_rate = tree.xpath('/root/film_table/film[@film_id="'+film_id+'"]/rental_rate/text()')
    rental_duration = tree.xpath('/root/film_table/film[@film_id="'+film_id+'"]/rental_duration/text()')
    kes.append((title[0],release_year[0],rating[0],rental_rate[0],rental_duration[0]))
kes.sort(key=lambda x:x[0])
for i in kes:
    print(i)

