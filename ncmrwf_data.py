import numpy as np
import os
import glob
np.set_printoptions(threshold=np.inf)
import numpy.ma as ma
from netCDF4 import Dataset
path="ncmrwf_files/"
files = glob.glob(os.path.join(path, "*.nc"))
nwp= [Dataset(file,more="r") for file in files]
maskfile=Dataset("mask.nc", more="r")
mask=ma.getmask(maskfile.variables["RAINFALL"][0][1:,3:-4])

Data=[[],[],[],[],[]]
for k in range(len(nwp)):
	if (nwp[k].variables["APCP_sfc"].shape[0]==1460):
		loop=range(608,1088,24)
	else:
		loop=range(611,1091,24)
  
	for i in loop:
		DP=np.zeros(128)
		for p in range(i,i+24):
			temp=np.array(nwp[k].variables["APCP_sfc"][p,:,:])
			DP=np.add(temp,DP)
		DP=np.divide(DP,24)
		for j in range(mask.shape[0]):
			for l in range(mask.shape[1]):
				if mask[j][l]== True:
					DP[j][l]=-1
		if (np.amax(DP)!=0):
			DP=DP/np.amax(DP)
		DP[DP<0]=-1.0

		Data[0].append(DP[0:48,20:68])
		Data[1].append(DP[40:88,0:48])
		Data[2].append(DP[40:88,40:88])
		Data[3].append(DP[50:98,80:128])
		Data[4].append(DP[80:128,15:63])

ncmrwfdata= np.concatenate((np.array(Data[4]), np.array(Data[1]), np.array(Data[2]), np.array(Data[3]), np.array(Data[0])), axis=0)
print(ncmrwfdata.shape)
np.save("ncmrwfdata",ncmrwfdata)
		

		
