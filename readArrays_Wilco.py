import os
import numpy as np
import pcraster as pcr

MV= -999.9
nrRows= 10; nrCols= 10
cloneMapFileName= 'temp_clone.map'

#-create and set temporary clone
command= 'mapattr -s %s -R %d -C %d' %\
  (cloneMapFileName,nrRows,nrCols)
os.system(command)
pcr.setclone(cloneMapFileName)
os.remove(cloneMapFileName)

#-get unique IDs and create some random map of those IDs
pandasList= np.arange(1,101)
a= pandasList.copy()
#np.random.shuffle(a)
a.shape= (nrRows,nrCols)

cellID= pcr.numpy2pcr(pcr.Nominal,a,0)
pcr.aguila(cellID)
a= None
del a
#-set one panda ID to a non-existing value
pandasList[-1]= 999
print pandasList

#-next find entry of each ID of the pandas list within the map
# to create an array of map locations
pandasKeys= np.ones(pandasList.shape)*int(MV)
print pandasKeys
a= pcr.pcr2numpy(cellID,MV).ravel()
print a
n= np.arange(a.size)

print n

iCnt= 0
for ID in pandasList:
  if ID in a:
    #print ID
    key= n[a == ID]
    pandasKeys[iCnt]= key
    print 'panda ID %d has been matched with %d at entry %d' %\
      (ID, a[key], key)
  else:
    print 'panda ID %d cannot be matched' % ID
  iCnt+= 1
a= None; n= None
del a, n
#-next, any map converted to an array can be linked directly to the pandas IDs
# re-using the keys
a= pcr.pcr2numpy(cellID,MV).ravel()
print 'panda IDs with keys'
print pandasList[pandasKeys != int(MV)]
print 'panda keys'
print pandasKeys[pandasKeys != int(MV)]
print 'cell ids'
print a[pandasKeys != int(MV)]


print 
  


##cellID= pcr.uniqueid(pcr.boolean(1))
##pandasIDList= pcr.pcr2numpy(cellID,0).ravel().astype(int).tolist()
##np.random.shuffle(pandasIDList)
##print pandasIDList
###-find entries 


