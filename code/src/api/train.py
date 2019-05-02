import mxnet as mx
from mxnet import gluon, nd
from mxnet.gluon.model_zoo import vision
import multiprocessing
from mxnet.gluon.data.vision.datasets import ImageFolderDataset
from mxnet.gluon.data import DataLoader
import numpy as np
import wget
import imghdr
import json
import pickle
import hnswlib
import numpy as np
import glob, os, time
import matplotlib.gridspec as gridspec
import urllib2
import gzip
import os, tempfile, glob
from image import data as data_image
import configparser
import pymongo

config = configparser.ConfigParser()
config.read("config.ini")

config_dic = {}

for option in config['DEFAULT']:
    config_dic[option] = config.get('DEFAULT', option, raw=True)


images_path = "images/"
idx_loc = config_dic.get("idx_loc")
idx_dir = config_dic.get("idx_dir")
BATCH_SIZE = 10
EMBEDDING_SIZE = 512
SIZE = (224, 224)
MEAN_IMAGE= mx.nd.array([0.485, 0.456, 0.406])
STD_IMAGE = mx.nd.array([0.229, 0.224, 0.225])

ctx = mx.cpu()
net = vision.resnet18_v2(pretrained=True, ctx=ctx)
net = net.features

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

empty_folder = tempfile.mkdtemp()
# Create an empty image Folder Data Set
dataset = ImageFolderDataset(root=empty_folder, transform=transform)
print dataset



# def download_files():
#     for asin, url in data_image.iteritems():
#         path = os.path.join(images_path, asin+'.jpg')
#         if not os.path.isfile(path):
#             f = urllib2.urlopen(url)
#             print images_path+asin+'.jpg'
#             with open(images_path+asin+'.jpg', "wb") as local_file:
#                 local_file.write(f.read())



def download_files():
    print "Inside download-files"
    data = list(get_mongo_connection().catalog.products.find({}))
    for d in data:
        print "d ",d
        asin = d['asin']
        url = d['img_url']
        path = os.path.join(images_path, asin+'.jpg')
        if not os.path.isfile(path):
            f = urllib2.urlopen(url)
            print images_path+asin+'.jpg'
            with open(images_path+asin+'.jpg', "wb") as local_file:
                local_file.write(f.read())

            
download_files()

list_files = glob.glob(os.path.join(images_path, '**.jpg'))
print list_files
dataset.items = list(zip(list_files, [0]*len(list_files)))
print dataset.items
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, last_batch='keep', shuffle=False, num_workers=1)
print dataset.items
if os.path.isfile(idx_dir+"dataset.pkl"):
    os.remove(idx_dir+"dataset.pkl")
pickle.dump(dataset.items, open(idx_dir+"dataset.pkl", "wb" ))
features = np.zeros((len(dataset), EMBEDDING_SIZE), dtype=np.float32)
tick = time.time()
n_print = 100
j = 0
print "hello"
for i, (data, label) in enumerate(dataloader):
    print "i ",i
    print "data ",data
    data = data.as_in_context(ctx)
    if i%n_print == 0 and i > 0:
        print("{0} batches, {1} images, {2:.3f} img/sec".format(i, i*BATCH_SIZE, BATCH_SIZE*n_print/(time.time()-tick)))
        tick = time.time()
    output = net(data)
    features[(i)*BATCH_SIZE:(i+1)*max(BATCH_SIZE, len(output)), :] = output.asnumpy().squeeze()
print output
num_elements = len(features)
print num_elements
labels_index = np.arange(num_elements)
p = hnswlib.Index(space = 'l2', dim = EMBEDDING_SIZE) # possible options are l2, cosine or ip

# Initing index - the maximum number of elements should be known beforehand
p.init_index(max_elements = num_elements, ef_construction = 100, M = 16)

# Element insertion (can be called several times):
print labels_index
int_labels = p.add_items(features, labels_index)

# Controlling the recall by setting ef:
p.set_ef(100) # ef should always be > k
p.save_index(idx_loc)
