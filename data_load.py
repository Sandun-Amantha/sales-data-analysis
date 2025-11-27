import pandas as pd

# Load the dataset
try:
    df = pd.read_csv('sales_data_sample.csv', encoding='latin-1')
except UnicodeDecodeError:
    # Try a different common encoding if 'utf-8' fails
    df = pd.read_csv('sales_data_sample.csv', encoding='iso-8859-1')

print("--- Initial Data Shape ---")
print(df.shape)

print("\n--- Column Information and Data Types ---")
print(df.info())

print("\n--- Missing Value Count (Top 10) ---")
print(df.isnull().sum().sort_values(ascending=False).head(10))

print("\n--- First 5 Rows ---")
print(df.head())