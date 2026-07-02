# 📱 Mobile Price Range Prediction

A complete, end-to-end machine learning project: a trained classifier that predicts a
mobile phone's **price range (Low / Medium / High / Very High)** from its hardware specs,
served through a **FastAPI** backend and a **React (Vite)** frontend, plus a fully
documented Jupyter notebook covering the whole data science workflow.

```
mobile-price-prediction/
├── data/
│   ├── generate_dataset.py     # builds train.csv
│   └── train.csv                # 2,000 phones x 20 specs + price_range
├── notebook/
│   └── Mobile_Price_Range_Prediction_Professional.ipynb
├── model/
│   ├── train_model.py           # trains & compares 6-7 models, saves the best one
│   ├── model.pkl                 # trained classifier (best model)
│   ├── scaler.pkl                 # fitted StandardScaler
│   ├── feature_names.json
│   ├── metrics.json               # comparison results + class label mapping
│   ├── confusion_matrix.png
│   └── feature_importance.png
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app (/predict, /model-info, /health)
│   │   ├── schemas.py             # request/response models
│   │   └── model/                 # copy of trained artifacts used by the API
│   └── requirements.txt
├── frontend/                      # React + Vite single-page app
│   ├── src/
│   ├── package.json
│   └── ...
├── requirements.txt               # for dataset generation / training / notebook
└── README.md
```

---

## 1. Business Problem

Bob is launching a mobile phone brand and needs a data-driven way to position new devices
by price tier (`0` = Low Cost, `1` = Medium Cost, `2` = High Cost, `3` = Very High Cost)
based on hardware specs such as RAM, battery, camera, display, and connectivity. This
project builds, evaluates, and deploys a classifier that does exactly that.

## 2. About the dataset

This repo cannot download files from Kaggle directly, so `data/generate_dataset.py`
produces a **2,000-row synthetic dataset that mirrors the structure, value ranges, and
feature/target relationships of the well-known Kaggle "Mobile Price Classification"
dataset** (20 hardware specs → `price_range`). RAM is by far the dominant driver of
price range, followed by battery power and screen resolution — matching the real dataset's
known correlations.

> If you have the real Kaggle `train.csv` (from
> [iabhishekofficial/mobile-price-classification](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification)),
> just drop it into `data/train.csv` (same 21 columns) and re-run
> `model/train_model.py` — everything downstream works unchanged.

---

## 3. Quick start

### 3.1 Generate the dataset

```bash
cd data
python generate_dataset.py
# -> writes data/train.csv
```

### 3.2 Train the model

```bash
pip install -r requirements.txt
cd model
python train_model.py
```

This trains Logistic Regression, KNN, Decision Tree, Random Forest, Gradient Boosting, SVM
(and XGBoost if installed), evaluates each with accuracy / precision / recall / F1 /
5-fold CV accuracy, and saves the **best model** (by CV accuracy) plus the scaler and
metadata into `model/`. Copy the four artifact files into `backend/app/model/` if you
retrain (the repo already ships with pre-trained copies):

```bash
cp model/model.pkl model/scaler.pkl model/feature_names.json model/metrics.json backend/app/model/
```

### 3.3 Run the backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- Swagger UI: https://mobile-price-api.onrender.com/docs
- Health check: https://mobile-price-api.onrender.com/health
- Model info: https://mobile-price-api.onrender.com/model-info

### 3.4 Run the frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173 — adjust the 20 spec sliders/toggles and click **Run
Prediction**. The app calls the FastAPI backend at `https://mobile-price-api.onrender.com` by default.
To point at a different backend URL, create `frontend/.env`:

```
VITE_API_BASE_URL=https://mobile-price-api.onrender.com
```

### 3.5 Explore the notebook

```bash
jupyter notebook notebook/Mobile_Price_Range_Prediction_Professional.ipynb
```

Covers: business problem, data quality checks, EDA (with business interpretation for every
chart), preprocessing, model building (7 algorithms explained), evaluation, feature
importance, model comparison, business recommendations, challenges, and conclusion — and
ends by re-saving `model.pkl` / `scaler.pkl` so you can retrain directly from the notebook.

---

## 4. Model comparison (current trained artifacts)

| Model | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) | CV Accuracy (5-fold) |
|---|---|---|---|---|---|
| **Logistic Regression** ⭐ | 0.8275 | 0.8289 | 0.8275 | 0.8273 | **0.7919** |
| Gradient Boosting | 0.8125 | 0.8145 | 0.8125 | 0.8120 | 0.7775 |
| Random Forest | 0.8125 | 0.8120 | 0.8125 | 0.8110 | 0.7744 |
| Decision Tree | 0.7400 | 0.7402 | 0.7400 | 0.7388 | 0.7412 |
| SVM (RBF) | 0.7550 | 0.7512 | 0.7550 | 0.7515 | 0.7031 |
| KNN | 0.4975 | 0.5132 | 0.4975 | 0.5013 | 0.4756 |

⭐ = model currently saved in `model/model.pkl` and served by the backend. Re-run
`train_model.py` after installing `xgboost` to include it in the comparison.

**Top features driving price range**: `ram` ≫ `battery_power` > `px_width` ≈
`px_height` > `int_memory`. Connectivity flags (Bluetooth, WiFi, dual SIM, 3G/4G) and
camera megapixels contribute comparatively little.

---

## 5. API reference

### `POST /predict`

Request body — all 20 specs (see `backend/app/schemas.py` for valid ranges):

```json
{
  "battery_power": 1500, "blue": 1, "clock_speed": 2.2, "dual_sim": 1, "fc": 5,
  "four_g": 1, "int_memory": 32, "m_dep": 0.5, "mobile_wt": 150, "n_cores": 4,
  "pc": 10, "px_height": 800, "px_width": 1200, "ram": 2048, "sc_h": 13, "sc_w": 7,
  "talk_time": 10, "three_g": 1, "touch_screen": 1, "wifi": 1
}
```

Response:

```json
{
  "price_range": 1,
  "label": "Medium Cost",
  "confidence": 0.5024,
  "probabilities": {
    "Low Cost": 0.0072,
    "Medium Cost": 0.5024,
    "High Cost": 0.4872,
    "Very High Cost": 0.0032
  }
}
```

### `GET /model-info`

Returns the best model name, the full comparison table, and the class label mapping
(from `model/metrics.json`).

### `GET /health`

Simple liveness check.

---

## 6. Business recommendations (summary)

1. **Pricing**: Use the model to assign a price tier to new device designs before
   manufacturing.
2. **R&D focus**: RAM, battery, and screen resolution have the largest impact on price
   tier — prioritize these when designing for a higher tier.
3. **Marketing**: Lead with RAM/battery/display specs for premium tiers; connectivity
   features are now baseline expectations across all tiers.
4. **Inventory**: Segment catalog and stock levels by predicted price tier.
5. **Competitive benchmarking**: Run competitor specs through the model to see how their
   pricing compares to their hardware.

See the notebook's Section 12 for the full discussion, and Section 13 for challenges
(data quality, feature correlation, model selection, overfitting, class balance) and
Section 14 for the production recommendation and retraining/monitoring guidance.

---

## 7. Tech stack

- **Modeling**: scikit-learn (Logistic Regression, KNN, Decision Tree, Random Forest,
  Gradient Boosting, SVM; XGBoost optional), pandas, numpy, matplotlib, seaborn, joblib
- **Backend**: FastAPI, Pydantic, Uvicorn
- **Frontend**: React 18, Vite, plain CSS (no UI framework dependency)

## 8. License

MIT — feel free to use this as a portfolio project or starting point for your own.
