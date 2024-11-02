#%% Importing Necessary Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from openpyxl import Workbook

#%% Step 1: Data Loading
# Load datasets (make sure these paths are correct)
colon_cancer = pd.read_csv('/Users/alfredoserranofigueroa/Desktop/Github/Colon_Cancer_ML/colon-cancer.csv')
gdsc1 = pd.read_csv('/Users/alfredoserranofigueroa/Desktop/Github/Colon_Cancer_ML/GDSC_DATASET.csv')
gdsc2 = pd.read_csv('/Users/alfredoserranofigueroa/Desktop/Github/Colon_Cancer_ML/GDSC2-dataset.csv')
cell_lines = pd.read_excel('/Users/alfredoserranofigueroa/Desktop/Github/Colon_Cancer_ML/Cell_Lines_Details.xlsx')
compounds = pd.read_csv('/Users/alfredoserranofigueroa/Desktop/Github/Colon_Cancer_ML/Compounds-annotation.csv')

# Print column names for verification
print("Colon Cancer Columns:", colon_cancer.columns)
print("GDSC1 Columns:", gdsc1.columns)
print("GDSC2 Columns:", gdsc2.columns)
print("Cell Lines Columns:", cell_lines.columns)
print("Compounds Columns:", compounds.columns)

#%% Step 2: Data Preprocessing
# Rename columns to match across datasets
cell_lines.rename(columns={'COSMIC identifier': 'COSMIC_ID', 'Sample Name': 'CELL_LINE_NAME'}, inplace=True)

# Concatenate GDSC datasets
gdsc = pd.concat([gdsc1, gdsc2], ignore_index=True)

# Merge datasets
merged_data = gdsc.merge(
    cell_lines[['COSMIC_ID', 'CELL_LINE_NAME', 'Gene Expression', 'Copy Number Alterations (CNA)', 'Whole Exome Sequencing (WES)']],
    on=['COSMIC_ID', 'CELL_LINE_NAME'],
    how='left'
).merge(
    compounds[['DRUG_ID', 'DRUG_NAME', 'TARGET', 'TARGET_PATHWAY']],
    on='DRUG_ID',
    how='left',
    suffixes=('', '_compound')
)

# Drop duplicates and handle missing values
merged_data.drop_duplicates(inplace=True)
merged_data.dropna(subset=['AUC'], inplace=True)

# Fill missing values in numerical and categorical columns
numerical_cols = merged_data.select_dtypes(include=['float64', 'int64']).columns
merged_data[numerical_cols] = merged_data[numerical_cols].fillna(merged_data[numerical_cols].mean())
categorical_cols = merged_data.select_dtypes(include=['object']).columns
for col in categorical_cols:
    merged_data[col] = merged_data[col].fillna(merged_data[col].mode()[0])

# Encode categorical features
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    merged_data[col] = le.fit_transform(merged_data[col].astype(str))
    label_encoders[col] = le

# Scale numerical features
scaler = StandardScaler()
merged_data[numerical_cols] = scaler.fit_transform(merged_data[numerical_cols])

#%% Step 3: Exploratory Data Analysis (EDA)

# Distribution plot of AUC
plt.figure(figsize=(12, 6))
sns.histplot(merged_data['AUC'], bins=30, kde=True)
plt.title('Distribution of AUC')
plt.xlabel('AUC')
plt.ylabel('Frequency')
plt.show()
plt.clf()

# Correlation heatmap
plt.figure(figsize=(15, 12))
sns.heatmap(merged_data.corr(), cmap='coolwarm', annot=False)
plt.title('Feature Correlation Heatmap')
plt.show()
plt.clf()

# Scatter plot of LN_IC50 vs AUC
plt.figure(figsize=(10, 6))
sns.scatterplot(data=merged_data, x='LN_IC50', y='AUC', alpha=0.5)
plt.title('Scatter Plot of LN_IC50 vs AUC')
plt.xlabel('LN_IC50')
plt.ylabel('AUC')
plt.show()
plt.clf()

# Box plot of AUC across different tissue types
plt.figure(figsize=(12, 6))
sns.boxplot(data=merged_data, x='GDSC Tissue descriptor 1', y='AUC')
plt.xticks(rotation=90)
plt.title('Drug Sensitivity (AUC) Across Different Tissue Types')
plt.xlabel('Tissue Type')
plt.ylabel('AUC')
plt.show()
plt.clf()

# Violin plot of AUC by MSI Status
plt.figure(figsize=(10, 6))
sns.violinplot(data=merged_data, x='Microsatellite instability Status (MSI)', y='AUC')
plt.title('Distribution of AUC by MSI Status')
plt.xlabel('MSI Status')
plt.ylabel('AUC')
plt.show()
plt.clf()

# Pair plot for selected features
sample_data = merged_data.sample(200, random_state=42)
selected_features = [col for col in ['AUC', 'LN_IC50', 'Gene Expression', 'Copy Number Alterations (CNA)'] if col in sample_data.columns]
sns.pairplot(sample_data[selected_features], diag_kind='kde')
plt.suptitle('Pair Plot for Selected Features', y=1.02)
plt.show()

# Feature distribution of Gene Expression and CNA
if 'Gene Expression' in merged_data.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(merged_data['Gene Expression'], bins=30, kde=True)
    plt.title('Distribution of Gene Expression')
    plt.xlabel('Gene Expression')
    plt.ylabel('Frequency')
    plt.show()
    plt.clf()

if 'Copy Number Alterations (CNA)' in merged_data.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(merged_data['Copy Number Alterations (CNA)'], bins=30, kde=True)
    plt.title('Distribution of Copy Number Alterations (CNA)')
    plt.xlabel('Copy Number Alterations (CNA)')
    plt.ylabel('Frequency')
    plt.show()
    plt.clf()

#%% Step 4: Model Training

X = merged_data.drop(['AUC', 'LN_IC50'], axis=1)
y = merged_data['AUC']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

#%% Step 5: Model Evaluation

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print('Model Performance:')
print(f'Mean Squared Error: {mse:.4f}')
print(f'R-squared: {r2:.4f}')

# Feature importance
importances = model.feature_importances_
indices = np.argsort(importances)[-10:]  # Top 10 features
plt.figure(figsize=(12, 6))
plt.barh(range(len(indices)), importances[indices], align='center')
plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
plt.xlabel('Feature Importance')
plt.title('Top 10 Feature Importances in RandomForest Model')
plt.show()

#%% Step 6: Save Results to Excel

# Creating an Excel writer and workbook
excel_writer = pd.ExcelWriter('Cancer_Analysis_Results.xlsx', engine='openpyxl')

# Model metrics
model_metrics = pd.DataFrame({
    'Metric': ['Mean Squared Error', 'R-squared'],
    'Value': [mse, r2]
})
model_metrics.to_excel(excel_writer, sheet_name='Model Evaluation', index=False)

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)
feature_importance.to_excel(excel_writer, sheet_name='Feature Importance', index=False)

# Summary statistics
summary_stats = merged_data[['AUC', 'LN_IC50', 'Gene Expression', 'Copy Number Alterations (CNA)']].describe()
summary_stats.to_excel(excel_writer, sheet_name='Summary Statistics')

# Correlation matrix
correlation_matrix = merged_data.corr()
correlation_matrix.to_excel(excel_writer, sheet_name='Correlation Matrix')

# Save and close the Excel writer
excel_writer.save()
excel_writer.close()
print("Results have been saved to Cancer_Analysis_Results.xlsx")
