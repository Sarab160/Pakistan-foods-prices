import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ---------------- LOAD FILES ----------------
model = pickle.load(open("model.pkl", "rb"))
ohe = pickle.load(open("ohe.pkl", "rb"))
oe = pickle.load(open("oe.pkl", "rb"))

df = pd.read_csv("final_data.csv")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Pakistan Food Intelligence", layout="centered")

st.title("🥦 Pakistan Food Price Intelligence System")
st.markdown("### Predict price + smart buying recommendation with location insights")

# ---------------- INPUTS ----------------
admname = st.selectbox("📍 Admin Area", df["admname"].unique())
mktname = st.selectbox("🏪 Market Name", df["mktname"].unique())
cmname = st.selectbox("🛒 Commodity", df["cmname"].unique())

prev_price = st.number_input("💰 Previous Price", min_value=0.0)
day = st.number_input("📅 Day", min_value=1, max_value=31)
month = st.number_input("📅 Month", min_value=1, max_value=12)
year = st.number_input("📅 Year", min_value=2000, max_value=2100)

# ---------------- PREDICTION ----------------
if st.button("🚀 Predict Price"):

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

    # ---------------- CALCULATIONS ----------------
    price_change = predicted_price - prev_price
    percent_change = (price_change / prev_price) * 100 if prev_price != 0 else 0

    # ---------------- OUTPUT HEADER ----------------
    st.success("✅ Prediction Completed Successfully")

    st.markdown("## 📊 Result Summary")

    st.write(f"📍 **Location:** {admname} → {mktname}")
    st.write(f"🛒 **Commodity:** {cmname}")
    st.write(f"💰 **Previous Price:** {prev_price}")
    st.write(f"🔮 **Predicted Price:** {predicted_price:.2f}")
    st.write(f"📊 **Change:** {percent_change:.2f}%")

    # ---------------- SMART MESSAGE ----------------
    st.markdown("## 🧠 Smart Recommendation System")

    if predicted_price < prev_price:
        st.success("🟢 BUY NOW")
        st.write(
            f"📉 At **{mktname}, {admname}**, price is expected to decrease. "
            f"This is a good opportunity to buy **{cmname}**."
        )

    elif percent_change <= 5:
        st.info("🟡 BUY (MODERATE)")
        st.write(
            f"📊 At **{mktname}, {admname}**, slight increase expected for **{cmname}**. "
            "You may buy if needed."
        )

    else:
        st.error("🔴 NOT RECOMMENDED TO BUY")
        st.write(
            f"📈 At **{mktname}, {admname}**, price of **{cmname}** may increase significantly. "
            "It is better to wait."
        )

    # ---------------- MARKET INSIGHT ----------------
    st.markdown("## 📌 Market Insight")

    if percent_change > 10:
        st.warning(f"⚠️ High inflation trend detected in {mktname}, {admname}.")
    elif percent_change < -5:
        st.success(f"📉 Deflation trend detected in {mktname}, {admname}.")
    else:
        st.info(f"📊 Stable market conditions in {mktname}, {admname}.")