# statistical functions involved in processing geochemical data for use in clustering and ML
from itertools import combinations
import pandas as pd
import math
import numpy as np
from importlib import reload
from scipy import stats

# ==========================================================
#pairwise correlations between columns
def corrcolumns(df):

    All_Corr=[]
    x_=len(df.columns)
    
    correlation_mat_=df.corr()
    correlation_mat=correlation_mat_.abs()

    Corr_Avg=[]
    for i in range(x_):
        corr_sum=(correlation_mat.iloc[:,i].sum())-1
        corr_avg=(corr_sum/(x_-1))
        Corr_Avg.append(corr_avg)

    corr=pd.DataFrame(Corr_Avg)      
    avg_corr=corr.mean()
    All_Corr.append(avg_corr)

    return corr, avg_corr, Corr_Avg

# ==========================================================
#coefficient of variation
def coefvar(df):
    from scipy.stats import variation
    
    All_Var=[]
    var_=(variation(df))*100
    var=pd.DataFrame(var_)
    avg_var=var.mean()
    All_Var.append(avg_var)
    
    return var, avg_var, All_Var

# ==========================================================
#dip test
#downloaded from https://github.com/BenjaminDoran/unidip
#note that you need to correct the smoothness of the histograms to avoid divide by zero errors: https://github.com/BenjaminDoran/unidip/issues/3

def diptest(df):
    from unidip import UniDip
    import unidip.dip as dip
    reload(dip)
    
    All_Dip=[]
    Dip=[]
    Dip_mean=[]
    
    x_=len(df.columns)

    for z in range(x_):
#    intervals = UniDip(np.msort(df2.iloc[:,z])).run()
#    Dip.append(len(intervals))
        dip_prob=dip.diptst(df.iloc[:,z])[1]
#           dip_mean=(dip_prob[0]+dip_prob[1])/2
        Dip_mean.append(dip_prob)

#dip_value=pd.DataFrame(Dip)
    dip_p_avg=pd.DataFrame(Dip_mean)

    avg_d=dip_p_avg.mean()
    All_Dip.append(avg_d)


    #print(avg_d)
    #print(dip_p_avg[dip_p_avg < .5].count())
    return dip_p_avg, avg_d, All_Dip


# ==========================================================


    