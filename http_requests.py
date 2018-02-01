
import urllib.request
import zlib

import xml.etree.ElementTree as ET
import itertools as IT

import lxml
from lxml.html.clean import Cleaner
from lxml import etree

import io
import sys

from bs4 import BeautifulSoup


def PersonLookup(ID):
  url = "http://academictree.org/neurotree/peopleinfo.php?pid="+str(ID)
  #url = "http://neurotree.org/neurotree/peopleinfo.php?pid="+str(ID)
  headers = {
  #'Host': 'neurotree.org', # 'academictree.org',
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'Cache-Control': 'max-age=0'
  }

  a=urllib.request.Request(url, headers=headers)

  b=urllib.request.urlopen(a)

  decompressed_data=zlib.decompress(b.read(), 16+zlib.MAX_WBITS)


  f = decompressed_data



  cleaner = Cleaner()
  cleaner.javascript = True # This is True because we want to activate the javascript filter
  cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter

  f_clean = cleaner.clean_html(f)


  m = open('test.txt','w')
  m.write(f_clean.decode('utf-8'))
  m.close()


  # oh my god beautiful soup is amazing
  soup = BeautifulSoup(f, 'html.parser')

  #print(soup.find_all('a'))
  
  
  AdvisorList=[]
  
  # this is nt robust
  # errors when an advisor does not have a location, or no link on a location
  for x in soup.find_all('table', "connection_list"):
    if x.parent.parent("h4")[0].string=="Parents":
      for row in x("tr"):
        name,ID,location="","",""
        if len(row("td"))>1:
          #print("ADVISOR: "+row("td")[0].string)
          name=row("td")[0].string
          if len(row("td")[0]("a"))>0:
            id_no=row("td")[0]("a")[0]['href']
            #print("  ID: "+id_no[id_no.index('?pid=')+5:])
            ID=id_no[id_no.index('?pid=')+5:]
          if len(row("td"))>=3:
            if row("td")[3].string != None:
              #print("  LOCATION: "+row("td")[3].string)
              location=row("td")[3].string
          AdvisorList.append(Person(name,ID,location))
  return AdvisorList


class Person:
  def __init__(self, name, tree_id,uni):
    self.name=name
    self.ID = tree_id
    self.university=uni
  def debugprint(self):
    print("  "+self.name)
    print("  "+self.ID)
    print("  "+self.university)


l = PersonLookup(sys.argv[1])


for x in l:
  x.debugprint()
  print("")
