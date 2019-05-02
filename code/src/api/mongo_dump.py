import pymongo
from imagebulk import data 

con = None

def get_mongo_connection(host='localhost', port=27017):
    global con
    if con is None:
        print "Establishing connection %s host and port %d" %(host,port)
        try:
            con = pymongo.MongoClient(host, port)
        except Exception, e:
            print e
            return None
    return con



def run():
    for d in data['prediction']:
        exist = list(get_mongo_connection().catalog.products.find({'asin':d['ASIN']}))
        if not exist:
            t = {'asin':d['ASIN'],'img_url':d['url'],'title':d['title']}
            print t
            get_mongo_connection().catalog.products.insert(t)


if __name__ == '__main__':
    run()