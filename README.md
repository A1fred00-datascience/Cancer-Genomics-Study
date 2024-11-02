# Colon Cancer Genomics and Drug Sensitivity Analysis

This project focuses on the genomics and drug sensitivity analysis for colon cancer, utilizing datasets from GDSC1, GDSC2, cell line information, and compounds. The project implements data preprocessing, exploratory data analysis, and machine learning modeling to predict drug sensitivity (AUC) values for different compounds tested on colon cancer cell lines.

## Introduction
This project is dedicated to analyzing colon cancer genomics data to predict drug sensitivity, primarily focusing on colon cancer cell lines. Leveraging machine learning techniques, we aim to explore the relationships between genomic features and drug responses, measured as AUC (Area Under Curve) values for different compounds. The analysis includes feature engineering, exploratory data analysis (EDA), model training, and feature importance evaluation.

## Project Structure
- **Colon_Cancer_Genomics.py**: Main Python script containing data loading, preprocessing, EDA, model training, and evaluation.
- **Data Files**: 
  - `colon-cancer.csv`: Colon cancer dataset.
  - `GDSC_DATASET.csv`: Drug sensitivity dataset (GDSC1).
  - `GDSC2-dataset.csv`: Additional drug sensitivity data (GDSC2).
  - `Cell_Lines_Details.xlsx`: Cell line information.
  - `Compounds-annotation.csv`: Compounds data with drug information and targets.
- **Output Files**: Results saved to `Cancer_Analysis_Results.xlsx`.

## Data Description
1. **Colon Cancer Dataset**: Contains genomic information for colon cancer patients.
2. **GDSC1 and GDSC2 Datasets**: Drug sensitivity data, detailing the response of various cell lines to specific drugs.
3. **Cell Line Dataset**: Describes characteristics of cell lines, including genomic alterations.
4. **Compounds Dataset**: Information on compounds, including drug names, targets, and pathways.

# Data Loading and Preprocessing

- Load datasets (GDSC1, GDSC2, Cell Lines, and Compounds).
- Merge datasets based on COSMIC_ID, CELL_LINE_NAME, and DRUG_ID.
- Handle missing values:
- Fill numerical columns with mean values.
- Fill categorical columns with the most frequent values.
- Encode categorical columns using LabelEncoder.
- Scale numerical features using StandardScaler.
- Exploratory Data Analysis (EDA)

### Distribution Plot: Displays the distribution of AUC values.
### Correlation Heatmap: Highlights correlations between features.
### Scatter Plot: Plots the relationship between LN_IC50 and AUC.
### Box Plot: Shows drug sensitivity across different tissue types.
### Violin Plot: Displays AUC distribution by MSI status.
### Pair Plot: Examines relationships between selected features.

# Model Training
- Algorithm: Random Forest Regressor
- Training and Test Split: 80/20 split for training and testing.
- Training Process: Fit the model on the training dataset using selected features.
- Model Evaluation

# The model's performance is evaluated using:
- Mean Squared Error (MSE)
- R-squared (R²)
- Both metrics are displayed after the model evaluation, showing how well the model fits the data.

# Feature Importance
Top 10 important features in predicting AUC values are displayed in a horizontal bar plot, derived from the Random Forest Regressor's feature importances.

# Saving Results
Results are saved in an Excel file, Cancer_Analysis_Results.xlsx, with multiple sheets:

- Model Evaluation: Displays MSE and R².
- Feature Importance: Lists feature importance values.
- Summary Statistics: Provides descriptive statistics for selected features.
- Correlation Matrix: Shows feature correlations.

