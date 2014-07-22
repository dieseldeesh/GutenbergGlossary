import urllib2
from BeautifulSoup import BeautifulSoup
from collections import namedtuple

Metadata = namedtuple("Metadata", "title author path")

data= urllib2.urlopen('file:///Users/adhishramkumar/Documents/GutenbergGlossary/test.html').read()

def getResults(query):
	url = 'http://www.gutenberg.org/ebooks/search/?query=' + query.replace(' ','+')
	html = data #urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	bookListing = []
	for bookHolder in soup.findAll('li', {'class':'booklink'}):
		bookInfo = bookHolder.find('span', {'class':'cell content'})
		title = bookInfo.find('span', {'class':'title'}).getText()
		if(bookInfo.find('span', {'class':'subtitle'}) != None):
			author = bookInfo.find('span', {'class':'subtitle'}).getText()
		bookListing.append(Metadata(title=title, author=author, path="http://www.google.com"))
	return bookListing