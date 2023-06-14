import pandas as pd
import numpy as np

#reading the dataset
df = pd.read_csv("WeatherData_2023-04-21.csv")
df1=pd.read_csv('output21.4 (1).csv')
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], format='%Y-%m-%d %H:%M:%S')

#rounding off the the time
times = pd.to_datetime(df['time'])
rounded_times = times - pd.to_timedelta(times.dt.second, unit='s')
rounded_times = rounded_times - pd.to_timedelta(rounded_times.dt.minute % 10, unit='m')
rounded_times = rounded_times.dt.strftime('%H:%M:%S')
df['time']=rounded_times

times = pd.to_datetime(df['time'])
times = pd.to_datetime(df['time'], format='%H:%M:%S')

#storing the length for the same tens digit of minute wrt hour
length = []
count = 0
start_time = None

for index, row in df.iterrows():
    if start_time is None:
        start_time = row['TimeStamp'].time()
        count = 1
    elif row['TimeStamp'].time().minute // 10 != start_time.minute // 10:
        length.append(count)
        start_time = row['TimeStamp'].time()
        count = 1
    else:
        count += 1

# Append the count of the last interval
length.append(count)

#creating empty columns for the Light, humidity, temperature mean
df['light_mean']=np.nan
df['humidity_mean']=np.nan
df['temp_mean']=np.nan

df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')
#finding the mean avg for the the Light_intensity columns
chunks = np.array_split(df['Light_intensity(Lux)'], len(df) / 10)
mean_list = [chunk.mean() for chunk in chunks]


mean_list = []

start_index = 0
for chunk_length in length:
    end_index = start_index + chunk_length
    chunk_mean = df['Light_intensity(Lux)'][start_index:end_index].mean()
    mean_list.append(chunk_mean)
    start_index = end_index

#adding the mean avg value to the df[mean] column
start_index = 0
for chunk_length, mean_value in zip(length, mean_list):
    end_index = start_index + chunk_length
    df.loc[start_index:end_index, 'light_mean'] = mean_value
    start_index = end_index
    


#for humidity finding the mean average
chunks = np.array_split(df['Relative_Humidity(%)'], len(df) / 10)
mean_list = [chunk.mean() for chunk in chunks]


mean_list = []

start_index = 0
for chunk_length in length:
    end_index = start_index + chunk_length
    chunk_mean = df['Relative_Humidity(%)'][start_index:end_index].mean()
    mean_list.append(chunk_mean)
    start_index = end_index

#adding the mean avg value to the df[mean] column
start_index = 0
for chunk_length, mean_value in zip(length, mean_list):
    end_index = start_index + chunk_length
    df.loc[start_index:end_index, 'humidity_mean'] = mean_value
    start_index = end_index
    
#for temperature finding the mean average
chunks = np.array_split(df['Temperature(C)'], len(df) / 10)
mean_list = [chunk.mean() for chunk in chunks]


mean_list = []

start_index = 0
for chunk_length in length:
    end_index = start_index + chunk_length
    chunk_mean = df['Temperature(C)'][start_index:end_index].mean()
    mean_list.append(chunk_mean)
    start_index = end_index

#adding the mean avg value to the df[mean] column
start_index = 0
for chunk_length, mean_value in zip(length, mean_list):
    end_index = start_index + chunk_length
    df.loc[start_index:end_index, 'temp_mean'] = mean_value
    start_index = end_index

df = df.drop_duplicates(subset=['time'])
df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
filtered_data=df
filtered_data = filtered_data.drop(['Light_intensity(Lux)'], axis=1)
filtered_data = filtered_data.drop(['TimeStamp'], axis=1)
filtered_data = filtered_data.drop(['Temperature(C)'], axis=1)
filtered_data = filtered_data.drop(['Relative_Humidity(%)'], axis=1)

filtered_data_filtered = filtered_data[filtered_data['time'].isin(df1['time'])]

#merging the mean/10 minute column
# Convert 'date' column in filtered_data_filtered to datetime
filtered_data_filtered['date'] = pd.to_datetime(filtered_data_filtered['date'])

# Convert 'time' column in filtered_data_filtered to datetime
filtered_data_filtered['time'] = pd.to_datetime(filtered_data_filtered['time']).dt.time

# Convert 'date' column in df1 to datetime
df1['date'] = pd.to_datetime(df1['date'])

# Convert 'time' column in df1 to datetime
df1['time'] = pd.to_datetime(df1['time']).dt.time

# Merge the DataFrames on 'date' and 'time' columns
merged_data = filtered_data_filtered.merge(df1[['date', 'time', 'Mean /10 min']], on=['date', 'time'], how='left')

# Display the merged DataFrame


merged_data.to_csv("final_21.4.csv", index=False)
print(merged_data)