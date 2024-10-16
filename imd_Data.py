import os
import glob
import numpy as np
np.set_printoptions(threshold=np.inf)
from netCDF4 import Dataset
path="netcdf_files/"
files = glob.glob(os.path.join(path, "*.nc"))
imdrain= [Dataset(file,more="r") for file in files]
Data=[[],[],[],[],[]]
scalefactor=[]
for k in range(len(imdrain)):#len(Highres)
  if (imdrain[k].variables["RAINFALL"].shape[0]==365):
    loop=range(152,270,6)
  else:
    loop=range(153,271,6)

  for i in loop:
    DP=np.zeros(128)
    for j in range(i,i+6):
      temp=np.array(imdrain[k].variables["RAINFALL"][j,1:,3:-4])
      DP=np.add(temp,DP)
    DP=np.divide(DP,6)
    scalefactor.append(np.amax(DP))
    if (np.amax(DP)!=0):
      DP=DP/np.amax(DP)

    DP[DP<0]=-1.0
    Data[0].append(DP[0:48,20:68])
    Data[1].append(DP[40:88,0:48])
    Data[2].append(DP[40:88,40:88])
    Data[3].append(DP[50:98,80:128])
    Data[4].append(DP[80:128,15:63])

imddata= np.concatenate((np.array(Data[4]), np.array(Data[1]), np.array(Data[2]), np.array(Data[3]), np.array(Data[0])), axis=0)
print(imddata.shape)
scalefactor=np.array(scalefactor*5)
print(scalefactor.shape)
np.save("scalefactor", scalefactor)
#np.save("imddata_final", imddata)







"""COLAB CODE
#packages import 
import numpy as np
import os 
import glob
import tensorflow as tf
from tensorflow import keras
from keras.layers import Concatenate
from numpy import expand_dims
import numpy.ma as ma
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import matplotlib.cm as mtpltcm
#from mpl_toolkits.mplot3d import Axes3D
import random
#from netCDF4 import Dataset
#import cartopy.crs as ccrs
np.set_printoptions(threshold=np.inf)
from warnings import filterwarnings
filterwarnings("ignore",category=DeprecationWarning)
filterwarnings("ignore", category=FutureWarning) 
filterwarnings("ignore", category=UserWarning)
filterwarnings("ignore", category=RuntimeWarning)
tempdata="/content/drive/MyDrive/gpcast_project/imddata_final.npy"
data=np.load(tempdata)

def obsfunc(data):
	data=tf.convert_to_tensor(data)
	data=tf.expand_dims(data, axis=-1)
	data=tf.cast(data,tf.float32)
	return data

imdfile=obsfunc(data)"""




