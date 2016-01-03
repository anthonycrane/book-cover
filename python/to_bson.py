import gzip
import requests
import pandas as pd
from pymongo import MongoClient
from progressbar import ProgressBar, ETA, FileTransferSpeed, Bar, Percentage

# function definitions
def unzip(path):
	"""unzips .gz compressed files"""
	g = gzip.open(path, 'rb')
	for f in g:
		yield eval(f)

def getDF(path):
	"""converts json obj of .gz archive to pandas data frame"""
	i = 0 
	df = {}
	client = MongoClient()
	db = client.book_cover
	meta = db.meta
	pbar = ProgressBar()
	for f in pbar(unzip(path)):
		df[i] = f
		meta.insert_one(df[i])
		i += 1
	print("Finished.")
	return 


def getImage(url, fout):
	"""retrieves book cover image file from url"""
	r = requests.get(url, stream = True)
	with open(fout, 'wb') as fd:
		for chunk in r:
			fd.write(chunk)


# load reviews and meta to data frames
# reviews = getDF('../json/reviews_Books.json.gz')
getDF('../json/meta_Books.json.gz')


"""
# add cover image files to img folder
for i in range(meta.shape[0]):
	getImage(meta['imUrl'][i], '../img/' + meta['asin'][i] + '.jpg')

# merge data
pd.DataFrame.merge(reviews, meta, on = 'asin')
pd.DataFrame.from_dict(df, orient = "index")
"""