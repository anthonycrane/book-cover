import requests
from PIL import Image
from numpy import array
from pymongo import MongoClient
from progressbar import ProgressBar, Percentage

# function defintions
def getImage(url, fout, pbar):
	"""retrieves book cover image file from url"""
	r = requests.get(url, stream = True)
	with open(fout, 'wb') as fd:
		for chunk in r:
			fd.write(chunk)
			pbar.update()


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
		getImage(item['imUrl'], '../img/' + item['asin'] + '.jpg', pbar)

	else:
		print(item['asin'] + '.jpg no image found')
