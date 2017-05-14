import datetime
import pandas as pd
import random
from random import randint
import numpy as np

todays_date = datetime.datetime.now().date()

index = pd.date_range(todays_date-datetime.timedelta(10), periods=10, freq='D')

columns = ['sid','share', 'side','price','re','openvalue', 'openposition']
df= pd.DataFrame(index=index, columns=columns)
df['sid']=1
df['share']=randint(1,10)
df['side']=df['side'].apply(lambda v: random.choice(['B','S']))
df['price']=df['price'].apply(lambda v: randint(20,100))
df['openposition']=0
for i in range (0,len(df.index)):
    if i==0:
        df.loc[:,'re']=0
        if df['side'][0]=='B':
            df['openposition'][0]=df['share'][0]
            df['openvalue'][0]=df['share'][0]*df['price'][0]
        elif df['side'][0]=='S':
            df['openposition'][0]=-df['share'][0]
            df['openvalue'][0]=-df['share'][0]*df['price'][0]
    else:
        if df['side'][i]=='B':
            df['openposition'][i]=df['openposition'][i-1]+df['share'][i]
            df['openvalue'][i]=df['openvalue'][i-1]+df['share'][i]*df['price'][i]
            df['re'][i]=0
        elif df['side'][i]=='S':
            df['openposition'][i]=df['openposition'][i-1]-df['share'][i]
            df['openvalue'][i]=df['openvalue'][i-1]-df['share'][i]*df['price'][i]
            df['re'][i]=df['share'][i]*(df['price'][i-1]-df['price'][i])

class StrategPerformance(object):
    def __init__(self, df):
        self.df=df
        self.daily_return=df['re']
    def annualized_return(self):
        total_return=self.daily_return.sum()
        total_days = self.daily_return.index.size
        if total_return < -1:
            total_return = -1
        return ((1 + total_return)**(252 / total_days) - 1)

    def annualized_std(self):
        return np.sqrt(252) * np.std(self.daily_return)

    def annualized_downside_std(self):
        downside_return = self.daily_return.copy()
        downside_return[downside_return > 0] = 0
        return np.sqrt(252) * np.std(downside_return)

    def annual_vol(self):
        return self.annualized_std()

    def sharpe_ratio(self):
        stdev = self.annualized_std()
        if stdev == 0:
            return np.nan
        else:
            return self.annualized_return() / stdev

    def sortino_ratio(self):
        stdev = self.annualized_downside_std()
        if stdev == 0:
            return np.nan
        else:
            return self.annualized_return() / stdev

    def max_drawdown(self):
        return np.max(np.maximum.accumulate(self.daily_return) - self.daily_return)
sp=StrategPerformance(df)
print sp.annualized_return(), sp.annualized_std(), sp.annualized_downside_std(), sp.annual_vol(), sp.sharpe_ratio()
