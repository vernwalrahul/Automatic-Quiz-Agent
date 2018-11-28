import rdflib
#import random
import csv
import pickle
KnowledgeGraph={}
#Dictionary of {"s":["LABEL","TYPE",list[(("o",type_of_o),list["p"])]]} object and list of predicates hashed with respect to 
# #hop distance 
PREFIX="http://data.linkedmdb.org/"
LABEL,TYPE,GRAPH=0,1,2
def save_obj(obj, name ):
    with open('./'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def write_to_csv(uri_actor_id,class_name):
    uri_actor_id_dict={}
    row = 1
    temp_file=open("temp_csv.csv","a")
    temp_csv = csv.writer(temp_file)
    for i in uri_actor_id:
        try:
            uri_actor_id_dict[i]=out_degree(i)
            temp_csv.writerow([row,i,uri_actor_id_dict[i]])
            temp_file.flush()
            print(row,i,uri_actor_id_dict[i])
            row = row+1
        except:
            pass
    #writing the dictionary as csv
    w = csv.writer(open(class_name+"_weight.csv", "w"))
    for key, val in dict.items():
        w.writerow([key, val])

def out_degree(url):
    deg=0
    if PREFIX in url:
        g1=rdflib.Graph()
        g1.parse(url)
        # print(g1.)
        actor_id=url.split("/")[-1]
        for s,p,o in g1:
            if PREFIX in p:
                #print(s,p,o)
                deg+=1
    return deg
"""For computing the weight based weight[u]=sum([outdegree[v] for v in OUT(u)])
"""
def weight(url):
    g1=rdflib.Graph()
    g1.parse(url)
    # print(g1.)
    weight_edge=0
    if PREFIX in url:
        g1=rdflib.Graph()
        g1.parse(url)
        # print(g1.)
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
def FindLabel(url):
    g=rdflib.Graph()
    g.parse(url)
    O,S=None,None
    for s,p,o in g:
        if('dc' in p) and ('title' in p):
            try:
                return str(o),s.split("/")[-2]
            except:
                pass
    return O,S
def fn(URI):
    return out_degree(URI[0])
def URLQuestionsCompute(url,URLname,URLid):
    g1=rdflib.Graph()
    g1.parse(url)
    print("Start")
    if PREFIX not in url:
        return
    #Helper function
    def isdigit(string):
        try:
            string=int(string)
            return True
        except:
            return False
    #For a given url entity two types of questions can be generated
    # s,p,o where s is url or o is url,p is the connective between them
    for s,p,o in g1:
        if (str(URLid) in o) and (PREFIX in s) and isdigit(s.split("/")[-1]):
            try:
                #print("This is p : ",p)
                label_S,type_P=FindLabel(s)
                if label_S:
                    KnowledgeGraph[URLname][GRAPH].append(((label_S,type_P),p.split("/")[-1]))
            except Exception as e:
                print("Error: ",e)
        if (str(URLid) in s) and (PREFIX in o) and isdigit(o.split("/")[-1]):
            try:
                label_O,type_P=FindLabel(o)
                if label_O:
                    KnowledgeGraph[URLname][GRAPH].append(((label_O,type_P),p.split("/")[-1]))
            except Exception as e:
                print("Error: ",e)

def RankEntitiesBasedOnClass(base_url,class_name):
    class_name.lower().strip()
    url = base_url+class_name
    print("\n")
    print("Extracting Data From "+str(url))
    g=rdflib.Graph()
    g.parse(url)
    entities,entity_id,type_of_entity = [],[],None
    for s,p,o in g:
        if('label' in p):
            try:
                entity = str(o.split('(')[-2].strip(' '))
                entities.append(entity)
                entity_id.append(s.split("/")[-1])
            except Exception as e:
                print("Error:", e)
        #print(s,"|||",p,"|||",o)
        if (not type_of_entity) and ('foaf' in o):
            type_of_entity=o.split("/")[-1]
    print(" ")
    print("Total "+str(len(entities))+" entities found! Showing first "+str(min(10, len(entities)))+" entities")
    print(" ")
    Entities=list(zip(entity_id,entities))
    Entities.sort(key=fn,reverse=True)

    for i in range(len(Entities)):
        print(str(i+1)+": ", Entities[i][1])
        if Entities[i][1] not in list(KnowledgeGraph.keys()):
            KnowledgeGraph[Entities[i][1]]=[class_name,type_of_entity,[]]
    print("\n")
    print(base_url[:-4]+"data/"+class_name+"/"+entity_id[0])
    uri_actor_id=[ base_url[:-4]+"data/"+class_name+"/"+entity_id[i] for i in range(len(entity_id))]
    print("Out degree of the first one:",out_degree(base_url[:-4]+"data/"+class_name+"/"+entity_id[0]))
    #write_to_csv(uri_actor_id,class_name)
    #print("Weight of first one :",uri_actor_id[0],weight(uri_actor_id[0]))
    return base_url,class_name,[Entities[i][0] for i in range(len(Entities))],[Entities[i][1] for i in range(len(Entities))]
    
def KnowledgeGraphCompute(base_url,class_name):
    base_url,class_name,actor_id,entities=RankEntitiesBasedOnClass(base_url,class_name)
    
    for i in range(1):
        URLQuestionsCompute(base_url[:-4]+"data/"+class_name+"/"+actor_id[i],entities[i],actor_id[i])
        save_obj(KnowledgeGraph,"KnowledgeGraph_"+class_name)
    KG=load_obj("KnowledgeGraph_"+class_name)
    # print(type(KG))

def main():
    ListOfClasses=["actor","cinematographer","director","editor","film_art_director","film_casting_director"
     ,"film_character","film_costume_designer","film_crewmember","film_critic","film_distributor", 
     "film_festival_sponsor","film_production_designer","film_story_contributor","film_theorist"
     ,"music_contributor","producer","writer"]
    base_url = 'http://data.linkedmdb.org/all/'

    class_name="actor"
    KnowledgeGraphCompute(base_url,class_name)
    print(len(list(KnowledgeGraph.keys())))

if __name__ == '__main__':
    main()
