This repo contains a monthly stock return data (Year 1995 - Year 2021) and a python class ```PeerFirm``` for measuring peer firms R2.

The peer firms regression test is proposed in Bhojraj et al. 2003. 

Bhojraj, Sanjeev, Charles MC Lee, and Derek K. Oler. "What's my line? A comparison of industry classification schemes for capital market research." Journal of Accounting Research 41.5 (2003): 745-774.

```python
### load in monthly return data
PeerFirm = PeerFirm('monthly_return.csv') 

focal = ['AAPL']
peers = ['MSFT', 'TSLA']  # Different ways for identifying the peers
years = [2016, 2017]  

### how much the focal firm's monthly returns can be explained by the peers monthly returns
PeerFirm.rsquared(focal, peers, years) 
### 0.3288147452874622

```
