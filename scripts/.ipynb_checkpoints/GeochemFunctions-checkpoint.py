# functions involved in processing geochemical data for use in clustering and ML
from itertools import combinations
import pandas as pd
import math

# ==========================================================
# make ratios between every column of a dataframe and every other, then append onto orininal
def makeratios(DF):
    cc = list(combinations(DF.columns,2))
    cnames=[]
    for c in cc:
        cname=c[1] + '/' +c[0]
        cnames.append(cname)
    
    ratios = pd.concat([DF[c[1]].divide(DF[c[0]]) for c in cc], axis=1, keys=cnames)
    #now append the ratios onto the original dataframe
    df_wratios = pd.concat([DF,ratios],axis=1)
    
    return df_wratios



# ==========================================================

#function to find the number of distinct ratios between elements in a list
def numcomb(n,k):
    Cnk = math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    return Cnk

# ==========================================================

#function to normalize a dataframe 

def normalizedata(df,method):
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.preprocessing import PowerTransformer  
    from sklearn.preprocessing import Normalizer
# Min Max Scaler

    if method == 'minmax':
        dfi= MinMaxScaler().fit_transform(df)
        dfo =pd.DataFrame(dfi)
    elif method == 'powert':
        dfi= PowerTransformer().fit_transform(df)
        dfo =pd.DataFrame(dfi)
    elif method == 'normalize':
        dfi= Normalizer().fit_transform(df)
        dfo =pd.DataFrame(dfi)
    elif method == 'columnnorm':
        dfi= df.mean()
        dfo = df.divide(dfi, axis=1)
        
    return dfo

# ==========================================================

#function to normalize a dataframe 
def scaledata(df,method):
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import RobustScaler
    
    if method == 'standardscalar':
        dfi= StandardScaler().fit_transform(df)
        dfo =pd.DataFrame(dfi)
    elif method == 'robustscalar':
        dfi= RobustScaler().fit_transform(df)
        dfo =pd.DataFrame(dfi)
    elif method == 'morb':
        dfo=df
        
    return dfo
    
    
    

