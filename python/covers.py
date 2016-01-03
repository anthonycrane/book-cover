import requests
import pickle
from PIL import Image
from numpy import array
from pymongo import MongoClient
from progressbar import ProgressBar, Percentage
from bson.binary import Binary

# function defintions
def get_array(url, fout, pbar):
	"""retrieves book cover image file from url and converts it to numpy array"""
	r = requests.get(url, stream = True)
	img = Image.open(r.raw).thumbnail((255, 255), Image.ANTIALIAS)
	ar = array(img)
	pbar.update()
	return ar

# open connection to mongod
client = MongoClient()

# connect to mongodb data base
db = client.book_cover

# connect to meta collection
meta = db.meta

# get first 100 meta entries
cursor = meta.find().batch_size(100)

# initialize progress bar
wdgs = ['Test: ', Percentage()]
pbar = ProgressBar( max_value = 100, poll = 0.0001)

# loop through k meta entries and download image
for item in pbar(cursor[1:100]):
	if 'imUrl' in item:
		img_array = get_array(item['imUrl'], '../img/' + item['asin'] + '.jpg', pbar)
		item['img'] = Binary(pickle.dumps(img_array, protocol = 2), subtype = 128)
		meta.save(item)
	else:
		print(item['asin'] + '.jpg no image found')

