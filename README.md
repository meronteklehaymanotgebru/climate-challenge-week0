# 🌍 African Climate Trend Analysis for COP32

## 10 Academy - Artificial Intelligence Mastery | Week 0 Challenge

### 📊 Project Overview
This repository contains exploratory climate data analysis for five African nations (Ethiopia, Kenya, Sudan, Tanzania, and Nigeria) using NASA POWER satellite-derived measurements from 2015-2026. The analysis supports EthioClimate Analytics in preparing evidence-backed insights for Ethiopia's hosting of COP32 in Addis Ababa (2027).

### 🎯 Business Objective
Position Ethiopia as a credible, data-informed host for COP32 by surfacing key climate trends, seasonal patterns, and anomalies that amplify Africa's voice in global climate negotiations.

### 📈 Key Findings
- Comprehensive climate vulnerability ranking across 5 African nations
- Temperature anomaly analysis against 1991-2020 baseline
- Extreme event frequency assessment (heatwaves, droughts, floods)
- Cross-country precipitation variability comparison
- Actionable policy recommendations for COP32 negotiations

### 🛠️ Technical Stack
- **Language:** Python 3.10+
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Dashboard:** Streamlit
- **CI/CD:** GitHub Actions
- **Version Control:** Git with Conventional Commits

### 📁 Repository Structure
```
climate-challenge-week0/
├── .github/workflows/
│ └── ci.yml # CI pipeline configuration
├── notebooks/
│ ├── ethiopia_eda.ipynb # Ethiopia EDA
│ ├── kenya_eda.ipynb # Kenya EDA
│ ├── sudan_eda.ipynb # Sudan EDA
│ ├── tanzania_eda.ipynb # Tanzania EDA
│ ├── nigeria_eda.ipynb # Nigeria EDA
│ └── compare_countries.ipynb # Cross-country comparison
├── app/
│ ├── main.py # Streamlit dashboard
│ └── utils.py # Helper functions
├── scripts/
│ └── data_loader.py # Data loading utilities
├── tests/
│ └── test_data_quality.py # Unit tests
├── requirements.txt
├── .gitignore
└── README.md
```

### 🚀 Quick Start

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/climate-challenge-week0.git
cd climate-challenge-week0

### 2. Set Up Virtual Environment
```
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Run Jupyter Notebooks
```
jupyter notebook
```

### 5. Launch Streamlit Dashboard
```
streamlit run app/main.py
```






