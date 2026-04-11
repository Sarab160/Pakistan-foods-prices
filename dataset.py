import pandas as pd

df=pd.read_csv("Pakistan_Food_Price.csv")

print(df.head())

df['prev_price'] = df['price'].shift(1)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

# Extract features
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# (Optional but useful)
df['day_of_week'] = df['date'].dt.dayofweek

# Drop original date column
df = df.drop('date', axis=1)

print(df.head())

df.to_csv("final_data.csv",index=False)