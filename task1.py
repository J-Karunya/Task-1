import pandas as pd

# Load the dataset
df = pd.read_csv('car_prices.csv')

# Step 1: Remove duplicate rows
df_cleaned = df.drop_duplicates()

# Step 2: Handle missing values
# Drop rows missing critical information
df_cleaned = df_cleaned.dropna(subset=['make', 'model', 'saledate', 'vin', 'sellingprice'])

# Fill missing condition with median
df_cleaned['condition'] = df_cleaned['condition'].fillna(df_cleaned['condition'].median())

# Fill missing transmission with mode
df_cleaned['transmission'] = df_cleaned['transmission'].fillna(df_cleaned['transmission'].mode()[0])

# Step 3: Standardize text values
df_cleaned['color'] = df_cleaned['color'].str.strip().str.lower()
df_cleaned['interior'] = df_cleaned['interior'].str.strip().str.lower()
df_cleaned['seller'] = df_cleaned['seller'].str.strip().str.lower()

# Step 4: Convert 'saledate' to datetime with format handling
df_cleaned['saledate'] = pd.to_datetime(
    df_cleaned['saledate'].str.extract(r'([A-Za-z]{3} \w+ \d{1,2} \d{4})')[0],
    format='%a %b %d %Y',
    errors='coerce'
)
df_cleaned = df_cleaned.dropna(subset=['saledate'])  # Remove rows with invalid date parsing

# Step 5: Clean column names
df_cleaned.columns = df_cleaned.columns.str.strip().str.lower().str.replace(' ', '_')

# Step 6: Ensure correct data types
df_cleaned['odometer'] = df_cleaned['odometer'].astype(float)
df_cleaned['sellingprice'] = df_cleaned['sellingprice'].astype(float)
df_cleaned['mmr'] = df_cleaned['mmr'].astype(float)

# Save cleaned dataset
df_cleaned.to_csv('car_prices_cleaned.csv', index=False)

# Optional: Print summary
print("✅ Cleaning Completed")
print(f"Initial rows: {len(df)}")
print(f"Final rows: {len(df_cleaned)}")
print(f"Duplicates removed: {len(df) - len(df.drop_duplicates())}")
print(f"Rows dropped (missing critical info): {len(df.drop_duplicates()) - len(df_cleaned)}")
