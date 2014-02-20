from pyquery import PyQuery as pq
import sys, os, re, unicodedata
import urllib, threading, os.path

def slugify(value):
	value = unicodedata.normalize('NFKD', value)
	value = value.encode('ascii', 'ignore').decode('ascii')
	value = re.sub('[^\w\s-]', '', value).strip().lower()
	value = re.sub('[-\s]+', '-', value)
	return value

def download_pic(url, name):
	print(u'Download: %s' % url)
	urllib.urlretrieve(url, name)

def get_name_and_quality():    
	if len(sys.argv) == 1:
		print(u'Username not found, run "python ficr.py <username> <size>"')
		print(u'Sizes: o->Original, q->150x150, k->2048x???')
		exit(1)
	else:
		username = sys.argv[1]
		try:
			size = sys.argv[2]     # Picture-Size (o->Original, q->150x150, k->2048x???)
		except:
			size = u'o'
	
	return [username, size]

def find_links(url, username, size):
	doc = pq(url='%s%s' % (url, username))
	for d in doc('.photo-display-item'):    
		doc = pq(url='%s/%s/%s/sizes/%s/' % (url,username,d.attrib['data-photo-id'],size))
		photo_title = u'%s' % doc('meta[name=title]').attr("content")
		link = doc('#allsizes-photo').children().attr('src')
		print photo_title
		filename = u'%s.jpg' % slugify(photo_title)
		if not os.path.isfile(filename):
			download_thread = threading.Thread(target=download_pic, args=[link, filename])
			download_thread.start()

# Execute 
url = u'http://www.flickr.com/photos/'
username, size = get_name_and_quality()
find_links(url, username, size)
