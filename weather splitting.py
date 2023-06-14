import pandas as pd

#reading the dataset
df = pd.read_csv("WeatherData315.csv")
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], format='%Y-%m-%d %H:%M:%S')

# Group the dataframe by date
grouped = df.groupby(df['TimeStamp'].dt.date)

# Iterate over the groups and save each group to a separate CSV file
for date, group in grouped:
    filename = f"WeatherData_{date}.csv"  # Generate a unique filename for each date
    group.to_csv(filename, index=False)