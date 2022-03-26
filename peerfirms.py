import pandas as pd
import numpy as np
import scipy

'''
data format

PERMNO date TICKER RET year month
10001 1995-01-31 EWST -0.031250 1995 1
10001 1995-02-28 EWST -0.026210 1995 2
10001 1995-03-31 EWST 0.006377 1995 3
10001 1995-04-28 EWST 0.000000 1995 4
10001 1995-05-31 EWST 0.050000 1995 5
'''

class MsgError(Exception):
    pass

class PeerFirm:
    
    def __init__(self, monthly_return_file):
        print('**************loading the file**************')
        self.df = pd.read_csv(monthly_return_file) #read in monthly stock return file
        print('number of rows:', self.df.shape[0])
        
        self.df['RET'] = self.df['RET'].apply(pd.to_numeric, errors='coerce')
        self.df = self.df.dropna(subset=['RET'])
        self.df['date'] =  pd.to_datetime(self.df['date'], format='%Y%m%d')
        self.df['year'] = self.df['date'].apply(lambda x: x.year)
        self.df['month'] = self.df['date'].apply(lambda x: x.month)
        print('number of rows after removing nan:', self.df.shape[0])
        print('**************finish loading**************')
        
        
    def rsquared(self, focal, peers, years):
        '''
        focal: a list, [AAPL]
        peers: a list, ['MSFT', 'AAPL']
        years: a list, [2012, 2013]
        '''
        if len(focal) != 1:
            raise MsgError("focal company should be a list with only one element")
        
        focal_returns = self.df[(self.df['TICKER'].isin(focal)) & (self.df['year'].isin(years))].RET.to_numpy()
        
        if len(focal_returns) == 0:
            raise MsgError("focal company has an empty return series. check if TICKER is valid in that year")
        
        peer_returns = self.df[(self.df['TICKER'].isin(peers)) & (self.df['year'].isin(years))]
        avg_peer_returns = peer_returns.groupby(['year','month'])['RET'].apply(np.mean).to_numpy()
        
        if len(avg_peer_returns) == 0:
            raise MsgError("peer companies have an empty return series")
        
        #print('number of focal returns', len(focal_returns))
        #print('number of peer returns', len(avg_peer_returns))
        
        if len(focal_returns) != len(avg_peer_returns):
            raise MsgError("two return series have different size", '# focal returns', len(focal_returns), '# peer returns', len(avg_peer_returns) )
        
        '''Return R^2 where x and y are array-like.
        https://stackoverflow.com/questions/893657/how-do-i-calculate-r-squared-using-python-and-numpy
        '''
        
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(avg_peer_returns, focal_returns)
        return r_value**2

    