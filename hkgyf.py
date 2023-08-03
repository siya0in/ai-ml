import pandas as pd

data = pd.read_csv("another_dataframe.csv")
data['insect count'] = None

def extract_sum_from_prediction_string(prediction_str):
    sum_value = 0
    for char in prediction_str:
        if char.isdigit():
            sum_value += int(char)
    return sum_value

data['insect count'] = data['Predictions'].apply(lambda x: extract_sum_from_prediction_string(x) if x else 0)

# Convert the "Date" column to datetime type
data['Date'] = pd.to_datetime(data['Date'])

# Group the data by week (start of the week on Monday) and aggregate the "insect count" and count the number of images for each week
grouped_data = data.groupby(pd.Grouper(key='Date', freq='W-MON')).agg({
    'Predictions': 'count',
    'insect count': 'sum'
}).reset_index()

# Rename the columns to represent the output correctly
grouped_data.rename(columns={'Predictions': 'no. of images'}, inplace=True)

print(grouped_data)
