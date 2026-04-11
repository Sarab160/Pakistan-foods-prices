import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

df=pd.read_csv("final_data.csv")

x=df[["prev_price","day","month","year"]]

y=df["price"] 

sns.pairplot(data=x)
# plt.show()
ohe=OneHotEncoder(sparse_output=False,drop="first")
fe=df[["admname","mktname"]]
fe_en=ohe.fit_transform(fe)
en_datafram=pd.DataFrame(data=fe_en,columns=ohe.get_feature_names_out(fe.columns))

x_f=pd.concat([x,en_datafram],axis=1)

oe=OrdinalEncoder()
fe=df[["cmname"]]
fe_e=oe.fit_transform(fe)
oe_dataframe=pd.DataFrame(data=fe_e,columns=fe.columns)

X=pd.concat([x_f,oe_dataframe],axis=1)

x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

lr=KNeighborsRegressor()
lr.fit(x_train,y_train)

print(lr.score(x_test,y_test))
print(lr.score(x_train,y_train))