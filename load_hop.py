import rdflib
import random
PREFIX="http://data.linkedmdb.org/"

def out_degree(url):
    g1=rdflib.Graph()
    g1.parse(url)
    # print(g1.)
    deg=0
    actor_id=url.split("/")[-1]
    for s,p,o in g1:
        if PREFIX in p:
            #print(s,p,o)
            deg+=1
    return deg
def weight(url):
    g1=rdflib.Graph()
    g1.parse(url)
    # print(g1.)
    weight_edge=0
    actor_id=url.split("/")[-1]
    for s,p,o in g1:
        if PREFIX in o:
            #print("Object:",o)
            try:
                weight_edge+=out_degree(o)
            except:
                pass
    return weight_edge
def comp(s1):
    return weight(s1)
def main():
    base_url = 'http://data.linkedmdb.org/all/'
    print(" ")
    class_name = input("Enter Class Name: ")
    class_name.lower().strip()

    url = base_url+class_name
    print("\n")
    print("Extracting Data From "+str(url))
    g=rdflib.Graph()
    g.parse(url)
    # print(g.all_nodes())
    entities,actor_id = [],[]
    for s,p,o in g:
        # print(s,p,o)
        if('label' in p):
            #o = o.encode('utf-8')
            # print(o)
            try:
                entity = str(o.split('(')[-2].strip(' '))
                entities.append(entity)
                actor_id.append(s.split("/")[-1])
            except Exception as e:
                print("Error:", e)
    print(" ")
    print("Total "+str(len(entities))+" entities found! Showing first "+str(min(10, len(entities)))+" entities")
    print(" ")
    print(actor_id[:10])
    for i in range(min(len(entities), 10)):
        print(str(i+1)+": ", entities[i])
    print("\n")
    print(base_url[:-4]+"data/"+class_name+"/"+actor_id[0])
    uri_actor_id=[ base_url[:-4]+"data/"+class_name+"/"+actor_id[i] for i in range(len(actor_id))]
    
    print(out_degree(base_url[:-4]+"data/"+class_name+"/"+actor_id[0]))
    print("Weight of first one :",uri_actor_id[0],weight(uri_actor_id[0]))

    uri_actor_id_dict={}
    for i in uri_actor_id:
        uri_actor_id_dict[i]=weight(i)
    
    #writing the dictionary as csv
    import csv
    w = csv.writer(open("actor_id_weight.csv", "w"))
    for key, val in dict.items():
        w.writerow([key, val])
    
    #print("Weight of Highest one :",uri_actor_id[0],weight(uri_actor_id[0]))

if __name__ == '__main__':
    main()