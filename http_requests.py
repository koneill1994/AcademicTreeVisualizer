
import urllib.request
import zlib

from lxml.html.clean import Cleaner

from bs4 import BeautifulSoup


def PersonLookupNew(ID):
  url = "http://academictree.org/neurotree/peopleinfo.php?pid="+str(ID)
  headers = {
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
  
  AdvisorList=[]
  name=""
  
  for x in soup.find_all('div', "personinfo"):
    name= x("h1")[0].string.strip()
  
  for x in soup.find_all('table', "connection_list"):
    if x.parent.parent("h4")[0].string=="Parents":
      for row in x("tr"):
        if len(row("td"))>1:
          if len(row("td")[0]("a"))>0:
            advisor_url=row("td")[0]("a")[0]['href']
            AdvisorList.append(advisor_url[advisor_url.index('?pid=')+5:])
  
  return Person(name, ID, AdvisorList)


class Person:
  def __init__(self, name, tree_id,advisorlist):
    self.name=name
    self.ID = tree_id
    self.advisorlist=advisorlist
  def debugprint(self):
    print("  "+self.name)
    print("  "+self.ID)


