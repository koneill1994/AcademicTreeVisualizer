# Kevin J. O'Neill

# An algorithm to arrange a directed acyclic graph into a number of hierarchical levels
# such that each node is on a level higher than all of its children

# this is similar to a topological ordering
# but allows nodes to be in the same position, 
# so that they could be next to each other on the hierarchy

import networkx as nx


  
  # step 1: initial depth assignment
  #   for each start node:
  #     (i.e. a node which has no children)
  #     (marked as "genesis" in attr)
  #       set its depth to 0
  #       for each of that nodes' parents
  #         set depth to n+1
  #         recurse
  
  # in the event that a node is parent to 2 different children
  #   set the depth to the max+1 of their two depths
  
  
  
  # after step 1, we should have as many depth-ordered trees as we do start nodes
  # now we need to deal with the possibility that the 
  #   start nodes might not be on the same level
  
  # step 2: tree reconciliation
  #
  #  pick a tree A to be the PRIME TREE, the standard of comparison for 
  #    all the other trees
  #  
  #  for each pair of trees:
  #     for node in UNION(tree A, tree X):
  #       find the nodes with the maximum discrepancy in depth 
  #         between the A and X versions
  #       offset all depths in tree X by that discrepancy
  
  
  
  # ok, so now the constraints of the problem should be satisfied, 
  #   but it still doesn't look very pretty
  # some nodes only have a single parent who is several levels above them
  #   yet they are only 1 level above their children
  # we'll solve this by moving these nodes to the midway point between their parents and children
  
  # step 3: depth-balancing
  
  # for node in G:
  #   for parent in node.parents:
  #     if parent.depth > 1+node.depth:
  #       node.depth=avg(min(parent.depth),max(child.depth))
  
  
  # now that we've added all these properties to the graph, we'll return it
  # when the graph is moved into javascript,
  #  the depth value will be used to determine the y-value of a node in the tree
  
  

def BuildHierarchy(G):
  return

