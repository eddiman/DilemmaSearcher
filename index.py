from __future__ import unicode_literals
import os
import random
from HTMLParser import HTMLParser
from optparse import OptionParser

from algoliasearch import algoliasearch


def parse_file(filename):
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.obj = {}
            self._key = None

        def handle_starttag(self, tag, attrs):
            if tag != "div":
                return
            for k, v in attrs:
                if k == "id":
                    self._key = v
                    break
            else:
                raise Exception("No id found")

        def handle_endtag(self, tag):
            self._key = None

        def handle_data(self, data):
            self.obj[self._key] = data

    parser = MyHTMLParser()
    with open(filename, "r") as fd:
        parser.feed(fd.read())
    return parser.obj


def walk(path):
    for path, _, files in os.walk(path):
        for f in files:
            yield os.path.join(path, f)


def main(input, index, base_url=None):
    objs = []
    n = 0
    for filename in walk(input):
        print filename
        obj = parse_file(filename)
        obj_url = filename
        if base_url:
            obj_url = obj_url.replace(input, base_url)
        obj["url"] = obj_url
        obj["objectID"] = obj_url
        obj["random"] = random.random()
        objs.append(obj)

        n += 1
        if n % 1000 == 0:
            print n
            index.save_objects(objs)
            objs = []

    index.save_objects(objs)
    print "DONE"

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input")
    parser.add_option("-b", "--base-url", dest="base_url")

    parser.add_option("-u", "--algolia-app-id", dest="algolia_app_id")
    parser.add_option("-p", "--algolia-api-key", dest="algolia_api_key")
    parser.add_option("--algolia-index", dest="algolia_index")

    options, args = parser.parse_args()

    client = algoliasearch.Client(options.algolia_app_id,
                                  options.algolia_api_key)
    index = client.init_index(options.algolia_index)
    main(options.input, index, base_url=options.base_url)
