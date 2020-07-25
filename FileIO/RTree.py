"""
@author: bspark
"""
import numpy as np
from rtree import index

def pointRect(coord):
    '''
    Method for generating rectangle for a point
    
    Parameter
    ---------
    coord:  tuple or list of two values
            x and y coordinates of a point
            
    Return
    ------
            boundary box of a point
    '''
    return (coord[0]-1, coord[1]-1, coord[0]+1, coord[1]+1)

def rtree_point(graph, indField='Ind'):
    '''
    Method for creating a rtree index and inserting records using networkx graph
    
    Parameters
    ----------
    graph:      networkx graph
                graph containing points
            
    indField:   string
                graph attribute for ind of the index
                
    Returns
    -------
    idxPoint            rtree.Index
                        Index of points
                        
    pointIdCoordDict    dictionary
                        Index values (key:index, value:tuple(x, y))
    '''
    idxPoint = index.Index()
    pointIdCoordDict = {}
    for point in graph.nodes(data=True):
        pointRectVal = pointRect((point[0][0], point[0][1]))
        idxPoint.insert(int(point[1][indField]), pointRectVal)
        
        pointIdCoordDict[point[1][indField]] = (point[0][0], point[0][1])
        
    return idxPoint, pointIdCoordDict

def lineRect(lineGraph, node1, node2):
    '''
    Method for generating rectangle for a edge using coordinates of vertises
    
    Parameters
    ----------
    lineGraph:  networkx graph
                graph containing lines
            
    node1:      tuple(x, y)
                starting point of an edge
    
    node2:      tuple(x, y)
                ending point of an edge
                
    Return
    ------
                tuple(float, float, float, float)
                bounding box of an edge
    
    '''
    left = min(np.array(lineGraph.edge[node1][node2]['coordinates'])[:,0])
    bottom = min(np.array(lineGraph.edge[node1][node2]['coordinates'])[:,1])
    right = max(np.array(lineGraph.edge[node1][node2]['coordinates'])[:,0])
    up = max(np.array(lineGraph.edge[node1][node2]['coordinates'])[:,1])
    return (left, bottom, right, up)
    

def rtree_polyline(polylineGraph, indField='Ind'):
    '''
    Method for creating a rtree Index object and inserting records into it
    
    Parameters
    ----------
    polylinGraph:   networkx graph
                    graph containing edges
                    
    indField:       string
                    graph attribute for ind of the index
                    
    Return
    ------
    idxLine             rtree.Index
                        Index of lines
                        
    edgeIdCoordDict     dictionary
                        Index values (key:index, value:tuple(tuple(x, y), tuple(x,y)))
    '''
    idxLine = index.Index()
    edgeIdCoordDict = {}
    for edge in polylineGraph.edges(data=True):
        lineRectVal = lineRect(polylineGraph, edge[0], edge[1])
        idxLine.insert(int(edge[2][indField]), lineRectVal)
        
        edgeIdCoordDict[edge[2][indField]] = (edge[0], edge[1])
        
    return idxLine, edgeIdCoordDict
