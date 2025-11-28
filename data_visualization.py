import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the processed dataset
df = pd.read_csv('sales_data_processed.csv')

# Ensure ORDERDATE is datetime, even though it was converted, just to be safe after loading from CSV
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

# --- 1. Total Sales by Product Line ---
sales_by_product = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False).reset_index()

# Plotting Total Sales by Product Line
plt.figure(figsize=(12, 6))
# Using Seaborn for a clean, professional bar plot
sns.barplot(x='PRODUCTLINE', y='SALES', data=sales_by_product, palette='viridis')
plt.title('Total Sales by Product Line (USD)')
plt.xlabel('Product Line')
plt.ylabel('Total Sales (USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
# Save the plot
plt.savefig('sales_by_productline.png')
plt.close()

# --- 2. Sales Trend Over Time (Monthly) ---
# Group sales by Year and Month IDs for correct chronological ordering
df_monthly_sales = df.groupby(['YEAR_ID', 'MONTH_ID'])['SALES'].sum().reset_index()
# Create a sortable period string (e.g., '2003-02')
df_monthly_sales['PERIOD'] = (
    df_monthly_sales['YEAR_ID'].astype(str) + '-' + 
    df_monthly_sales['MONTH_ID'].astype(str).str.zfill(2)
)
df_monthly_sales = df_monthly_sales.sort_values(by='PERIOD')

# Plotting Sales Over Time
plt.figure(figsize=(14, 7))
# Using Matplotlib for the time-series line plot
plt.plot(df_monthly_sales['PERIOD'], df_monthly_sales['SALES'], 
         marker='o', linestyle='-', color='b', markersize=4)
plt.title('Total Sales Trend Over Time (Monthly)')
plt.xlabel('Year-Month')
plt.ylabel('Total Sales (USD)')
# Adjust X-axis labels for readability
plt.xticks(rotation=60, ha='right', fontsize=8) 
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
# Save the plot
plt.savefig('sales_over_time_monthly.png')
plt.close()

# --- 3. Output Metrics ---
total_sales_metric = df['SALES'].sum()
sales_by_product.to_csv('sales_by_product_line_metric.csv', index=False)

print(f"Overall Total Sales: ${total_sales_metric:,.2f}")
print("Top 5 Product Lines by Sales:")
print(sales_by_product.head())