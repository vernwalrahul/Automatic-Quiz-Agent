import rdflib
import random

def main():
    base_url = 'http://data.linkedmdb.org/all/'
    print(" ")
    class_name = raw_input("Enter Class Name: ")
    class_name.lower().strip(' ')

    url = base_url+class_name
    print("\n")
    print("Extracting Data From "+str(url))
    g=rdflib.Graph()
    g.load(url)

    entities = []
    for s,p,o in g:
        if('label' in p):
            o = o.encode('utf-8')
            # print(o)
            try:
                entity = str(o.split('(')[-2].strip(' '))
                entities.append(entity)
            except:
                pass
    print(" ")
    print("Total "+str(len(entities))+" entities found! Showing first "+str(min(10, len(entities)))+" entities")
    print(" ")
    for i in range(min(len(entities), 10)):
        print(str(i+1)+": ", entities[i])
    print("\n")

if __name__ == '__main__':
    main()