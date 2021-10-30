from xml.etree.ElementTree import Element, ElementTree
import csv

csv_list=['actor.csv','film.csv','category.csv','film_actor.csv','film_category.csv']

def beatau(e, level=0):
    if len(e) > 0:
        e.text = '\n' + '\t' * (level + 1)
        child = None
        for child in e:
            beatau(child, level + 1)
        child.tail = child.tail[:-1]
    e.tail = '\n' + '\t' * level


root=Element('root')
def csv_to_xml(file_name):
    #print(file_name)
    with open(file_name,'r',encoding='utf-8') as f:
        reader=csv.reader(f)
        header=next(reader)
        header=header[0]
        header=header.replace('"','').split(';')
        erow = Element(file_name.replace('.csv','')+'_table')
        root.append(erow)
        for row in reader:
            row=row[0].replace('"','').split(';')
            for i in range(len(row)):
                row[i]=row[i].replace('"','')
            erow_id=Element(file_name.replace('.csv',''))
            erow_id.set('{}'.format(header[0]),'{}'.format(row[0]))
            erow.append(erow_id)
            for tag,text in zip(header[1:],row[1:]):
                e=Element(tag)
                e.text=text
                erow_id.append(e)

    beatau(erow)
    beatau(root)
    return

for i in csv_list:
    csv_to_xml(i)

tree=ElementTree(root)
tree.write('main.xml',encoding='utf-8')
