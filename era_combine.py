import os
import glob
import numpy as np
import numpy.ma as ma
from netCDF4 import Dataset
#path="GFSDATA/"
#files = glob.glob(os.path.join(path, "*.nc"))
#gfsrain= [Dataset(file,more="r") for file in files]
era=Dataset("era.nc", more="r")
imd=Dataset("RF25_ind1999_rfp25.nc", more="r")
eratemp=era.variables["t2m"]
eratcw=era.variables["tcw"]
def trimfunc(eradata):
	eradata=np.array(eradata)
	eradatacopy=np.concatenate((eradata[0:2880,:,:],eradata[2928:5808],eradata[5856:8736,:,:],eradata[8784:11664,:,:]),axis=0)
	return(eradatacopy)
eratemp= trimfunc(eratemp)
eratcw= trimfunc(eratcw)		

#print(eratcw.shape)
#print(eratemp.shape)

size = (133,133)
mask=ma.getmask(imd.variables["RAINFALL"][0][1:,3:-4])

def sixhrs_combine(eradata, size, mask):
	Data=[[],[],[],[],[]]
	
	for i in range(0,eradata.shape[0],6):
		DP=np.zeros(size)
		for j in range(i,i+6):
			temp=np.array(eradata[j,:,:])
			DP=np.add(temp,DP)
		DP=np.divide(DP,6)
		DP=DP[2:-3,5:]
		DP=np.flip(DP, axis=0)
		if (np.amax(DP)!=0):
            		DP=DP/np.amax(DP)		
		
		
		for j in range(mask.shape[0]):
			for k in range(mask.shape[1]):
				if mask[j][k]== True:
					DP[j][k]=-1
		
		Data[0].append(DP[0:48, 20:68])
		Data[1].append(DP[40:88,0:48])
		Data[2].append(DP[40:88,40:88])
		Data[3].append(DP[30:78,80:128])
		Data[4].append(DP[80:128,15:63])
	output= np.concatenate((np.array(Data[4]), np.array(Data[1]), np.array(Data[2]), np.array(Data[3]), np.array(Data[0])), axis=0)
	return output

Tempdata=sixhrs_combine(eratemp, size, mask)
Tcwdata= sixhrs_combine(eratcw, size, mask)
#TEMP=np.array(Tempdata)
#TCW=np.array(Tcwdata)
print(Tempdata.shape)
print(Tcwdata.shape)
np.save("eratemp", Tempdata)
np.save("eratcw", Tcwdata)


"""Data=[[],[],[],[],[]]
for i in range(len(gfsrain)):
	DP=np.array(gfsrain[i].variables["RAINFALL"][i,:,:])
	DP=DP[3:-2,5:]
	
	if (np.amax(DP)!=0):
            		DP=DP/np.amax(DP)

	for j in range(mask.shape[0]):
			for k in range(mask.shape[1]):
				if mask[j][k]== True:
					DP[j][k]=-1
	Data[0].append(DP[0:48, 20:68])
	Data[1].append(DP[40:88,0:48])
	Data[2].append(DP[40:88,40:88])
	Data[3].append(DP[30:78,80:128]) #50 to 98 if data not flipped like in case of era
	Data[4].append(DP[80:128,15:63])
GFSprecip=[Data[4], Data[1], Data[2], Data[3], Data[0]]
	
GFS=np.array(GFSprecip)"""













