import urllib2
from BeautifulSoup import BeautifulSoup
from collections import namedtuple
import os

"all characters must be converted to hex so that the site can read them upon search"
def convertToSearchable(input):
    hexVersion = input.encode("hex")
    return '%' + "%".join([hexVersion[start:start+2] for start in range(0, len(hexVersion), 2)])

Metadata = namedtuple("Metadata", "title author path")
path = "file://" + os.path.dirname(os.path.realpath(__file__)) + '/test.html'
data= urllib2.urlopen(path).read()

gutenRootURL = "http://www.gutenberg.org"

def getResults(query):
	url = gutenRootURL + '/ebooks/search/?query=' + convertToSearchable(query)
	html = data #urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	bookListing = []
	for bookHolder in soup.findAll('li', {'class':'booklink'}):
                ## We may want to remove the gutenRootURL and just apply it after clicks, but for now, for completeness
		bookUrl = gutenRootURL + bookHolder.find('a', {'class':'link'}).get("href")
		bookInfo = bookHolder.find('span', {'class':'cell content'})
		title = bookInfo.find('span', {'class':'title'}).getText()
		"FIND THAT HTML"
		if(bookInfo.find('span', {'class':'subtitle'}) != None):
			author = bookInfo.find('span', {'class':'subtitle'}).getText()
		num = bookUrl.split("/")[-1]
		htmlPath = "http://www.gutenberg.org/files/"+num+"/"+num+"-h/"+num+"-h.htm"
		bookListing.append(Metadata(title=title, author=author, path=htmlPath))
	return bookListing
