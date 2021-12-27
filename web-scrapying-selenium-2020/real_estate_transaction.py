from glob import glob
import os
import pandas as pd
import cn2an

files = glob('D:/new/*/*_lvr_land_*.csv')

# 季別
folder_path_list = []

new_col = 'df_name'

df_all = pd.DataFrame()

folder_path = 'D:/new'
folder_content = os.listdir(folder_path)
for f in folder_content:
    if ".zip" not in f:
        if ".log" not in f:
            folder_path_list.append(f)
            
            
            
for f in folder_path_list:
    files = glob('D:/new/'+f+'/*_lvr_land_*.csv')
    
    for file in files:
        try:
            df = pd.read_csv(file,encoding = "utf-8", header = 1, engine = "python", index_col=0)
            columns = df.columns.tolist()
            file_split = file.split('\\',2)[1].strip('.csv')
            df[new_col] = f[0:3] + "_"+ f[-1:] + "_" + file_split[:1] + "_" + file_split[-1:]
            df_all = pd.concat([df, df_all])
            print(file,"完成")
        except Exception as e:
            print(file,"有問題")
            
# 資料處理
df_all['total floor number'] = df_all['total floor number'].str.replace("層","")
df_all['total floor number'] = df_all['total floor number'].str.replace("地下",'-1')
#補0
df_all['total floor number'] = df_all['total floor number'].fillna(0)


# 阿拉伯數字轉換
def transform(v):
    if isinstance(v, int):
        return v
    else:
        try:
            v = cn2an.cn2an(v,"smart")
            return v
        except:
            return v

    return v

df_all['total floor number'] = df_all['total floor number'].map(transform)


# 篩選條件1 filter.csv
df_all_mask = (df_all['main use'] == '住家用') &(df_all['total floor number'].astype('int') >= 13) & (df_all['building state'].str.contains('住宅大樓'))
# df_all[df_all_mask].head(5)
result1 = df_all[df_all_mask]
result1
result1.to_csv('D:/new/'+'filter.csv', encoding = "utf-8")


# 篩選條件2 count.csv

# 總件數
total_count = df_all['land sector position building sector house number plate'].count()

# 總車位數 
cols = ['1','2']
df_all['transaction pen number'].str.split('車位').tolist()
total_berth =pd.DataFrame(df_all['transaction pen number'].str.split('車位').tolist(), columns= cols).iloc[:,-1].astype(int).sum()

# 平均總價元
total_price = df_all['total price NTD'].astype(int).sum()
avg_total_price = round(total_price / total_count, 3)

# 平均車位總價元
total_berth_price = df_all['the berth total price NTD'].astype(int).sum()
avg_berth_price = round(total_berth_price / total_berth, 3)

data ={
    '總件數' : total_count,
    '總車位數': total_berth,
    '平均總價元' :avg_berth_price,
    '平均車位總價元':avg_total_price,
}
frame = pd.DataFrame(data, index = [0])
frame.to_csv('D:/new/'+'count.csv', encoding = "utf-8")