# web scraper to pull data from academictree and compile it into a viewable database
# Kevin J. O'Neill

# I could do this with scrapy but for this purpose its probably not worth the effort to learn


import urllib,
import networkx as nx

import http_requests as hr

G = nx.DiGraph()


# start at a person
#   get that person's parents
#   add those people to the graph
#   add directional edges to those people
function AddPerson(person):
  parents=GetParents(person)
  for p in parents:
    G.add_node(p)
    G.add_edge(p,person)
    AddPerson(p) # dangerous without a stopping condition, but kinda the point of the whole thing

# given a person, gives that person's parents in an array
function GetParents(person):
  # todo
  return []


'''
class Person:
  self.__init__(self, name, tree_id,uni):
    self.name=name
    self.ID = tree_id
    self.university=uni
'''


# make sure we comply with academictree's crawler policy
# wouldn't want to piss off the site admin
# crawl-delay is 10 seconds 
rp = urllib.robotparser.RobotFileParser()
rp.set_url('https://academictree.org/robots.txt')
rp.read()



# ok this seems hard i give up
# academictree pages don't have an easy way to grab data from them
# without parsing all the text

# apparently you can export from the database if you ask nicely
# so i sent an email to the site admin


# no response yet, so progress continues
# look at http_requests.py
