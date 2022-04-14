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
        
    
    def rsquared_month_based(self, firm_peers, year, month):
        '''
        for this regression, each observation is firm. The # of regression observation is the # firms.
        firms: a dictionary
        calculate the r2 of cross-sectional regression of firm and peer returns in month and year
        firm_peers: a dictionary. key: ticker, value: a list of peer tickers
        '''
        month_ret = self.df[(self.df['year']==year) & (self.df['month']==month)] # querying based on monthly data is more efficient
        
        Ys, Xs = [], [] # Ys is a list of focal returns, Xs is a list of peer's average returns.
        for firm, peers in firm_peers.items():
            try:
                focal_ret = month_ret[month_ret['TICKER']==firm].RET.iloc[0]
                peer_ret = month_ret[month_ret['TICKER'].isin(peers)].RET.to_list()
            except:
                focal_ret = np.nan
                peer_ret = np.nan

            Xs.append(np.nanmean(peer_ret))
            Ys.append(focal_ret)
            
        tempdf = pd.DataFrame({'y':Ys, 'x':Xs}).dropna(subset=['y','x'])
        
        '''Return R^2 where x and y are array-like.
        https://stackoverflow.com/questions/893657/how-do-i-calculate-r-squared-using-python-and-numpy
        '''
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(tempdf.x, tempdf.y)
        
        return r_value**2
        
