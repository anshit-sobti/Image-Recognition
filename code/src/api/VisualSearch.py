import mxnet as mx
from mxnet import nd
from mxnet.gluon.model_zoo import vision
import hnswlib
import matplotlib.pyplot as plt 
import configparser
import pickle
import pymongo
from bson import ObjectId

config = configparser.ConfigParser()
config.read("config.ini")

config_dic = {}

for option in config['DEFAULT']:
    config_dic[option] = config.get('DEFAULT', option, raw=True)


BATCH_SIZE = 256
EMBEDDING_SIZE = 512
SIZE = (224, 224)
MEAN_IMAGE= mx.nd.array([0.485, 0.456, 0.406])
STD_IMAGE = mx.nd.array([0.229, 0.224, 0.225])


p=None
net=None
datasets=None

ctx = mx.cpu()

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

def transform(image, label):
    resized = mx.image.resize_short(image, SIZE[0]).astype('float32')
    cropped, crop_info = mx.image.center_crop(resized, SIZE)
    cropped /= 255.
    normalized = mx.image.color_normalize(cropped,
                                      mean=MEAN_IMAGE,
                                      std=STD_IMAGE) 
    transposed = nd.transpose(normalized, (2,0,1))
    return transposed, label

def set_p():
    global p
    global net
    global datasets
    if not p:
        p = hnswlib.Index(space = 'l2', dim = EMBEDDING_SIZE)
        print config_dic
        idx_loc = config_dic.get("idx_loc")
        print idx_loc
        p.load_index(idx_loc)
        p.set_ef(300)
        net = vision.resnet18_v2(pretrained=True, ctx=ctx)
        net = net.features
        pkl_loc = config_dic.get("idx_dir")+"dataset.pkl"
        datasets = pickle.load( open( pkl_loc, "rb" ) )


def predict(path):
    global p
    if not p:
        set_p()
    image = plt.imread(path)[:,:,:3]
    image_t, _ = transform(nd.array(image), 1)
    print image_t
#     print "net ",net
    print ctx
    output = net(image_t.expand_dims(axis=0).as_in_context(ctx))
    labels, distances = p.knn_query([output.asnumpy().reshape(-1,)], k = 10)
    result = []
    for l in labels[0]:
        print "labels ",datasets[l]
        res = datasets[l]
        try:
            d = res[0].split('/')[1].split('.')[0]
            result.append(d)
        except Exception as e:
            print e
            continue
    _id = get_mongo_connection().catalog.suggestions.insert({"suggestions":result})
    return {'doc_id':str(_id)}


def get_docs(doc_id):
    o = ObjectId(doc_id)
    result = []
    s = list(get_mongo_connection().catalog.suggestions.find({'_id':o},{'_id':0}))
    temp = []
    for i in s:
        for a in i['suggestions']:
            p = list(get_mongo_connection().catalog.products.find({'asin':a},{'_id':0}))
            if not p:
                continue
            temp.append(p[0])
            if len(temp)==3:
                result.append(temp)
                temp = []
    if temp:
        result.append(temp)
    return result
        
        


    
    
    
    
    
    
    
    
    