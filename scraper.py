# web scraper to pull data from academictree and compile it into a viewable database
# Kevin J. O'Neill



# usage:
# python3 scraper.py TYPE ID_NUMBER

# ID_NUMBER
  # the id number on academictree of the person who's lineage you are trying to pull
  # for example:
    # https://academictree.org/physics/peopleinfo.php?pid=3611
    #                                                     ^^^^
    # in this example, the ID would be 3611

# TYPE
  # either "scrape" or "read"
  # scrape will pull all academic ancestors of ID_NUMBER up to maxdepth from academictree.org
  # read will unpickle a saved verson (if it exists) of the network (named ID_NUMBER) so you don't have to create it from scratch


import urllib
import networkx as nx
import matplotlib.pyplot as plt

import sys, time

import http_requests as hr

from networkx.readwrite import json_graph
import json

import webbrowser



def GetPerson(ID_no):
  print("making http request at t="+str(time.strftime("%H:%M:%S")))
  return hr.PersonLookupNew(ID_no)
  
def AddPerson(ID,depth,child=None):
  person = GetPerson(ID)
  if (child==None):
    genesis = "true"
  else:
    genesis="false"
  d=DictFromPersonObject(person,genesis)
  
  in_graph=False
  if person.name in G:
    in_graph=True
  else:
    print("Adding "+person.name+" to graph")
    
  G.add_node(person.name,attr_dict=d)
  if child != None:
    G.add_edge(person.name,child)
  
  for mentor_ID in person.advisorlist:
    if depth<maxdepth and not in_graph:
      AddPerson(mentor_ID,depth+1, person.name)



def DictFromPersonObject(person,genesis):
  d={}
  d['name']=person.name
  d['ID']=person.ID
  d['genesis']=genesis
  d['label']=person.name
  return d
# todo: have this function (^^^) add depth as a dictionary attribute
#   whenever someone comes up in AddPerson, and they already exist in the network:
#     1. check the current depth against the network's recorded depth
#     2. set the depth attribute to max(current_depth, depth_attr)
#   
# in displaying the hierarchy, these will be the levels at which the nodes will be arranged vertically
# this will ensure that mentors are strictly above their mentees




def DrawGraph(G,ls):
  pos=nx.nx_agraph.graphviz_layout(G,prog='dot',args='')
  nx.draw(G, pos)
  nx.draw_networkx_labels(G,pos, labels=ls, font_size=6)
  plt.show()

def MakeLabels(G):
  labels={}
  for node in G.nodes():
    labels[node]=node
  return labels
'''
def GetRootNode(G, root_ID):
  for node in G.nodes:
    if 
'''
def SaveAsJSON(G):
  data = json_graph.node_link_data(G)
  with open("./html/nld_"+str(sys.argv[2])+"_"+str(maxdepth)+".json", 'w') as fp:
    json.dump(data, fp)
    '''
  d2 = json_graph.tree_data(G, root)
  with open("./html/td_"+str(sys.argv[2])+"_"+str(maxdepth)+".json", 'w') as fp:
    json.dump(data, fp)
'''


maxdepth=7


G = nx.DiGraph()


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
    AddPerson(person, 0, None)
  
  # maximum recursion depth exceeded [???]
  # this is a lame solution but it works
  sys.setrecursionlimit(10000)
  nx.write_gpickle(G,"./pickled_graphs/"+str(sys.argv[2]))
else:
  G=nx.read_gpickle("./pickled_graphs/"+str(sys.argv[2]))


SaveAsJSON(G)

webbrowser.open("./html/test.html")

#nx.write_gexf(G, "./pickled_graphs/"+str(sys.argv[2])+".gexf")


DrawGraph(G,MakeLabels(G))
