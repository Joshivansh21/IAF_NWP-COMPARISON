import os
import glob
import numpy as np
np.set_printoptions(threshold=np.inf)
import numpy.ma as ma
from netCDF4 import Dataset
path="gfs_files/"
files = glob.glob(os.path.join(path, "*.nc"))
gfsrain= [Dataset(file,more="r") for file in files]

maskfile=Dataset("mask.nc", more="r")
mask=ma.getmask(maskfile.variables["RAINFALL"][0][1:,3:-4])
size(133,133)
Data=[[],[],[],[],[]]
for i in range(0,len(gfsrain),6):
	DP=np.zeros(size)
	
	DP=np.array(gfsrain[i].variables["A_PCP_L1_Accum_1"][0,:,:])
	
	



DP=DP[2:-3,5:]
	
	if (np.amax(DP)!=0):
            		DP=DP/np.amax(DP)

	for j in range(mask.shape[0]):
			for k in range(mask.shape[1]):
				if mask[j][k]== True:
					DP[j][k]=-1
	Data[0].append(DP[0:48, 20:68])
	Data[1].append(DP[40:88,0:48])
	Data[2].append(DP[40:88,40:88])
	Data[3].append(DP[30:78,80:128]) #50 to 98 if data not flipped
	Data[4].append(DP[80:128,15:63])

GFSdata= np.concatenate((np.array(Data[4]), np.array(Data[1]), np.array(Data[2]), np.array(Data[3]), np.array(Data[0])), axis=0)
	
print(GFSdata.shape)
