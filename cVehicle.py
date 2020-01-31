# -*- coding: utf-8 -*-
"""
    checkVehiclePosition
    14.12.2018
    Version 1.0
    by Dipl.-Ing (FH) Sebastian Keidler
    ADrive LivingLab Kempten
"""

__author__ = "Dipl.-Ing(FH) Sebastian Keidler"
__version__ = "1.0"
__email___ = "sebastian.keidler@hs-kempten.de"
__status__ = "Develop"

#%%
from shapely.geometry import Polygon, Point, MultiPolygon
import shapefile
import time
from tqdm import tqdm
import sys
import os
import os,sys,inspect
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from scipy import interpolate
#sys.path.append("../")
import methods.distanceWGS84 as wgs84
import methods.plotVehicleonRoad as pvr
import methods.plotVehicleonRoadJupyterNotebook as pvrjn
import methods.importVehicledata as vd
#os.chdir('..')



#%%


class Vehicle():
    
    
    
    
    def __init__(self):
        
        
        #geth current path
        self.cwd = os.getcwd()

        
        



        #Road input
        #plot Text
        self.listofLines = ['M0','P0',
                   'P0P1',
                   'P1','P2',
                   'P2P3',
                   'P3','P4']
        #all excisting roads
        self.roadpolypath = 'AdriveRoadsSHP/ADriveRoads.shp'
        #all ADrive Roads
        self.listADriveRoads = ['A7N',
                            'A7S',
                            'A8W',
                            'B19S',
                            'B295W',
                            'L1180S',
                            'L1180N']
        
        
        self.dictADriveRoads = {'A7N':[],
                                'A7S':['CRO_RoadBook1.0/data/A7/south/griddata/cro/A7.S.L0.R1.ASCII.cro',
                                       'CRO_RoadBook1.0/data/A7/south/griddata/cro/A7.S.L1.R1.ASCII.cro'],
                                'A8W':[],
                                'B19S':[],
                                'B295W':[],
                                'L1180S':[],
                                'L1180N':[]
                                }
        #get pandas Datafame of .cro roads
        self.dfCROLayer0Road = []
        self.dfCROlayer1Road = []
        
        #dataframe CRO road layer 0 for NearestNeigbourSearch
        self.dfroadL0cro =[]
        
        #nearest Neigbour
        self.minIdx = []
        
        #get  lateral grid cro road coordinates
        self.lateralGridCoords =[]
        
        #current Road Coorinates
        self.rlat = 0
        self.rlon = 0
        self.rele = 0
        
        #get the distance to all lines 
        self.ldistance2lines = []
        
        
        #print(os.chdir('..'))
        #Path to Shapefile of ADrive Roads
        polygon = shapefile.Reader(self.roadpolypath) 
        #get polygon
        polygon = polygon.shapes() 
        
        shpfilePoints = [ shape.points for shape in polygon ]
        
        #print(shpfilePoints)
        
        self.polygons = shpfilePoints
        
 


       
    def VehicleDGPSSimulator(self,lat,lon):
        
        self.vlat = lat
        self.vlon = lon                
         #Vecile Input
        self.vpoi = np.array([[self.vlat,self.vlon]])
               





    
    def checkWhichRoad(self):
        

        
        i = 0
        
        for polygon in self.polygons:
            
            poly = Polygon(polygon)
            
            point = Point(float(self.vlon),float(self.vlat))
            
            if point.within(poly) == True:
                print('Fahrzeugposition ist auf ADrive Roads:   ', self.listADriveRoads[i])
                road = self.listADriveRoads[i]
                
            elif point.within(poly) == False:
                road = 'None'
                print('Fahrzeugposition nicht auf ADrive Roads:   ', self.listADriveRoads[i])
                break
            
            i = i + 1
        
        return road
    
    
    
    
    
    def importRoadLayer(self,road,layer):
        #get crolayerpath from dict 
        crolayerpath = self.dictADriveRoads.get(road)

        
        # Wenn der Layer 0 gewählt wird 
        if layer == 0:
            
    
            #Road Data
            self.dfCROLayer0Road = pd.read_csv(crolayerpath[layer],sep=',', skiprows = 40)
            
            # CRO Layer0 DATA to Lines cache load in Arbeitsspeicher
    
    
            roadP0L0points = []
            roadM0L0points = []
            roadP1L0points = []
            roadP2L0points = []
            roadP3L0points = []
            roadP4L0points = []
        
            # Linien der Straße werden geladen
            #self.dfcurrentCRORoad.
            
#LineM0_lat,LineM0_lon,LineM0_ele,LineP0_lat,LineP0_lon,LineP0_ele,LineP0P1_lat,LineP0P1_lon,LineP0P1_ele,LineP1_lat,LineP1_lon,LineP1_ele,LineP2_lat,LineP2_lon,LineP2_ele,LineP2P3_lat,LineP2P3_lon,LineP2P3_ele,LineP3_lat,LineP3_lon,LineP3_ele,LineP4_lat,LineP4_lon,LineP4_ele
     
            
            for i in range(0,len(self.dfCROLayer0Road.LineP0_lon.values),1):
                #LineP0
                roadP0L0point = np.array([self.dfCROLayer0Road.LineP0_lat.values[i],
                                          self.dfCROLayer0Road.LineP0_lon.values[i]])
                roadP0L0points.append(np.array(roadP0L0point))
                #LineM0
                roadM0L0point = np.array([self.dfCROLayer0Road.LineM0_lat.values[i],
                                          self.dfCROLayer0Road.LineM0_lon.values[i]])
                roadM0L0points.append(np.array(roadM0L0point))
                #LineP1
                roadP1L0point = np.array([self.dfCROLayer0Road.LineP1_lat.values[i],
                                          self.dfCROLayer0Road.LineP1_lon.values[i]])
                roadP1L0points.append(np.array(roadP1L0point))
                #LineP2
                roadP2L0point = np.array([self.dfCROLayer0Road.LineP2_lat.values[i],
                                          self.dfCROLayer0Road.LineP2_lon.values[i]])
                roadP2L0points.append(np.array(roadP2L0point))    
                #LineP3
                roadP3L0point = np.array([self.dfCROLayer0Road.LineP3_lat.values[i],
                                          self.dfCROLayer0Road.LineP3_lon.values[i]])
                roadP3L0points.append(np.array(roadP3L0point))
                #LineP4
                roadP4L0point = np.array([self.dfCROLayer0Road.LineP4_lat.values[i],
                                          self.dfCROLayer0Road.LineP4_lon.values[i]])
                roadP4L0points.append(np.array(roadP4L0point))




            self.dfroadL0cro = pd.DataFrame({'LineM0':roadM0L0points,
                                             'LineP0':roadP0L0points,
                              'LineP1':roadP1L0points,
                              'LineP2':roadP2L0points,
                              'LineP3':roadP3L0points,
                              'LineP4':roadP4L0points,},
            columns=['LineM0','LineP0','LineP1','LineP2','LineP3','LineP4'])
            
            
            

            for i in range(0,len(self.dfCROLayer0Road.LineP0_lon.values),1):
                roadP0L0point = [self.dfCROLayer0Road.LineP0_lat.values[i],self.dfCROLayer0Road.LineP0_lon.values[i]]
                roadP0L0points.append(roadP0L0point)
            #print(np.array(roadP0L0points))
            self.LineP0 = np.array(roadP0L0points)
            
            
            
        #return dfcurrentCRORoad        
        elif layer == 1:
                
            #Road Data
            self.dfCROLayer1Road = pd.read_csv(crolayerpath[layer],sep=',', skiprows = 40)
            
            pass
            
        

    def searchNearestNeigbourP0(self):
        
        #nntime = time.time()       
        #print(self.dfroadL0cro.LineP0.values)
        self.minIdx = np.argmin(np.linalg.norm(self.LineP0-self.vpoi,axis=1))
        
        #print("--- %s seconds ---  NearestNeigbour" % (time.time() - nntime))  
        
        #print(self.minIdx)
        



    def getLateralGridCoordinatesCRO(self):
        #get the lateral grid coordinates from .cro road
        self.lateralGridCoords = self.dfCROLayer0Road.iloc[[self.minIdx+1]]
        return self.lateralGridCoords
        

        
    def distance2lines(self):
        
        #distance to all lines
        self.ldistance2lines = []
        
        
        #print(self.lateralGridCoords)
        #intteration über alle linien im cro datafile
        for line in range(0,len(self.lateralGridCoords.values[0]),3):
            
            #only lines not middlelines
#            if line == 6 or line == 15:
#                pass
#            
#            else:
                
            # 0 3 6 9 12 15 18 21
            #print(line)
            #calc distance 2 line for each line
            self.rlat = self.lateralGridCoords.values[0][line]
            self.rlon = self.lateralGridCoords.values[0][line+1] 
            self.rele = self.lateralGridCoords.values[0][line+2]
            
            #vector zum nächsten Straßenpunkt 
            vector2NN = wgs84.distanceWGS84(self.vlat,self.vlon,self.rlat,self.rlon)
            
              
            #print(vector2NN)
        
            #berechnung orthogonaler Abstand
            
            #distance of road resolution at current index
            #rsIdx = self.dfCROLayer1Road.s.values[self.minIdx]
            
            #bearing of road resolution at current index
            rbIdx = self.dfCROLayer1Road.bearing.values[self.minIdx]
            #print(rbIdx)
            
            #distance2line[0] postitives Entfernungsmaß
            if vector2NN[1] >= 350 and rbIdx <= 10:
                d2l = math.sin(math.radians(360-vector2NN[1]+rbIdx)*abs(vector2NN[0]))
                
            else:
                d2l = math.sin(math.radians(abs(vector2NN[1]-rbIdx)))*abs(vector2NN[0])
                
                
                #d2l = round(d2l,3)
                self.ldistance2lines.append(d2l)
              
        return self.ldistance2lines
        #print('Distance 2 Lines :',self.ldistance2lines, ' m')
        
    #check which line distance    
    def lanedetection(self):
        #find minimum of list 
        minimum = min(self.ldistance2lines, key=abs)
        #getting index
        index = self.ldistance2lines.index(minimum)
        
        #print('nearest line',self.listofLines[index])
        
        #copy list to get second nearest line
        new_list = self.ldistance2lines.copy()
        #remove the minimum
        new_list.remove(minimum)
        #find second minimum of list 
        minimum2 = min(new_list, key=abs)
        #getting index
        index2 = self.ldistance2lines.index(minimum2)
        
        #print('second nearest line',self.listofLines[index2])
        #print('{0}\r'.format(self.listofLines[index],'<- EGO VEHICLE ->',self.listofLines[index2]))
        #print("Progress {:2.1%}".format(index), end="\r")
        return index,index2
        
        #now the nearest lines are clear calc sign of distance2line
    def calcSigndistance2line(self,index,index2):
        
        #calc mean value
        numb = abs(index+index2)/2
        #counter
        i = 0
        
        for distance2line in self.ldistance2lines:
            
            #right side is positive
            if i <= numb:
                self.ldistance2lines[i] = abs(self.ldistance2lines[i])
                
            #left side is negative
            elif i >= numb:
                
                self.ldistance2lines[i] = (abs(self.ldistance2lines[i])*-1)
                
            i += 1 
        
        return self.ldistance2lines
    
        #width = abs(float(self.distance2lines[0]))+abs(float(self.distance2lines[-1]))
        
        #calculate width of road
        #print('{0}\r'.format(width))
        #print(self.ldistance2lines)
        
        
    def camAlgo(self,index,index2):
        ##CAMERA ALGO HAS NO P0P1 P2P3 
            #self.ldistance2lines[0] -> M0
            #self.ldistance2lines[1] -> P0
            #self.ldistance2lines[2] -> P0P1
            #self.ldistance2lines[3] -> P1
            #self.ldistance2lines[4] -> P2
            #self.ldistance2lines[5] -> P2P3
            #self.ldistance2lines[6] -> P3
            #self.ldistance2lines[7] -> P4
        ix = 0 
        ix2 = 0
        d2l = 0
        #get the closest value to line without P0P1 and P2P3
        
        
        if index == 1 and index2 == 0: # wenn P0 ist  die nöhste dann P0
            d2l = abs(self.ldistance2lines[1])#*-1
            ix = 'P0'
            ix2 = 'M0'
                    
        
        
        elif index == 1 and index2 ==2: #wenn M0 ist die nähste ist und P0 der 
            #der zweitnächste, dann ausßerhalb der STraße 
            d2l = abs(self.ldistance2lines[1])
            ix = 'P0'
            ix2 = 'M0'


                        
            
        elif index == 2 and index2 == 1:
            d2l = abs(self.ldistance2lines[1])
            ix='P0'
            ix2 ='M0'
            
            
        elif index == 2 and index2 == 3:
            d2l = abs(self.ldistance2lines[3])
            ix='P1'
            ix2 ='P2'
            
            
#        elif index == 1 and index2 == 0: # wenn P0 ist  die nöhste dann P0
#            d2l = abs(self.ldistance2lines[1])
#            ix = 'M0'
#            ix2 = 'P0'
#            
#            
#            
#            
#        elif index == 1 and index2 == 2: # wenn P0 ist  die nöhste dann P0
#            d2l = abs(self.ldistance2lines[1])
#            ix = 'P0'
#            ix2 = 'P1'
#
#
#            
#
#            
#
#        elif index == 3 and index2 == 2: # wenn P0 ist  die nöhste dann P0
#            d2l = abs(self.ldistance2lines[3])
#            ix='P1'
#            ix2 ='P2'
#            
#        elif index == 3 and index2 == 4: # wenn P0 ist  die nöhste dann P0
#            d2l = abs(self.ldistance2lines[3])
#            ix='P1'
#            ix2 ='P2'
#            
#        elif index == 4 and index2 == 3: # wenn P0 ist  die nöhste dann P0
#            d2l = abs(self.ldistance2lines[4])
#            ix='P2'
#            ix2 ='P1'
#
#        elif index == 4 and index2 == 5: # wenn P0 ist  die nöhste dann P0
#            d2l = abs(self.ldistance2lines[4])
#            ix='P2'
#            ix2 ='P1'
#            
#            
#        elif index == 5 and index2 == 6:
#            d2l = abs(self.ldistance2lines[5])
#            ix='P3'
#            ix2 ='P4'
#            
#        elif index == 5 and index2 == 4:
#            d2l = abs(self.ldistance2lines[5])
#            ix='P2'
#            ix2 ='P1'
#            
#        elif index == 6 and index2 == 5: # wenn P0 ist  die nöhste dann P0
#            d2l = abs(self.ldistance2lines[6])
#            ix='P3'
#            ix2 ='P4'
#
#        elif index == 6 and index2 == 7: # wenn P0 ist  die nöhste dann P0
#            d2l = abs(self.ldistance2lines[6])
#            ix='P3'
#            ix2 ='P4'
#
#            
#        elif index == 7 and index2 == 6: # wenn P0 ist  die nöhste dann P0
#            d2l = self.ldistance2lines[7]*-1            
#            ix='P4'            
#            ix='P3'
            
            
        return d2l,ix,ix2
        
        
        
    def saveDistance2Line(self,d2l,txtname,i,ix,ix2,index,index2):

        #D2L nearest Point 
        #d2l = min(self.ldistance2lines,key=abs)
        #D2L P0
        #d2l = self.ldistance2lines
        with open(txtname, "a") as myfile:
            myfile.write(str(i)+','+str(d2l)+','+str(index)+','+str(index2)+','+str(ix)+','+str(ix2)+'\n')
            
        
        
            
            
    def plotDistance2Line(self):
        #recalculation
        pvr.plotVehicleonRoad(self.ldistance2lines)
        #pvrjn.plotVehicleonRoadJupyterNotebook(self.distance2lines)
        
        
        #
        
    
    def evalDistance2line(self,txt,vehiclepath):
        #         

        def fill_nan(A):
            '''
            interpolate to fill nan values
            '''
            inds = np.arange(A.shape[0])
            good = np.where(np.isfinite(A))
            f = interpolate.interp1d(inds[good], A[good],bounds_error=False)
            B = np.where(np.isfinite(A),A,f(inds))

            return B
        

        dfvehicle = vd.importVehicledata(vehiclepath)
        #interpolate nans
        ldwdlc = fill_nan(dfvehicle.d2l.values)
        yCam = list(ldwdlc)
        
        graphData = open(txt,"r").read()
        lines = graphData.split("\n")
        lines = lines[:-1]
        
        
        
        xValues = []
        yValues = []
        ixValues =[]
        ix2Values =[]
        indexValues =[]
        indexValues2 =[]
        for line in lines:
            
            if len(line) > 1:
                x, y, ix, ix2, index, index2 = line.split(",")
                xValues.append(x)
                yValues.append(y)
                ixValues.append(ix)
                ix2Values.append(ix2)
                indexValues.append(index)
                indexValues2.append(index2)
                
        print(len(xValues),len(lines),len(yValues),len(yCam))
        

        
        dfd2l = pd.DataFrame({'x':xValues,
                              'd2lGT':yValues,
                              'd2lCAM':yCam,
                              'nearestIndex':ixValues,
                              'secondIndex':ix2Values,
                              'nearestline':indexValues,
                              'secondline':indexValues2},
                columns=['x','d2lGT','d2lCAM','nearestIndex','secondIndex',
                         'nearestline','secondline'])

        
            #get list from pandas 
        liste = []
        
        for i in range(0,len(dfd2l.d2lGT.values),1):
            liste.append(dfd2l.d2lGT.values[i])
            
        #replace 0 wit NaN
        new_items = [np.nan if x == 0 else x for x in liste]
        
        #Interpolate NAN
        yValues = fill_nan(np.array(new_items))
                
        #replace pandas
        dfd2l["d2lGT"] = yValues
        
        #
        print(dfd2l[470:490])
        
        dfd2l.to_csv('Distance2Line.csv',sep=',',index=False)
        

        
        
    
    
        
#    def distance2Line(self,):
        
        
#    def getNearestLine():
#    def loadRoad(self,road):
        
    

    
        
    
