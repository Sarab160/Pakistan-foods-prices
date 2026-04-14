from fastapi import FastAPI
import pickle
import numpy as np
import pandas as pd

#####3 http://127.0.0.1:8000/docs

app=FastAPI()


model=pickle.load(open("model.pkl","rb"))
ohe=pickle.load(open("ohe.pkl","rb"))
oe=pickle.load(open("oe.pkl","rb"))


@app.get("/")
def home():
    return {"message: Pakistan Food Price Intelligence API Reunning"}

#-====Prediction============

@app.post("/predict")
def predict(data:dict):
    
    try:
        admname=data["admname"]
        mktname=data["mktname"]
        cmname=data["cmname"]
        
        prev_price=float(data["prev_price"])
        day=int(data["day"])
        month=int(data["month"])
        year=int(data["year"])
        
        ## encoding    
        ohe_input=pd.DataFrame([[admname,mktname]],columns=["admname","mktname"])
        ohe_encoded=ohe.transform(ohe_input)
        
        cm_encoded=oe.transform([[cmname]])
        
        
        final_input=np.concatenate([
            [prev_price,day,month,year],
            ohe_encoded[0],
            cm_encoded[0],
            
        ]).reshape(1,-1)
        
        predicted_price=model.predict(final_input)[0]
        
        price_change = predicted_price - prev_price
        percent_change = (price_change / prev_price) * 100 if prev_price != 0 else 0

        # Recommendation logic
        if predicted_price < prev_price:
            recommendation = "BUY NOW"
            message = "📉 Price is expected to decrease. Good time to purchase."
        
        elif percent_change <= 5:
            recommendation = "BUY (MODERATE)"
            message = "📊 Slight price increase expected. You may buy if needed."
        
        else:
            recommendation = "NOT RECOMMENDED"
            message = "📈 Price is expected to increase significantly. Consider waiting."

        # Market insight
        if percent_change > 10:
            insight = "⚠️ High inflation trend detected."
        elif percent_change < -5:
            insight = "📉 Deflation trend detected — prices are dropping."
        else:
            insight = "📊 Stable market conditions."

        # ---------------- FINAL FORMATTED MESSAGE ----------------
        full_message = f"""
📊 Price Prediction Report

📍 Location: {mktname}, {admname}
🛒 Product: {cmname}

💰 Current Price: {prev_price} PKR
🔮 Predicted Price: {round(predicted_price,2)} PKR

📈 Change: {round(percent_change,2)}%

🧠 Recommendation: {recommendation}
{message}

📌 Market Insight:
{insight}
"""

        # ---------------- RESPONSE ----------------
        return {
            "location": {
                "admin": admname,
                "market": mktname
            },
            "product": cmname,
            "predicted_price": round(predicted_price, 2),
            "price_change": round(price_change, 2),
            "percent_change": round(percent_change, 2),
            "recommendation": recommendation,
            "message": message,
            "market_insight": insight,
            "report": full_message.strip()
        }

    except Exception as e:
        return {"error": str(e)}
    