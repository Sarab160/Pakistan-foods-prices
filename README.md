cat << 'EOF' > README.md
# 📊 Price Prediction System (Machine Learning + Streamlit + Scraping Agent)

This project is a complete **end-to-end Machine Learning system** that predicts product prices based on multiple features such as previous price, date information, and categorical market data.  
It also includes a **Streamlit web app workflow** and a **scraping agent pipeline** for real-time or automated data collection.

---

## 🚀 Project Features

- 📈 Price prediction using **Random Forest Regressor**
- 🧹 Data preprocessing with encoding techniques:
  - OneHotEncoding (for `admname`, `mktname`)
  - OrdinalEncoding (for `cmname`)
- 📊 Data visualization using Seaborn
- 🤖 Trained ML model with evaluation metrics:
  - MAE (Mean Absolute Error)
  - MSE (Mean Squared Error)
  - RMSE (Root Mean Squared Error)
- 💾 Model persistence using **pickle**
- 🌐 Streamlit-based interactive web application
- 🕸️ Scraping Agent for automated data collection (used to update dataset)

---

## 🧠 Machine Learning Pipeline

### 1. Data Loading
df = pd.read_csv("final_data.csv")

### 2. Feature Selection
- Input Features:
  - prev_price
  - day
  - month
  - year
  - admname (encoded)
  - mktname (encoded)
  - cmname (ordinal encoded)

- Target:
  - price

---

### 3. Encoding
- OneHotEncoder → categorical location/market features  
- OrdinalEncoder → commodity names  

---

### 4. Model Training
RandomForestRegressor(
    n_estimators=150,
    max_depth=10,
    min_samples_split=5,
    random_state=42
)

---

### 5. Evaluation
- Train vs Test Score
- MAE
- MSE
- RMSE

---

### 6. Model Saving
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(ohe, open("ohe.pkl", "wb"))
pickle.dump(oe, open("oe.pkl", "wb"))
pickle.dump(X.columns, open("columns.pkl", "wb"))

---

## 🌐 Streamlit Workflow

Run the web app:

streamlit run app.py

Features:
- User input interface
- Live price prediction
- Clean UI dashboard

---

## 🕸️ Scraping Agent Workflow

- Collects real-time market data
- Updates dataset automatically
- Improves model accuracy
- Feeds `final_data.csv`

---

## 📁 Project Structure

├── final_data.csv
├── model.pkl
├── ohe.pkl
├── oe.pkl
├── columns.pkl
├── train_model.py
├── app.py
├── scraper.py
└── README.md

---

## 📊 Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- Seaborn, Matplotlib
- Streamlit
- Web Scraping (BeautifulSoup / Requests)
- Pickle

---

## 🎯 Future Improvements

- Deep Learning model integration
- Cloud deployment (AWS / Render / HuggingFace)
- Real-time API system
- Advanced analytics dashboard

---

## 👨‍💻 Author

Sarab Rafique

---

## ⭐ Support

If you like this project, give it a star on GitHub ⭐
EOF
