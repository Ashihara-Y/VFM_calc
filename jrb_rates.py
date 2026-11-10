import sys
sys.dont_write_bytecode = True
import requests
import pymupdf
import pandas as pd
import numpy as np

def main():
    url = 'https://www.jfm.go.jp/financing/rate/k87jfb00000002wt-att/beppyo-1-1.pdf'
    res = requests.get(url)
    res.raise_for_status()

    with open('./JRB.pdf', "wb") as myfile:
        myfile.write(res.content)

    doc = pymupdf.open('./JRB.pdf', filetype="pdf")
    page = doc[0]
    tabs = page.find_tables()
    tab = tabs[0]
    df = tab.to_pandas()

    df['うち据置期間\n償還期限'] = [
        "5","6","7","8","9","10","11","12","13","14","15","16","17",
        "18","19","20","21","22","23","24","25","26","27","28","29","30"
    ]
    df['うち据置期間\n償還期限'] = df['うち据置期間\n償還期限'].astype(int)
    df = df.set_index('うち据置期間\n償還期限')

    target_cols = [
        'なし', '１年以内', '１年を超え\n２年以内',
        '２年を超え\n３年以内', '３年を超え\n４年以内', '４年を超え\n５年以内'
    ]
    df = df[target_cols]

    # 1. 文字列化・パーセント記号（半角）の除去
    df = df.map(lambda x: str(x).replace("%", ""))

    # 2. 列ごとに pd.to_numeric(..., errors='coerce') を適用して float64 に変換
    #    ※ "-" や "－"、空文字などは自動的に np.nan (NaN) になり、確実に float64 型になります
    df = df.apply(pd.to_numeric, errors='coerce').astype(np.float64)

    # 3. inplace=True を使わず代入形式でカラム名をリネーム
    df = df.rename(columns={
        'なし': '0',
        '１年以内': '1',
        '１年を超え\n２年以内': '2',
        '２年を超え\n３年以内': '3',
        '３年を超え\n４年以内': '4',
        '４年を超え\n５年以内': '5'
    })

    df.to_csv('JRB_rates.csv', sep='\t', encoding='utf-8', mode='w', header=False)
    df.to_csv('JRB_rates2.csv', sep=',', encoding='utf-8', mode='w', header=True, index=True)

if __name__ == '__main__':
    main()
