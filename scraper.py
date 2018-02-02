# web scraper to pull data from academictree and compile it into a viewable database
# Kevin J. O'Neill

# I could do this with scrapy but for this purpose its probably not worth the effort to learn


import urllib
import networkx as nx
import matplotlib.pyplot as plt

import sys

import http_requests as hr






G = nx.DiGraph()


# start at a person
#   get that person's parents
#   add those people to the graph
#   add directional edges to those people
def AddPerson(person,depth):
  depth+=1
  parents=GetParents(person)
  for p in parents:
    d=DictFromPersonObject(person)
    G.add_node(p.name,attr_dict=d)
    G.add_edge(p.name,person.name)
    if depth<5:
      AddPerson(p,depth) # dangerous without a stopping condition, but kinda the point of the whole thing

# given a person, gives that person's parents in an array
def GetParents(person):
  print("making http request")
  return hr.PersonLookup(person.ID)


def DictFromPersonObject(person):
  d={}
  d['name']=person.name
  d['ID']=person.ID
  d['university']=person.university
  return d





### label stuff has not been bugtested yet ###
##############################################
def DrawGraph(G,ls):
  #nx.draw_networkx(G, with_labels=True, pos=nx.spring_layout(G), labels=ls)
  pos=nx.nx_agraph.graphviz_layout(G,prog='dot',args='')
  nx.draw(G, pos)
  nx.draw_networkx_labels(G,pos, labels=ls)
  plt.show()

def MakeLabels(G):
  labels={}
  for node in G.nodes():
    labels[node]=node
  return labels
##############################################




if sys.argv[1]=="read":
  read=True
else:
  read=False

if not read:
  AddPerson(hr.PersonLookup(sys.argv[1])[0],0)
  
  # maximum recursion depth exceeded [???]
  # this is a lame solution but it works
  sys.setrecursionlimit(10000)
  nx.write_gpickle(G,"graph_pickle")
else:
  G=nx.read_gpickle("graph_pickle")



DrawGraph(G,MakeLabels(G))



# ok this seems hard i give up
# academictree pages don't have an easy way to grab data from them
# without parsing all the text

# apparently you can export from the database if you ask nicely
# so i sent an email to the site admin


# no response yet, so progress continues
# look at http_requests.py
