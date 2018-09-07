import rdflib

def main():
    g=rdflib.Graph()
    print("\n")
    url = 'http://data.linkedmdb.org/all'
    print("Extracting Data From Linkedmdb, refer to "+str(url))
    g.load(url)
    classes = []
    for x in g:
        s,p,o = x
        if('label' in p):
            label = str(o.split(' ')[-1])
            classes.append(str(label))
    print(" ")
    print("Total "+str(len(classes))+" class labels found! Showing first 10")
    print(" ")

    for i in range(10):
        print(str(i+1)+": "+str(classes[i]))
    print("\n")


if __name__ == '__main__':
    main()