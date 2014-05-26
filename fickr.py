#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import sys
import os
import re
import unicodedata
import urllib
import threading
import os.path
import json

class Fickr(object):

    photostream_url = u'http://www.flickr.com/photos/'
    flickrit_url = u'http://f.pboehm.org/photos/'

    def __init__(self):
        self.__username, self.__size = self.get_name_and_quality()

    def slugify(self, value):
        value = unicodedata.normalize('NFKD', value)
        value = value.encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        value = re.sub('[-\s]+', '-', value)
        return value

    def download_pic(self, url, name):
        urllib.urlretrieve(url, name)

    def get_name_and_quality(self):
        if len(sys.argv) == 1:
            print(u'Username not found, run "./ficr.py <username> <size>"')
            print(u'Sizes: o->Original, q->150x150, k->2048x???')
            exit(1)
        else:
            username = sys.argv[1]
            try:
                size = sys.argv[2]     # Picture-Size (o->Original, q->150x150, k->2048x???)
            except:
                size = u'o'
        return [username, size]

    def use_photostream(self):
        doc = pq(url='%s%s' % (self.photostream_url, self.__username))
        for d in doc('.photo-display-item'):
            doc = pq(url='%s/%s/%s/sizes/%s/' % (self.photostream_url, self.__username,d.attrib['data-photo-id'],self.__size))
            photo_title = u'%s' % doc('meta[name=title]').attr("content")
            link = doc('#allsizes-photo').children().attr('src')
            self.prepare_download(link, photo_title)

    def prepare_download(self, photo_url, photo_title):
        path = self.slugify(u'%s' % self.__username)
        filename = u'%s/%s.jpg' % (path, self.slugify(photo_title))
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.isfile(filename):
            download_thread = threading.Thread(target=self.download_pic, args=[photo_url, filename])
            download_thread.start()
            print(u'Download: %s' % photo_title)
        else:
            print(u'Exists:   %s' % photo_title)

    def use_flickit(self):
        response = urllib.urlopen('%s%s' % (self.flickrit_url, self.__username))
        data = json.load(response)
        for photo in data:
            self.prepare_download(photo['url_o'], photo['title'])

    def get_photos(self):
        try:
            print('use flickrit: %s\n' % self.flickrit_url)
            self.use_flickit(sd)
        except:
            print('error flickrit, parse: %s\n' % self.photostream_url)
            self.use_photostream()

#Execute
Fickr().get_photos()
