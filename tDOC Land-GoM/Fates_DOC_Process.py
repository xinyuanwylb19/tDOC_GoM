import scipy.io
import numpy as np
from numpy import genfromtxt

mat=scipy.io.loadmat('Fates_DOC.mat')
fates_DOC=mat['ts']

biom_file='Biom.csv'
biom_data=genfromtxt(biom_file,delimiter=',')

'''
results=[]
half_DOC=[]

for i in range (92):
    day_data=fates_DOC[i][:,3]
    results.append(day_data)
    
    for j in range (180):
        if day_data[j]<50:
            half_DOC.append(j)
            break
                  
np.savetxt('Suspended_DOC.csv',results,delimiter=',')
np.savetxt('half_DOC.csv',half_DOC,delimiter=',')
'''

'''
results=[]

for i in range (92):
    day_data=fates_DOC[i][:,2]
    results.append(day_data)
                  
np.savetxt('BioM_DOC.csv',results,delimiter=',')
'''

'''
day_data=fates_DOC[0]                 
np.savetxt('day_data1.csv',day_data,delimiter=',')
'''
    
    
    