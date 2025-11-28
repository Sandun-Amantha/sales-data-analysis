import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import seaborn as sns

# Load the processed dataset
# Assuming 'sales_data_processed.csv' exists from the initial data cleaning step
df = pd.read_csv('sales_data_processed.csv')
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

# --- 1. Aggregate Data to Monthly Series ---
# Set ORDERDATE as index and resample to monthly sum of sales
df_monthly = df.set_index('ORDERDATE').resample('M')['SALES'].sum()

# --- 2. Build and Fit the ARIMA Model ---
# Using a simplified order for demonstration (4, 1, 2)
order = (4, 1, 2) 

try:
    # Fit the ARIMA model to the historical monthly sales data
    model = ARIMA(df_monthly, order=order)
    model_fit = model.fit()

    # --- 3. Forecast for the next 3 steps (3 months) ---
    forecast_steps = 3
    # Get the predicted sales values
    forecast_values = model_fit.forecast(steps=forecast_steps)
    # Create a range of dates for the forecast (starting right after the last historical date)
    forecast_dates = pd.date_range(start=df_monthly.index[-1], periods=forecast_steps + 1, freq='M')[1:]

    # --- 4. Prepare Combined Forecast DataFrame ---
    df_forecast = pd.DataFrame({
        'ORDERDATE': forecast_dates,
        'SALES': forecast_values,
        # Label these entries as 'Forecast'
        'STATUS_TYPE': 'Forecast'
    })

    # Prepare Historical DataFrame
    df_history = df_monthly.reset_index()
    df_history['STATUS_TYPE'] = 'History'
    
    # Merge history and forecast
    df_combined = pd.concat([df_history[['ORDERDATE', 'SALES', 'STATUS_TYPE']], 
                             df_forecast[['ORDERDATE', 'SALES', 'STATUS_TYPE']]], 
                            ignore_index=True)
    
    # Save the combined data (history + forecast)
    processed_file_name = 'sales_forecast_monthly.csv'
    df_combined.to_csv(processed_file_name, index=False)
    
    # --- 5. Generate Visualization for Confirmation ---
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_combined, x='ORDERDATE', y='SALES', hue='STATUS_TYPE', marker='o')
    plt.title('Sales History and 3-Month Forecast')
    plt.xlabel('Date')
    plt.ylabel('Sales (USD)')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('sales_forecast_visualization.png')
    plt.close()


    print("\n--- Sales Forecast Results ---")
    print(f"Historical data used up to: {df_history['ORDERDATE'].max().strftime('%Y-%m-%d')}")
    print(f"Forecast for the next {forecast_steps} months:")
    print(df_forecast[['ORDERDATE', 'SALES']].round(2))
    print(f"\nNew data file saved as: '{processed_file_name}'")

except Exception as e:
    print(f"An error occurred during the ARIMA modeling: {e}")
    print("If an error occurs, the next steps relying on 'sales_forecast_monthly.csv' cannot be completed.")