import requests
import pandas as pd
from datetime import datetime
import numpy as np


def JGB_rates_conv():
    JGB_rates = pd.read_csv('https://www.mof.go.jp/jgbs/reference/interest_rate/data/jgbcm_all.csv', encoding='Shift-JIS', header=1)

    def dateConv(date):

        wareki = {
            "R":2018,
            "H":1988,
            "S":1925
            }
  
        date_els = date.split('.', 2)
        year_num = int(date_els[0][1:])
        era = date_els[0][0]
 
        year = year_num + wareki[era]
        month =int(date_els[1])
        day = int(date_els[2])

        dt = datetime(year, month, day)
        return dt

    JGB_rates["基準日"] = JGB_rates['基準日'].apply(dateConv)
    JGB_rates = JGB_rates.set_index('基準日')
    JGB_rates.replace('-', np.nan, inplace=True)

    JGB_rate_5_30 = JGB_rates[['5年', '10年', '15年', '20年', '25年', '30年']].dropna()
    JGB_rate_5_30 = JGB_rate_5_30.astype(float, errors='raise')

    JGB_rate_5_30_12M_M = JGB_rate_5_30.resample('ME').mean().tail(12).mean()

    JGB_rate_5_30_12M_M.to_csv('JGB_rates.csv', sep='\t', encoding='utf-8', mode='w', header=False)

if __name__ == '__main__':
    JGB_rates_conv()
