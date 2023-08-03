import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("result.csv")

# Convert the "TimeStamp" column to a pandas datetime data type
df["TimeStamp"] = pd.to_datetime(df["TimeStamp"], format='%Y-%m-%d %H-%M-%S')

# Extract the date from the "TimeStamp" column and create a new column "Date"
df["Date"] = df["TimeStamp"].dt.date
data = df[["Date", "Predictions"]].copy()
data['insect count'] = None

def extract_sum_from_prediction_string(prediction_str):
    sum_value = 0
    for char in prediction_str:
        if char.isdigit():
            sum_value += int(char)
    return sum_value


data['insect count'] = data['Predictions'].apply(lambda x: extract_sum_from_prediction_string(x) if x else 0)

# Group the data by "Date" and aggregate the "insect count" and count the number of images for each date
grouped_data = data.groupby('Date').agg({
    'Predictions': 'count',
    'insect count': 'sum'
}).reset_index()

data['insect count'] = data['insect count'].fillna(0).astype(int)  # Convert 'insect count' column to integers and fill NaN with 0
# Rename the columns to represent the output correctly
grouped_data.rename(columns={'Predictions': 'no. of images'}, inplace=True)

print(grouped_data)
data.to_csv("modified_dataframe.csv", index=False)

# Group by date and sum the 'insect count' for each group
#grouped_data= pd.DataFrame(data.groupby('Date')['insect count'].sum().reset_index())
#data.to_csv("modified_dataframe.csv", index=False)
#print(grouped_data)


