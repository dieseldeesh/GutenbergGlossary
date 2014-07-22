import urllib2
import re

from BeautifulSoup import BeautifulSoup
from collections import namedtuple

query = 'Tale of two cities'

"all characters must be converted to text. \s --> +, rest become hex"
"Spaces can even become text"
def convertToSearchable(input):
    hexVersion = input.encode("hex")
    for i in range(len(hexVersion))/2:
         

BookMeta = namedtuple("BookMeta", "title author")

splitter = re.compile(r'\s+')

splitQuery = filter(None, splitter.split(query))
str = '+'
ending = str.join(splitQuery)
urlbase = 'http://www.gutenberg.org/ebooks/search/?query=' + ending

soup = BeautifulSoup(urllib2.urlopen(urlbase).read())

bookListing = []

for bookHolder in soup.findAll('li', {'class':'boolink'}):
    bookInfo = bookHolder.find('span', {'class':'cell content'})
    title = bookInfo.find('span', {'class':'title'}).getText()
    if(bookInfo.find('span', {'class':'subtitle'}) != None):
        subtitle = bookInfo.find('span', {'class':'subtitle'}).getText()
    bookListing.append(BookMeta(title, subtitle))


"""
  Get the HTML link
  Put into the form of an onward list - print out HTML
"""
