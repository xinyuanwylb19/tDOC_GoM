# Terrestrial-aquatic DOC fluxes model (TAF-DOC)
# Version 2
# Daliy simulation time step
# Xinyuan Wei
# 2022.10.02

import pandas as pd
import numpy as np
import math

# Read the diver data.
soiloc=pd.read_csv('Driver_SOC.csv')
wtland=pd.read_csv('Driver_Wetland.csv')
opwate=pd.read_csv('Driver_Openwater.csv')
watrew=pd.read_csv('Driver_WRTW.csv')
watred=pd.read_csv('Driver_WRTD.csv')

temp=pd.read_csv('Driver_Temp.csv')
prep=pd.read_csv('Driver_Prep.csv')
SDep=pd.read_csv('Driver_SDep.csv')
NDep=pd.read_csv('Driver_NDep.csv')

# The total number of days.
tdays=90

# The total number of watersheds.
twtsd=len(wtland)

# Outout results
DOC_Expt=[]
DOC_Burl=[]
DOC_Minl=[]

########################################
# Parameters
########################################
# Soil DOC parameters
sp1=0.1356
sp2=0.956

# Watershed DOC loading parameters
wp0=1.2369
wp1=-0.0072
wp2=0.0047
wp3=-0.4039
wp4=0.3055
wpe=-0.12073

wpp0=1.2361
wpp1=0.0053
wpp2=-0.1976

MaDOC=15
MiDOC=1.76

burp1=0.0896
burp2=0.0121

minp1=0.1563

# Delivery process.
dbp1=0.0005
dbp2=148.61

dmp1=1.441

# Maximum DOC export. Model results constratin g/m2
MDOC=15

print ('The total number of watershed is',twtsd,'.')
print ('The total number of simulated days is',tdays,'.')

########################################
# SDOCM, Soil DOC concentration.
# The DOC is g/m2.
########################################
def SDOCM(SOC):
    SDOC=sp1*sp2*SOC
    return(SDOC)

########################################
# DOCFM, DOC flux to the ocean.
# The DOC is g/day.
########################################
def WFDOCM(W, T, P, S, N, OW, WRW, WRD):
    # DOC export from a watershed.
    # If some environmental factors are not available. 
    if T!=0 and S!=0 and N!=0:
        DOCE=wp0*W+wp1*T+wp2*P+wp3*S+wp4*N+wpe
        
    # Only pricipitation
    else:
        DOCE=wpp0*W+wpp1*P+wpp2
        
    # Outliers
    if DOCE>MaDOC:
        DOCE=MaDOC
        
    if DOCE<0:
        DOCE=MiDOC

    # DOC buried within the watershed. 
    DOCB=burp1*math.exp(burp2*OW)*DOCE
    
    # DOC mineralized within the watershed.
    DOCM=minp1*WRW*DOCE
    
    # DOC buried and mineralized during the delivery process.
    DOCEB_r=dbp1*math.exp(dbp2*WRD)*DOCE
    DOCEM_r=dmp1*WRD*DOCE
    
    if (DOCEB_r+DOCEM_r)>0.17:
        DOCEB_r=0.06
        DOCEM_r=0.11

    DOCEB=DOCE*DOCEB_r
    DOCEM=DOCE*DOCEM_r
    
    DOCBB=DOCB+DOCEB
    DOCMM=DOCM+DOCEM
    DOCEE=DOCE-DOCEB-DOCEM
    
    return(DOCBB,DOCMM,DOCEE)

# Estimation for each watershed.
for i in range (twtsd):
    
    print('Calculation for the watershed:',str(i+1))
    wtsd_ID=i
    
    WT=wtland.at[wtsd_ID,'Wetland']
    OW=opwate.at[wtsd_ID,'Openwater']
    
    WRT_W=watrew.at[wtsd_ID,'WRTW']
    WRT_D=watred.at[wtsd_ID,'WRTD']
    
    SOC=soiloc.at[wtsd_ID,'SOC']
    
    # Soil DOC.
    SDOC=SDOCM(SOC)

    temp_DOCB=[]
    temp_DOCM=[]
    temp_DOCE=[]

    for j in range (tdays):
        Tj=float(temp.iloc[i,j])
        Pj=float(prep.iloc[i,j])
        Sj=float(SDep.iloc[i,j])
        Nj=float(NDep.iloc[i,j])
        
        DOC_B=WFDOCM(WT, Tj, Pj, Sj, Nj, OW, WRT_W, WRT_D)[0]
        DOC_M=WFDOCM(WT, Tj, Pj, Sj, Nj, OW, WRT_W, WRT_D)[1]
        DOC_E=WFDOCM(WT, Tj, Pj, Sj, Nj, OW, WRT_W, WRT_D)[2]
        
        # DOC loading should be less than SDOC
        if (DOC_B+DOC_M+DOC_E)>SDOC:
            DOC_B=0.1396*SDOC
            DOC_M=0.2563*SDOC   
            DOC_E=0.3563*SDOC
            
        temp_DOCB.append(DOC_B)
        temp_DOCM.append(DOC_M)
        temp_DOCE.append(DOC_E)
        
    DOC_Burl.append(temp_DOCB)
    DOC_Minl.append(temp_DOCM)
    DOC_Expt.append(temp_DOCE)

np.savetxt('DOC_Burial.csv', DOC_Burl, delimiter=',')
np.savetxt('DOC_Mineral.csv', DOC_Minl, delimiter=',')
np.savetxt('DOC_Export.csv', DOC_Expt, delimiter=',')
