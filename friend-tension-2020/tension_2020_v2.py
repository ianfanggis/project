import os
import pandas as pd



InputPath = str(input('寫上str9ex的資料夾路徑，例如D:/謝38/20200717'))
BasePath = str(input('寫上str9ex-tension的檔案路徑，例如D:/謝38/20200717/str9ex-tension.csv'))

InuputList = []

with os.scandir(InputPath) as entries:
    for entry in entries:
        if ".csv" in entry.name:
            if "Final" not in entry.name:
                if "tension" not in entry.name:
                    InuputList.append(entry.name)

for fname in InuputList:
    input_data = pd.read_csv(InputPath + "/" + fname, index_col='Date', encoding='utf-8')
    base_data = pd.read_csv(BasePath, index_col='Date', encoding='utf-8')

    input_data['Time'].astype('object')
    # input_data['Date'].astype('object')
    base_data['Time'].astype('object')
    # base_data['Date'].astype('object')

    res = pd.merge(input_data, base_data, on=['Date', 'Time'], how='left')
    res['Time'] = res['Time'].str.replace('U', '下午')
    res['Time'] = res['Time'].str.replace('W', '上午')
    res['Time'] = res['Time'].str.replace('?', '')

    fname1 = fname.rstrip(".csv")

    res.to_csv(InputPath + "/" + fname1 + "_final.csv", encoding='big5')