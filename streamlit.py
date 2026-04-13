import streamlit as st
import pandas as pd
import numpy as np
import pickle

# LOAD FILES
model = pickle.load(open("model.pkl", "rb"))
ohe = pickle.load(open("ohe.pkl", "rb"))
oe = pickle.load(open("oe.pkl", "rb"))

df = pd.read_csv("final_data.csv")

st.title("🥦 Pakistan Food Price Intelligence System")

st.markdown("### Predict price + get smart buying recommendation")

# ---------------- INPUTS ----------------
admname = st.selectbox("Admin Name", df["admname"].unique())
mktname = st.selectbox("Market Name", df["mktname"].unique())
cmname = st.selectbox("Commodity Name", df["cmname"].unique())

prev_price = st.number_input("Previous Price", min_value=0.0)
day = st.number_input("Day", min_value=1, max_value=31)
month = st.number_input("Month", min_value=1, max_value=12)
year = st.number_input("Year", min_value=2000, max_value=2100)

# ---------------- PREDICTION ----------------
if st.button("Predict Price"):

    # Encoding
    ohe_input = pd.DataFrame([[admname, mktname]], columns=["admname", "mktname"])
    ohe_encoded = ohe.transform(ohe_input)

    cm_encoded = oe.transform([[cmname]])

    final_input = np.concatenate([
        [prev_price, day, month, year],
        ohe_encoded[0],
        cm_encoded[0]
    ]).reshape(1, -1)

    predicted_price = model.predict(final_input)[0]

    st.success(f"📊 Predicted Price: {predicted_price:.2f}")

    # ---------------- BUY / NOT BUY LOGIC ----------------
    price_change = predicted_price - prev_price
    percent_change = (price_change / prev_price) * 100 if prev_price != 0 else 0

    st.markdown("### 🧠 Smart Recommendation")

    if predicted_price < prev_price:
        st.success("🟢 BUY NOW")
        st.write("📉 Price is expected to decrease. Good time to purchase this commodity.")

    elif percent_change <= 5:
        st.info("🟡 BUY (MODERATE)")
        st.write("📊 Slight price increase expected. You may buy if needed.")

    else:
        st.error("🔴 NOT RECOMMENDED TO BUY")
        st.write("📈 Price is expected to increase significantly. Consider waiting.")

    # ---------------- EXTRA INSIGHT ----------------
    st.markdown("### 📌 Market Insight")

    if percent_change > 10:
        st.warning("⚠️ High inflation trend detected for this item.")
    elif percent_change < -5:
        st.success("📉 Deflation trend detected — prices are dropping.")
    else:
        st.info("📊 Stable market conditions for this commodity.")