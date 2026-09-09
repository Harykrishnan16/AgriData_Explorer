# 🌾 AgriData Explorer – Understanding Indian Agriculture with EDA

An interactive **Streamlit dashboard** for exploring and analyzing Indian agricultural data using the **ICRISAT District-Level Dataset**.

This project transforms traditional Power BI-style agricultural analysis into an interactive **Python-based dashboard** using Streamlit, Pandas, NumPy, and Plotly.

---

## 📌 Project Overview

**AgriData Explorer** provides an interactive platform to understand agricultural production, cultivated area, and crop yield across Indian states and districts over multiple years.

The dashboard includes:

* Data cleaning and preprocessing
* Exploratory Data Analysis (EDA)
* Interactive visualizations
* SQL-style analytical questions implemented using Pandas
* Historical crop production analysis
* State and district-level comparisons
* Area vs. production correlation analysis
* A rule-based crop recommendation helper

The application uses the **ICRISAT District-Level Data** covering the period **1966–2017**.

---

## 🚀 Features

### 🏠 1. Overview

The Overview section provides a high-level summary of the dataset, including:

* Number of districts
* Number of states
* Years covered
* Number of records
* India-wide Rice vs Wheat production trends

---

### 🧹 2. Data Cleaning Summary

The dashboard documents and displays the major preprocessing steps applied to the dataset.

#### Cleaning steps:

1. Load the ICRISAT Excel dataset.
2. Identify negative values used as missing/not-recorded indicators.
3. Replace `-1` values with `NaN`.
4. Remove unnecessary whitespace from state and district names.
5. Convert the `Year` column to integer format.
6. Preserve the original ICRISAT units.

#### Dataset Units

| Measure    | Unit      |
| ---------- | --------- |
| Area       | 1000 ha   |
| Production | 1000 tons |
| Yield      | Kg/ha     |

The dashboard also displays missing-value statistics and a preview of the cleaned dataset.

---

## 📊 3. Exploratory Data Analysis

The EDA Explorer contains multiple interactive analyses covering crop production, yield, cultivated area, and historical trends.

### Analyses Included

* Top 7 Rice Production States
* Top 5 Wheat Producing States
* Wheat production share by state
* Oilseed production by top states
* Top 7 Sunflower Production States
* India's Sugarcane Production Trend
* Rice vs Wheat Production Trend
* Rice Production by West Bengal Districts
* Top 10 Wheat Production Years in Uttar Pradesh
* Pearl + Finger Millet Production Trend
* Kharif vs Rabi Sorghum Production
* Top Groundnut Producing States
* Soybean Production and Yield Efficiency
* Major Oilseed Producing States
* Impact of Cultivated Area on Production
* Rice vs Wheat Yield Across States

---

## 🧠 4. SQL-Style Analytical Questions

The project includes **10 analytical questions** that demonstrate SQL-style data analysis using Pandas.

### Q1. Year-wise Trend of Rice Production Across States

Identifies the top three rice-producing states and visualizes their production trends over time.

### Q2. Top 5 Districts by Wheat Yield Increase

Identifies districts showing the highest increase in wheat yield between the first and last years of the final five-year period.

### Q3. States with Highest Growth in Oilseed Production

Calculates the five-year percentage growth in oilseed production across states.

### Q4. District-wise Correlation Between Area and Production

Calculates the correlation between cultivated area and production for:

* Rice
* Wheat
* Maize

### Q5. Yearly Cotton Production Growth

Analyzes yearly cotton production trends for the top five cotton-producing states.

### Q6. Highest Groundnut Production in 2017

Identifies districts with the highest groundnut production during 2017.

### Q7. Annual Average Maize Yield

Visualizes the yearly average maize yield across all states.

### Q8. Total Oilseed Cultivated Area

Compares total cultivated oilseed area across Indian states.

### Q9. Districts with Highest Rice Yield

Identifies districts with the highest average historical rice yield.

### Q10. Wheat vs Rice Production Comparison

Compares rice and wheat production across the top five states over the final ten years of available data.

---

## 🌱 5. Crop Recommendation Helper

The dashboard includes a simple **rule-based crop recommendation system**.

Users can select:

1. State
2. District

The application then evaluates the historical yield data available for different crops in that district.

The ranking considers:

* Average historical yield
* Yield trend
* Number of recorded years

The crop with the highest historical average yield is presented as the best-performing crop for the selected district.

> **Note:** This is a descriptive, rule-based recommendation and not a machine-learning prediction model.

---

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Streamlit**
* **Plotly**
* **Excel / XLSX**
* **Exploratory Data Analysis**
* **Statistical Correlation**
* **Data Cleaning & Preprocessing**

---

## 📂 Project Structure

```text
AgriData-Explorer/
│
├── agridata_explorer_app.py
├── ICRISAT-District_Level_Data.xlsx
└── README.md
```

The Excel dataset should be placed in the **same folder** as the Python application unless the `DATA_PATH` variable is modified.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AgriData-Explorer.git
```

### 2. Navigate to the project folder

```bash
cd AgriData-Explorer
```

### 3. Install the required libraries

```bash
pip install pandas numpy streamlit plotly openpyxl
```

---

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run agridata_explorer_app.py
```

The application will open in your browser.

---

## 📊 Dataset

The project uses:

**ICRISAT District-Level Data**

Dataset file:

```text
ICRISAT-District_Level_Data.xlsx
```

The dataset contains district-level agricultural information including:

* State
* District
* Year
* Crop cultivated area
* Crop production
* Crop yield

The application works with multiple crops including:

* Rice
* Wheat
* Maize
* Sorghum
* Pearl Millet
* Finger Millet
* Barley
* Chickpea
* Pigeonpea
* Groundnut
* Sesamum
* Rapeseed & Mustard
* Safflower
* Castor
* Linseed
* Sunflower
* Soybean
* Oilseeds
* Sugarcane
* Cotton

---

## 📈 Key Data Analysis Techniques

This project demonstrates practical data analytics techniques such as:

### Data Cleaning

* Missing-value identification
* Sentinel-value replacement
* Text standardization
* Data type conversion

### Aggregation

```python
groupby()
sum()
mean()
nlargest()
```

### Correlation Analysis

```python
corr()
```

Used to examine relationships between cultivated area and agricultural production.

### Time-Series Analysis

Agricultural production and yield are aggregated by year to identify historical trends.

### Ranking

The project uses ranking techniques to identify:

* Top-producing states
* Top-performing districts
* Highest-yield crops
* Highest-growth states

### Interactive Visualization

Plotly is used to create:

* Bar charts
* Line charts
* Scatter plots
* Pie charts
* Histograms

---

## 💡 Business / Analytical Value

The project demonstrates how agricultural datasets can be converted into actionable insights.

Potential applications include:

* Identifying major crop-producing regions
* Comparing agricultural productivity across states
* Studying long-term production trends
* Understanding the relationship between cultivated area and production
* Identifying high-performing districts
* Supporting preliminary crop-selection decisions

---

## 🎯 Skills Demonstrated

This project showcases practical experience in:

* Python Data Analysis
* Pandas
* NumPy
* Exploratory Data Analysis
* Data Cleaning
* Data Visualization
* Statistical Analysis
* Time-Series Analysis
* Streamlit Dashboard Development
* Plotly
* SQL-style analytical thinking
* Agricultural Data Analytics

---

## 🔮 Future Improvements

Potential improvements include:

* Machine-learning-based crop recommendation
* Weather and rainfall integration
* Soil-property integration
* Interactive geographical maps
* State and district filters
* Crop price and market data integration
* Production forecasting
* Yield prediction
* Automated report generation
* Deployment through Streamlit Cloud

---

## 📌 Project Purpose

This project was developed to demonstrate an end-to-end **data analytics workflow**, starting from raw agricultural data and progressing through:

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
Exploratory Data Analysis
     ↓
Statistical Analysis
     ↓
Interactive Visualization
     ↓
Analytical Insights
     ↓
Crop Recommendation
```

---

## 🖥️ Application Navigation

The Streamlit application is organized into five sections:

```text
🌾 AgriData Explorer

├── 🏠 Overview
├── 🧹 Data Cleaning Summary
├── 📊 EDA Explorer
├── 🧠 SQL-Style Insights (Q1–Q10)
└── 🌱 Crop Recommendation Helper
```
