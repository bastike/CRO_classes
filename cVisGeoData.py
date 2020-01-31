"""@package docstring
Class to evaluate ADAS with KPI's
"""
import folium
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os,sys,inspect
import numpy as np


class cVisGeoData:


    def __init__(self):
        # current directory path
        self.sCurrentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # current parent directory path
        self.sParentDir = os.path.dirname(self.sCurrentDir)
        # current grandparent directory path
        self.sGrandParentDir = os.path.dirname(os.path.dirname(self.sCurrentDir))
        # all available CRO roads
        #self.oRoadslist = ['A7','A8','B19','B295','L1180']
        
      
        
    def getIndexClosestGPSpoint(self,afLat,afLon,extrapolate):
        '''
        plot folium map of lat , lon array

        @:param afLat             [in]    Latitude as float array
        @:param afLon             [in]    Longitude as float array
        @:param extrapolate       [in]    factor to extrapolate for plotting
        @:param map               [out]   map  
        '''
        m = folium.Map([np.nanmean(afLat), np.nanmean(afLon)], zoom_start=11)
        points = [[afLat[i],afLon[i]] for i in range(0,len(afLat),extrapolate) ]
        folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)
        folium.LatLngPopup().add_to(m)
        return m
        
        
    def plotCROdataBlock(self,m,afLat,afLon,extrapolate,color):
        '''
        plot folium map of lat , lon array

        @:param afLat             [in]    Latitude as float array
        @:param afLon             [in]    Longitude as float array
        @:param extrapolate       [in]    factor to extrapolate for plotting
        @:param map               [out]   map  
        '''

        points = [[afLat[i],afLon[i]] for i in range(0,len(afLat),extrapolate) ]
        folium.PolyLine(points, color=color, weight=2.5, opacity=1).add_to(m)
        folium.LatLngPopup().add_to(m)
        return m
        
        
        
        
    def visualCheckCRO(self,m,df):
        lineList = []
        for i in range(len(df.columns)):
            if df.columns[i][-3:] == 'ele':
                pass
            else:
                lineList.append(df.columns[i])
                
        for i in range(0,len(lineList),2):
            #print(lineList[i],lineList[i+1])
            #print(lineList[i][4:])
            
            if lineList[i][4:] == 'P0_lat':
                self.plotCROdataBlock(m,df[lineList[i]].values,
                                         df[lineList[i+1]].values,10,'red')
            elif len(lineList[i][4:]) == 6:
                self.plotCROdataBlock(m,df[lineList[i]].values,
                                         df[lineList[i+1]].values,10,'blue')
            else:
                self.plotCROdataBlock(m,df[lineList[i]].values,
                                         df[lineList[i+1]].values,10,'turquoise')
        return m