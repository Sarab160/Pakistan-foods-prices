import pandas as pd

df=pd.read_csv("Pakistan_Food_Price.csv")

print(df.head())

df['prev_price'] = df['price'].shift(1)

df.to_csv("price.csv",index=False)