import pandas as pd
import numpy as np

# Part 1: Data Ingestion
df = pd.read_csv("ecommerce_sales.csv")

# Part 2: Data Cleaning     
# 2-1

# Checking and dropping out duplicates based on order id
df = df.drop_duplicates(subset=['order_id'],keep='first',ignore_index=False)

# Replacing non-critical missing values
df = df.fillna({'country': 'Missing', 'product_id': 'Missing', 'customer_id': 'Missing'})

# Interpolate missing customer_id
df['customer_id'].interpolate(method='linear', inplace=True)

# Get missing unit_price according to similar product_id
df.loc[(df['product_id'] == 1003) & (df['unit_price'].isnull()), 'unit_price'] = 299.99

price_groups = df.groupby('product_id')['unit_price'].apply(list)



# Dropping rows where quantity or price is missing
df = df.dropna(subset=['quantity', 'unit_price'], how='any')

# missing_values = df.isnull().sum()
# print(missing_values)

# Part 2: Data Cleaning
# 2-2

# Converting order date column to datetime format
df['order_date'] = pd.to_datetime(df['order_date'])

# Converting quantity column to int64 format
df['quantity'] = df['quantity'].astype('int64')

# print(df.dtypes)


# Part 3: Data Manipulation
# 3-1

# Creating a new column by multiplying the quantity with price
df['total_sales'] = df['quantity'] * df['unit_price']

# 3-2

# Extracting new columns for order weekdays and months using order datetime
df['order_weekday'] = df['order_date'].dt.day_name()
df['order_month'] = df['order_date'].dt.month_name()

# Part 4: Data Transformation
# 4-1

# group by product_category and summiarize total sales and average quantity
# df_product_sum = merged_df_all.groupby(['user_id','name']).apply(lambda x: (x['price'] * x['quantity']).sum())

# Calculate total sales and average quantity of a sale per category 

df_category_totals = df.groupby('product_category').agg({'total_sales': 'sum', 'quantity': 'mean'}).round({'quantity': 2})
df_category_totals = df_category_totals.sort_values('total_sales', ascending=False)
print(df_category_totals)

# 4-2

# groupby total sales per month for each product

df_sales_per_month = df.groupby(['product_category', 'order_month']).agg({'total_sales': 'sum'})

print(df_sales_per_month)

# 4-3
average_price = df['unit_price'].mean()
df['normalized_price'] = (df['unit_price'] / average_price).round(2)

print(df.head(10))