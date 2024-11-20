# functions involved in processing geochemical data for use in clustering and ML
from itertools import combinations
import pandas as pd
import math

# ==========================================================
# make ratios between every column of a dataframe and every other, then append onto orininal
def makeratios(DF):
    """
    compute ratios of every element in a list with every other
    DF is a pandas dataframe containing features of interest
    """    
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

def normalizedata(df,method):
    """
    normalize a dataframe with various options
    df is a pandas dataframe containing features of interest
    method is how we want to normalize
    """      
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.preprocessing import PowerTransformer  
    from sklearn.preprocessing import Normalizer
    from scipy.stats import zscore


    if method == 'minmax':
        # Min Max Scaler
        dfi= MinMaxScaler().fit_transform(df)
        dfo =pd.DataFrame(dfi)
    elif method == 'powert':
        dfi= PowerTransformer().fit_transform(df)
        dfo =pd.DataFrame(dfi, columns=df.columns)        
    elif method == 'normalize':
        dfi= Normalizer().fit_transform(df)
        dfo =pd.DataFrame(dfi)
    elif method == 'columnnorm':
        dfi= df.mean()
        dfo = df.divide(dfi, axis=1)
    elif method == 'zscore':
        #Remove outliers
        #dropping rows that are greater than 3 standard deviations away from mean ..?
        z_scores = stats.zscore(df) #calculate z-scores of `df`
        abs_z_scores = np.abs(z_scores)
        filtered_entries = (abs_z_scores < 3).all(axis=1)
        df = df[filtered_entries]
  
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
     
# ==========================================================

#function to return the indices of a list that match a given value
#https://stackoverflow.com/questions/16685384/finding-the-indices-of-matching-elements-in-list-in-python
def find(lst, array, a):
    #     return [i for i, x in enumerate(lst) if x==a]
    result = []
    if len(array)!=0:
        for i, x in enumerate(lst):
            if x==a:
                result.append(array[i])#
    else:
        for i, x in enumerate(lst):
            if x==a:
                result.append(i)#
    #print(result)    
    return result
    

