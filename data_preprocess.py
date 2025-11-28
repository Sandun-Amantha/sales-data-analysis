import pandas as pd

# Load the dataset (using the determined encoding, or assuming it's correctly loaded in the environment)
try:
    # Assuming the file is accessible in the execution environment
    df = pd.read_csv('sales_data_sample.csv', encoding='latin-1')
except FileNotFoundError:
    print("Error: sales_data_sample.csv not found.")
    # Exit or handle the error appropriately
    # For this environment, we assume the file access is successful based on the previous step

# 1. Data Type Conversion: Convert ORDERDATE to datetime
# The original format might be M/D/YY H:MM (e.g., 2/24/2003 0:00)
# We use errors='coerce' to turn unparseable dates into NaT (Not a Time)
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')

# Check if any dates were coerced to NaT (Not Applicable Time)
if df['ORDERDATE'].isnull().sum() > 0:
    print(f"Warning: {df['ORDERDATE'].isnull().sum()} ORDERDATE values were unparseable and set to NaT.")
    # For a real project, we would investigate/impute these, but for this exercise, we will proceed.
    # Since the previous info showed 2823 non-null, this is just a precaution.

# 2. Missing Value Handling: Fill non-critical geographical columns with 'N/A'
cols_to_fill = ['STATE', 'TERRITORY', 'POSTALCODE', 'ADDRESSLINE2']
df[cols_to_fill] = df[cols_to_fill].fillna('N/A')

# 3. Feature Engineering: Create time-based features
# Extract Day of Week (0=Monday, 6=Sunday)
df['DAY_OF_WEEK'] = df['ORDERDATE'].dt.dayofweek
# Extract Month Name for better visualization labeling
df['MONTH_NAME'] = df['ORDERDATE'].dt.strftime('%b')

# 4. Save the processed data to a new CSV
processed_file_name = 'sales_data_processed.csv'
df.to_csv(processed_file_name, index=False)

print(f"\n--- Processed Data Info ---")
print(df[['ORDERDATE', 'DAY_OF_WEEK', 'MONTH_NAME'] + cols_to_fill].head())
print(f"\n--- Data Saved ---")
print(f"The cleaned and engineered data has been saved as '{processed_file_name}'")