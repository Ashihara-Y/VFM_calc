import requests
import pandas as pd
from datetime import datetime
import numpy as np
from scipy.interpolate import PchipInterpolator
from decimal import *

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

    JGB_rate_1_30 = JGB_rates[['1年', '2年', '3年', '4年', '5年', '10年', '15年', '20年', '25年', '30年']].dropna()
    JGB_rate_1_30 = JGB_rate_1_30.astype(float, errors='raise')

    JGB_rate_1_30_12M_M = JGB_rate_1_30.resample('ME').mean().tail(12).mean()

    val_array = JGB_rates_df.iloc[0:,0].to_numpy()
    col_series = JGB_rates_df.T.columns.to_series().apply(lambda x: x[:-1])
    col_array = col_series.values.astype(int)
    pchip_interp = PchipInterpolator(col_array, val_array)
    r1_fl_str = str(pchip_interp(proj_years))
    r1 = Decimal(r1_fl_str).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)

    JGB_rate_1_30_12M_M.to_csv('JGB_rates2.csv', sep='\t', encoding='utf-8', mode='w', header=False)

if __name__ == '__main__':
    JGB_rates_conv()
