import streamlit as st
import pandas as pd
import numpy as np
import pickle

# LOAD MODEL + ENCODERS
model = pickle.load(open("model.pkl", "rb"))
ohe = pickle.load(open("ohe.pkl", "rb"))
oe = pickle.load(open("oe.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# LOAD ORIGINAL DATA (for dropdown options)
df = pd.read_csv("final_data.csv")

st.title("🥦 Pakistan Food Price Prediction App")

# -------------------------
# DROPDOWNS (Categorical)
# -------------------------
admname = st.selectbox("Admin Name", df["admname"].unique())
mktname = st.selectbox("Market Name", df["mktname"].unique())
cmname = st.selectbox("Commodity Name", df["cmname"].unique())

# -------------------------
# NUMERIC INPUTS
# -------------------------
prev_price = st.number_input("Previous Price", min_value=0.0)
day = st.number_input("Day", min_value=1, max_value=31)
month = st.number_input("Month", min_value=1, max_value=12)
year = st.number_input("Year", min_value=2000, max_value=2100)

# -------------------------
# PREDICTION BUTTON
# -------------------------
if st.button("Predict Price"):

    # OneHotEncoding (admname + mktname)
    ohe_input = pd.DataFrame([[admname, mktname]], columns=["admname", "mktname"])
    ohe_encoded = ohe.transform(ohe_input)

    # OrdinalEncoding (cmname)
    cm_encoded = oe.transform([[cmname]])

    # Final input construction
    final_input = np.concatenate([
        [prev_price, day, month, year],
        ohe_encoded[0],
        cm_encoded[0]
    ]).reshape(1, -1)

    # Prediction
    prediction = model.predict(final_input)

    st.success(f"Predicted Price: {prediction[0]:.2f}")