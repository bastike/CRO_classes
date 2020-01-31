"""@package docstring
Class to evaluate ADAS with KPI's
"""
import warnings
from scipy.signal import filtfilt, butter
import numpy as np
from scipy import interpolate
import os,sys,inspect
import scipy.io as sio
import numpy as np
import pandas as pd
import random




class cDataHandling:


    def __init__(self):
        # current directory path
        self.sCurrentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # current parent directory path
        self.sParentDir = os.path.dirname(self.sCurrentDir)
        # current grandparent directory path
        self.sGrandParentDir = os.path.dirname(os.path.dirname(self.sCurrentDir))
        # all available CRO roads
        #self.oRoadslist = ['A7','A8','B19','B295','L1180']
        
        
        
        
    def getfilenamefrompath(self,mypath):
        '''
        the function gives back all file names as stings in a folder by the path
        @:param mypath            [in]    string of the folder path
        @:param onlyfiles         [out]   string list of all file names with data format
        '''
        onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        return onlyfiles
        
        
        
    def getfoldernamefrompath(self,mypath):
        '''
        the function gives back all folder names as stings in a folder by the path
        @:param mypath          [in]    string of the folder path
        @:param dirlist         [out]   string list of all filder names
        '''
        dirlist = [ item for item in os.listdir(mypath) if os.path.isdir(os.path.join(mypath, item)) ]
        return dirlist
        
        
        
        
    def randomNumber(self,versionnumber):
        '''
        the function generates a random nummber 6 letters and startung with versionsnumber
        @:param versionnumber     [in]    Versionsnummer 1,2,3,...
        @:param numbsum           [out]   Identifyer number 
        '''
        numbsum = 0
        for x in range(versionnumber * 10000):
            numbsum = random.randint(1,21)*versionnumber + numbsum
        return numbsum
        
        
        
        
    def getIndexClosestGPSpoint(self,afArray,fLat,fLon):
        '''
        get the index of the closest GPS-point of an array to a given GPS-point
        @:param afArray          [in]    array of GPS-points
        @:param fLat             [in]    Latitude as float
        @:param fLon             [in]    Longitude as float
        @:param nIndex           [out]   index 
        '''
        return np.argmin(np.linalg.norm(afArray-[fLat,fLon],axis=1))
       
    def fill_nan(self,A):
        '''
        interpolate to fill nan values
        '''
        inds = np.arange(A.shape[0])
        good = np.where(np.isfinite(A))
        f = interpolate.interp1d(inds[good], A[good],bounds_error=False)
        B = np.where(np.isfinite(A),A,f(inds))
        return B
        
    def calcLowPassFilter(self,afInput,iOrder,fFrequenzy):
        """
        import the cro road data as pandas DataFrame
        @:param afInput           [in]    road path
        @:param iOrder            [in]    road name
        @:param fFrequenzy        [in]    road direction
        @:param afOutput          [out]   road data as pandas DataFrame
        """
        with warnings.catch_warnings():
            # Create an order 2 lowpass butterworth filter.
            b, a = butter(iOrder, fFrequenzy)            
            # Use filtfilt to apply the filter.
            afOutput = filtfilt(b, a, afInput)
        return afOutput
        
        
    def checkUniqueValues(self,mylist):
        newList=[]
        indexList = []
        valuesList = []
        for i in range(len(mylist)):
            if mylist[i] == 0:
                pass
            elif mylist[i] not in newList:
                newList.append(mylist[i])
            else:
                indexList.append(i)
                valuesList.append(mylist[i])
        if len(mylist) == len(newList):
            print('All data are unique')
        else:
            print('Some double values')
        return indexList,valuesList
    
    
    
    
    def correctCROdoubledValues(self,df):
        
        for i in range(len(df.columns)):
            if df.columns[i][-3:] == 'ele':
                pass
            else:
                print(df.columns[i])
                print(self.checkUniqueValues(list(df[df.columns[i]].values)))
                indexList,valuesList = self.checkUniqueValues(list(df[df.columns[i]].values))
                for index in indexList:
                    df[df.columns[i]].values[index] = df[df.columns[i]].values[index]+ 0.0000000001
                    print(self.checkUniqueValues(list(df[df.columns[i]].values)))
        return df
    
    
    
    
    def importMAT(self,path):
        """
        import the cro road data as pandas DataFrame
        @:param path              [in]   path to mat file
        @:param df                [out]   road data as pandas DataFrame
        """
        df = pd.DataFrame()
        #load mat file
        mat = sio.loadmat(path)
        #get filename
        filename = sio.whosmat(path)[0][0]
        #get columns names
        liste = mat[filename].dtype.descr
        #itteration over column names
        counter = 0
        for i in liste:
            #print(i[0])
            
            for j in range(len(mat[filename][0][0][1].dtype.descr)):
                #print(counter,j)
                #print(mat[filename][0][0][1].dtype.descr[j][0])
                #print(i[0]+'_'+mat[filename][0][0][1].dtype.descr[j][0])
                df[i[0]+'_'+mat[filename][0][0][1].dtype.descr[j][0]] = [float(mat[filename][0][0][liste[counter][0]][0][0][j][k][0]) for k in range(len(np.array(mat[filename][0][0][liste[0][0]][0][0][0])))]
            counter = counter + 1
        return df