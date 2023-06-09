import pandas as pd
import numpy as np
from datetime import datetime, timedelta


df = pd.read_csv("InsectCount (3).csv")
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], format='%Y-%m-%d %H-%M-%S')


df['date'] = df['TimeStamp'].dt.date
df['time'] = pd.to_datetime(df['TimeStamp']).dt.time

start_time = df['time'].iloc[0]
end_time = df['time'].iloc[-1]

length = []
count = 0
start_time = None

for index, row in df.iterrows():
    if start_time is None:
        start_time = row['time']
        count = 1
    elif row['time'].minute // 10 != start_time.minute // 10:
        length.append(count)
        start_time = row['time']
        count = 1
    else:
        count += 1

# Append the count of the last interval
length.append(count)


df['mean_']=np.nan

chunks = np.array_split(df['Mean'], len(df) / 10)
mean_list = [chunk.mean() for chunk in chunks]


mean_list = []

start_index = 0
for chunk_length in length:
    end_index = start_index + chunk_length
    chunk_mean = df['Mean'][start_index:end_index].mean()
    mean_list.append(chunk_mean)
    start_index = end_index
pos = 0

start_index = 0
for chunk_length, mean_value in zip(length, mean_list):
    end_index = start_index + chunk_length
    df.loc[start_index:end_index, 'mean_'] = mean_value
    start_index = end_index
    
filtered_data = df.drop_duplicates(subset=['mean_'])
filtered_data = filtered_data.drop(['Mean'], axis=1)
filtered_data = filtered_data.drop(['TimeStamp'],axis=1)
filtered_data['time'] = df['time'].apply(lambda x: x.replace(second=0))
filtered_data['time'] = df['time'].apply(lambda x: x.replace(minute=(x.minute//10)*10, second=0))

filtered_data.to_csv("out.csv", index=False)
print(filtered_data)




