"""@package docstring
Class to evaluate ADAS with KPI's
"""

import pandas as pd
import numpy as np
import os,sys,inspect
import h5py
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
import math
import warnings
from scipy.signal import filtfilt, butter

class cOSMParser:
    
    def __init__(self):
        # current directory path
        self.sCurrentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # current parent directory path
        self.sParentDir = os.path.dirname(self.sCurrentDir)
        # current grandparent directory path
        self.sGrandParentDir = os.path.dirname(os.path.dirname(self.sCurrentDir))
        # all available CRO roads
        #self.oRoadslist = ['A7','A8','B19','B295','L1180']
        
        
    def getNodesFromOSM(self,dom):
        """
        Get all nodes from osm strored in pandas DataFrame
        @:param dom                 [in]    minidom object
        @:param df                  [out]   pandas DataFrame with nodes information
        """
        data = {}
        keys = []
            
        #  parse out osm nodes
        for n in dom.getElementsByTagName("node"):
            nid = n.getAttribute("id")
            data[nid] = {}
            data[nid]["lat"] = n.getAttribute("lat")
            data[nid]["lon"] = n.getAttribute("lon")
            for tag in n.getElementsByTagName("tag"):
                if(tag.hasAttribute("k")):
                    k = tag.getAttribute("k")
                    if(k not in keys):
                        keys.append(k)
                    if(tag.hasAttribute("v")):
                        data[nid][k] = tag.getAttribute("v")
        dnodes = pd.DataFrame(data)
        
        return dnodes
        
    def getWaysFromOSM(self,dom):
        """
        Get all ways from osm strored in pandas DataFrame
        @:param dom                 [in]    minidom object
        @:param df                  [out]   pandas DataFrame with ways information
        """ 
        ways = {}
        wkeys = []


        # parse out osm ways/polygons
        for n in dom.getElementsByTagName("way"):
            wid = n.getAttribute("id")
            ways[wid] = {}
            ways[wid]['ref'] = []
            ways[wid]['geomType'] = ""
            for nd in n.getElementsByTagName('nd'):
                if nd.hasAttribute('ref'):
                    ref = nd.getAttribute('ref')
                    ways[wid]['ref'].append(ref)
                del nd

            for tag in n.getElementsByTagName("tag"):
                if tag.hasAttribute("k") and \
                   tag.hasAttribute('v'):
                    k = tag.getAttribute("k")
                    if k not in wkeys:
                        wkeys.append(k)
                    ways[wid][k] = tag.getAttribute('v')
                del tag

            #first and last to identify the geomType
            first = ways[wid]['ref'][0]
            last = ways[wid]['ref'][len(ways[wid]['ref'])-1]
            if ways[wid]['ref'][0] == ways[wid]['ref'][len(ways[wid]['ref'])-1]:
                ways[wid]['geomType'] = "polygon"
            else:
                ways[wid]['geomType'] = "polyline"

        dways = pd.DataFrame(ways)
              
        return dways
         
    
    
    def getPandasDataFrameFromOSM(self,dnodes,dways):
        """
        calulate pandas DataFrame from OSM data with all information
        @:param dnodes               [in]    pandas DataFrame with nodes information 
        @:param dways                [in]    pandas DataFrame with ways information 
        @:param df                   [out]   pandas DataFrame with all osm information
        """
        #Get List of ways
        lcWayIds = list(dways.columns.values)

        #Get all points with all Information in one pandas DataFrame
        lcGeomType = []
        lcEle = []
        lcLat = []
        lcLon = []
        lcId = []
        lcWay = []
        lcRoadType = []

        for way in lcWayIds:
            cway = str(way)
            cGeomType = dways[way].iloc[0] #geomType
            cNodeIds = dways[way].iloc[4] # ref
            cRoadSign = dways[way].iloc[7] # roadsign:type
            #print(cNodesIds) 
            for node in cNodeIds:
                node = str(node)
                cEle = dnodes[node].iloc[0]
                lcEle.append(cEle)
                cLat = dnodes[node].iloc[1]
                lcLat.append(cLat)
                cLon = dnodes[node].iloc[2]
                lcLon.append(cLon)      
                lcId.append(node)   
                lcWay.append(cway)
                lcGeomType.append(cGeomType)
                lcRoadType.append(cRoadSign)

        #create new pandas Dataframe 
        dfdata = pd.DataFrame({'lon' : list(map(float,lcLon)),
                               'lat': list(map(float,lcLat)),  
                              'ele' : list(map(float,lcEle)),
                              'id': list(map(int,lcId)),
                               'way': list(map(int,lcWay)),
                            'geometry': list(map(str,lcGeomType)),
                              'roadsign':list(map(str,lcRoadType))}, columns=['lon','lat','ele','id','way','geometry','roadsign'])


        return dfdata
        
        
        
        
    def extractRoadSigns(self,dways,dnodes,dfdata):
        """
        claculate pandas DataFrame from .osm with all road signs
        @:param dways                   [in]    pandas DataFrame with ways information
        @:param dnodes                  [in]    pandas DataFrame with nodes information
        @:param dfdata                  [in]    pandas DataFrame with all osm information
        @:param dfsign                  [out]   pandas DataFrame with all road signs
        """
        # all Ways with roation clockwise
        WayIds = []
        RoadSigns = []


        #Get List of ways
        lcWayIds = list(dways.columns.values)

        #Get all points with all Information in one pandas DataFrame
        lcGeomType = []
        lcEle = []
        lcLat = []
        lcLon = []
        lcId = []
        lcWay = []
        lcRoadType = []

        #getting list of wayID's
        for i in range(0,len(dfdata.way.values),1):

            if dfdata.way.values[i] not in WayIds and dfdata.roadsign.values[i] != 'nan':
                WayIds.append(dfdata.way.values[i])
                RoadSigns.append(dfdata.roadsign.values[i])
                
                for way in WayIds:
                    cway = str(way)
                    cGeomType = dways[str(way)].iloc[0] #geomType
                    cNodeIds = dways[str(way)].iloc[4] # ref
                    cRoadSign = dways[str(way)].iloc[7] # roadsign:type
                    #print(cNodesIds) 
                    for node in cNodeIds:
                        node = str(node)
                        cEle = dnodes[node].iloc[0]
                        lcEle.append(cEle)
                        cLat = dnodes[node].iloc[1]
                        lcLat.append(cLat)
                        cLon = dnodes[node].iloc[2]
                        lcLon.append(cLon)      
                        lcId.append(node)   
                        lcWay.append(cway)
                        lcGeomType.append(cGeomType)
                        lcRoadType.append(cRoadSign)

                #create new pandas Dataframe 
                dfsign = pd.DataFrame({'lon' : list(map(float,lcLon)),
                                       'lat': list(map(float,lcLat)),  
                                      'ele' : list(map(float,lcEle)),
                                      'id': list(map(int,lcId)),
                                       'way': list(map(int,lcWay)),
                                    'geometry': list(map(str,lcGeomType)),
                                      'roadsign':list(map(str,lcRoadType))}, columns=['lon','lat','ele','id','way','geometry','roadsign'])
           
        #pandas dataframe with road signs
        return dfsign