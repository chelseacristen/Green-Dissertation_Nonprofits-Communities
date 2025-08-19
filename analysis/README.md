## Data Analysis ##

This folder contains the following scripts used to conduct analysis for this dissertation project:

**1: Data Preparation for Analysis (analysis_data_preparation.py):** Data preparation pipeline that transforms processed nonprofit datasets into analysis-ready formats for econometric modeling. The script performs data cleaning, merges multiple data sources, creates derived variables, and implements categorical encoding to prepare datasets for statistical analysis of nonprofit wealth determinants.

*Dependencies: pandas, numpy, os, re
Input: Processed nonprofit datasets, government grants data, NTEE classifications
Analysis Focus: 501(c)(3) organizations with validated geographic attribution*

**2: Exploratory Data Analysis (nonprofit_wealth_eda.py):** Statistical exploration and visualization pipeline for understanding relationships between nonprofit wealth, community characteristics, and organizational factors. The script generates visualizations, like masked heatmaps, and correlation analyses to identify key patterns in nonprofit financial data before formal modeling.

*Dependencies: pandas, numpy, seaborn, matplotlib
Visualization Focus: Wealth determinants, demographic relationships, organizational patterns*

**3: Statistical Modeling Pipeline (nonprofit_wealth_modeling.py):** Econometric modeling system deploying machine learning feature selection and advanced statistical methods to identify determinants of nonprofit organizational wealth. The script implements LASSO regularization for automated feature selection followed by OLS regression with clustered standard errors to account for geographic correlation and ensure reliable statistical inference.

Key Functions:

- LASSO regularization for automated feature selection across variable categories
- Multi-model comparison framework testing organizational, environmental, demographic, and policy effects
- Clustered and heteroskedasticity-consistent standard error corrections for geographic correlation
- Race-organization interaction effects and multiple dependent variable specifications

Methods:

- Dependent Variables: Log assets/income, binary wealth indicators
- Techniques: LASSO feature selection, OLS with clustered standard errors, L1-penalized logistic regression
- Variable Categories: Organizational, environmental, demographic, historical policy effects
- Evaluation: Cross-validation, R²/AIC/BIC model comparison

*Dependencies: pandas, statsmodels, sklearn, numpy, scipy
Statistical Methods: LASSO regularization, econometric modeling, clustered inference*
