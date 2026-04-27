import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,LabelEncoder
from sklearn.metrics import mean_absolute_error,mean_squared_error,root_mean_squared_error
import pickle
from sklearn.ensemble import RandomForestRegressor

## https://docs.google.com/forms/d/e/1FAIpQLScuPN0MqL6rTbyhb-l7dhqp70T3KZvgFrPU42IAY4teNqLkzg/viewform?usp=publish-editor

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

# scaler=StandardScaler()
# x_train_s=scaler.fit_transform(x_train)
# x_test_s=scaler.transform(x_test)


lr = RandomForestRegressor(
    n_estimators=150,
    max_depth=10,
    min_samples_split=5,
    random_state=42
)


lr.fit(x_train,y_train)

print("Test score",lr.score(x_test,y_test))
print("Train Score",lr.score(x_train,y_train))

test=lr.predict(x_test)

print("Mean absolute errror ",mean_absolute_error(y_test,test))
print("Mean Squared Error: ",mean_squared_error(y_test,test))
print("Root mean squared error",root_mean_squared_error(y_test,test))



pickle.dump(ohe, open("ohe.pkl", "wb"))
pickle.dump(oe, open("oe.pkl", "wb"))
pickle.dump(X.columns, open("columns.pkl", "wb"))
pickle.dump(lr, open("model.pkl", "wb"))
