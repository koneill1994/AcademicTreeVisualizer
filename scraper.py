# web scraper to pull data from academictree and compile it into a viewable database
# Kevin J. O'Neill

# I could do this with scrapy but for this purpose its probably not worth the effort to learn


import urllib
import networkx as nx
import matplotlib.pyplot as plt

import sys, time

import http_requests as hr






G = nx.DiGraph()


# start at a person
#   get that person's parents
#   add those people to the graph
#   add directional edges to those people
def AddPerson(person,depth):
  parents=GetParents(person)
  for p in parents:
    d=DictFromPersonObject(person)
    in_graph=False
    if p.name in G:
      in_graph=True
    else:
      print("Adding "+p.name+" to graph")
    G.add_node(p.name,attr_dict=d)
    G.add_edge(p.name,person.name)
    if depth<7 and not in_graph:
        AddPerson(p,depth+1) # dangerous without a stopping condition, but kinda the point of the whole thing

# given a person, gives that person's parents in an array
def GetParents(person):
  print("making http request at t="+str(time.strftime("%H:%M:%S")))
  return hr.PersonLookup(person.ID)


def DictFromPersonObject(person):
  d={}
  d['name']=person.name
  d['ID']=person.ID
  d['university']=person.university
  return d


def DrawGraph(G,ls):
  #nx.draw_networkx(G, with_labels=True, pos=nx.spring_layout(G), labels=ls)
  pos=nx.nx_agraph.graphviz_layout(G,prog='dot',args='')
  nx.draw(G, pos)
  nx.draw_networkx_labels(G,pos, labels=ls, font_size=10)
  plt.show()

def MakeLabels(G):
  labels={}
  for node in G.nodes():
    labels[node]=node
  return labels




read=True

if sys.argv[1]=="read":
  read=True
elif sys.argv[1]=="scrape":
  read=False
else:
  print("error: argument 1 must either be 'read' or 'scrape'")
  sys.exit()

if not read:
  persons=sys.argv[2].split(",")
  for person in persons:
    AddPerson(hr.PersonLookup(person)[0],0)
  
  # maximum recursion depth exceeded [???]
  # this is a lame solution but it works
  sys.setrecursionlimit(10000)
  nx.write_gpickle(G,"./pickled_graphs/"+str(sys.argv[2]))
else:
  G=nx.read_gpickle("./pickled_graphs/"+str(sys.argv[2]))



DrawGraph(G,MakeLabels(G))



# ok this seems hard i give up
# academictree pages don't have an easy way to grab data from them
# without parsing all the text

# apparently you can export from the database if you ask nicely
# so i sent an email to the site admin


# no response yet, so progress continues
# look at http_requests.py
