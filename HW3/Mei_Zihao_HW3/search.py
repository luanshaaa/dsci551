import mysql.connector

cnx=mysql.connector.connect(user='dsci551',password='Dsci-551',host='127.0.0.1',database='sakila')

cursor=cnx.cursor()

query="select FID,title,actors from nicer_but_slower_film_list where actors like '%Temple%' order by FID"

cursor.execute(query)

cnt=0
for name in cursor:
    cnt += 1

print(cnt, "films in total.\n")
cursor.execute(query)
for item in cursor:
    res=item[2].split(',')
    cur_sum=0
    ans=[]
    for c in res:
        if("Temple" in c):
            cur_sum+=1
            ans.append(c)
    s=""
    for i in range(len(ans)-1):
        s+=ans[i]+" and "
    s+=ans[-1]
    if(cur_sum>1):
        s+=" play "
    else:
        s+=" plays "
    s+=item[1]+"("+str(item[0])+")"
    print(s)
cursor.close()
cnx.close()
