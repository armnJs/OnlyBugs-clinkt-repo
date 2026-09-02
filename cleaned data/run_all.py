"""
Combined runner: executes all 10 analysis scripts in order.
Data is loaded from the CLINKT_CASE_FILE participant package.
"""
import os
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import glob

DATA_DIR = r"C:\Users\VIBEHACK\Desktop\CLINKT_CASE_FILE\PARTICIPANT_PACKAGE"
os.chdir(DATA_DIR)

# ============================================================
# Script 1 - Data Overview
# ============================================================
print("=" * 60)
print("SCRIPT 1: Data Overview")
print("=" * 60)

print("Files in working dir:", os.listdir('.'))

files = ['customer_interactions.csv', 'customers.csv', 'inventory.csv', 'orders.csv', 'products.csv']
for f in files:
    if os.path.exists(f):
        df = pd.read_csv(f)
        print("--- {} ---".format(f))
        print("Shape:", df.shape)
        print("Columns & Types:\n", df.dtypes)
        print("Missing values:\n", df.isnull().sum())
        print("Head:\n", df.head(3))
        print("\n")

# ============================================================
# Script 2 - Cart Conversion & Stock Analysis
# ============================================================
print("=" * 60)
print("SCRIPT 2: Cart Conversion & Stock Analysis")
print("=" * 60)

interactions = pd.read_csv('customer_interactions.csv')
customers = pd.read_csv('customers.csv')
inventory = pd.read_csv('inventory.csv')
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')

# Conversion / abandoned cart
add_to_cart = interactions[interactions['Interaction_Type'] == 'Add_to_Cart'].copy()
order_prod = orders[['Session_ID', 'Product_ID']].drop_duplicates()
order_prod['Ordered'] = 1
cart_analysis = add_to_cart.merge(order_prod, on=['Session_ID', 'Product_ID'], how='left')
cart_analysis['Ordered'] = cart_analysis['Ordered'].fillna(0)
print("Total Adds to Cart: {}, Actually Ordered: {}".format(len(cart_analysis), cart_analysis['Ordered'].sum()))

# Stock analysis
inventory = inventory.merge(products[['Product_ID', 'Product_Name', 'Category']], on='Product_ID')
print("Stock Status counts:\n", inventory['Stock_Status'].value_counts())

orders['Order_Date'] = pd.to_datetime(orders['Order_Timestamp']).dt.date.astype(str)
inventory['Date'] = inventory['Date'].astype(str)
orders_inv = orders.merge(inventory, left_on=['Product_ID', 'Order_Date'], right_on=['Product_ID', 'Date'], how='left')
print("Orders joined with inventory Stock Status:\n", orders_inv['Stock_Status'].value_counts())

add_to_cart_date = add_to_cart.copy()
add_to_cart_date['Date'] = pd.to_datetime(add_to_cart_date['Timestamp']).dt.date.astype(str)
cart_inv = add_to_cart_date.merge(order_prod, on=['Session_ID', 'Product_ID'], how='left')
cart_inv['Ordered'] = cart_inv['Ordered'].fillna(0)
cart_inv = cart_inv.merge(inventory, on=['Product_ID', 'Date'], how='left')
abandoned = cart_inv[cart_inv['Ordered'] == 0]
print("Abandoned carts stock status:\n", abandoned['Stock_Status'].value_counts())
print(abandoned.groupby('Stock_Status')['Interaction_ID'].count())

# ============================================================
# Script 3 - Abandonment by Category & Segment
# ============================================================
print("=" * 60)
print("SCRIPT 3: Abandonment by Category & Segment")
print("=" * 60)

cart_inv_cat = cart_inv.groupby(['Category', 'Ordered']).size().unstack(fill_value=0)
cart_inv_cat['Abandonment_Rate'] = cart_inv_cat[0] / (cart_inv_cat[0] + cart_inv_cat[1])
print("Abandonment by Category:\n", cart_inv_cat)

cart_cust = cart_inv.merge(customers, on='Customer_ID', how='left')
cart_cust_seg = cart_cust.groupby(['Customer_Segment', 'Ordered']).size().unstack(fill_value=0)
cart_cust_seg['Abandonment_Rate'] = cart_cust_seg[0] / (cart_cust_seg[0] + cart_cust_seg[1])
print("Abandonment by Segment:\n", cart_cust_seg)

abandoned_revenue = abandoned.merge(products, on='Product_ID')
print("Total Abandoned Revenue:", abandoned_revenue['Price'].sum())

# ============================================================
# Script 4 - Family Segment & Cart Sizes
# ============================================================
print("=" * 60)
print("SCRIPT 4: Family Segment & Cart Sizes")
print("=" * 60)

fam_carts = cart_cust[cart_cust['Customer_Segment'] == 'Family']
print("Family Segment Product Categories:\n", fam_carts['Category'].value_counts())

cart_sizes = cart_cust.groupby(['Session_ID', 'Customer_Segment'])['Product_ID'].count().reset_index()
print("Average items added to cart per session by segment:\n", cart_sizes.groupby('Customer_Segment')['Product_ID'].mean())

order_sizes = orders.merge(customers, on='Customer_ID', how='left').groupby(['Order_ID', 'Customer_Segment'])['Quantity'].sum().reset_index()
print("Average items actually ordered per session by segment:\n", order_sizes.groupby('Customer_Segment')['Quantity'].mean())

# ============================================================
# Script 5 - Revenue, AOV & City Analysis
# ============================================================
print("=" * 60)
print("SCRIPT 5: Revenue, AOV & City Analysis")
print("=" * 60)

print("Total Ordered Revenue:", orders['Total_Amount'].sum())

print(interactions.head())
interactions['Timestamp'] = pd.to_datetime(interactions['Timestamp'])

print("Average Order Value (AOV) overall:", orders.groupby('Order_ID')['Total_Amount'].sum().mean())
print("AOV by segment:\n", orders.merge(customers, on='Customer_ID').groupby(['Order_ID', 'Customer_Segment'])['Total_Amount'].sum().groupby('Customer_Segment').mean())
print("Cities covered:\n", customers['City'].value_counts())

# ============================================================
# Script 6 - AOV by City
# ============================================================
print("=" * 60)
print("SCRIPT 6: AOV by City")
print("=" * 60)

aov_city = orders.merge(customers, on='Customer_ID').groupby(['Order_ID', 'City'])['Total_Amount'].sum().groupby('City').mean()
print("AOV by City:\n", aov_city)
print("Orders count by city:\n", orders.merge(customers, on='Customer_ID').groupby('City')['Order_ID'].nunique())

# ============================================================
# Script 7 - Stock Status Deep Dive
# ============================================================
print("=" * 60)
print("SCRIPT 7: Stock Status Deep Dive")
print("=" * 60)

low_stock_days = inventory[inventory['Stock_Status'].isin(['Low Stock', 'Critical', 'Out of Stock'])]
print("Percentage of product-days in sub-optimal stock:", len(low_stock_days) / len(inventory))

print(inventory['Stock_Status'].value_counts())
critical = inventory[inventory['Stock_Status'].isin(['Critical', 'Out of Stock'])].groupby('Product_Name').size().sort_values(ascending=False)
print("Most critically low products:\n", critical.head(10))

try:
    print(abandoned.groupby('Stock_Status')['Price'].sum())
except KeyError:
    print("(Price column not yet merged on abandoned - see Script 8)")

# ============================================================
# Script 8 - Abandoned Revenue by Stock Status
# ============================================================
print("=" * 60)
print("SCRIPT 8: Abandoned Revenue by Stock Status")
print("=" * 60)

abandoned = abandoned.merge(products[['Product_ID', 'Price']], on='Product_ID', how='left')
print("Abandoned Revenue by Stock Status:\n", abandoned.groupby('Stock_Status')['Price'].sum())
print("Avg price abandoned:", abandoned['Price'].mean())
print("Avg price ordered:", orders['Unit_Price'].mean())

# ============================================================
# Script 9 - Top Abandoned & Ordered Products
# ============================================================
print("=" * 60)
print("SCRIPT 9: Top Abandoned & Ordered Products")
print("=" * 60)

print("Most abandoned products:\n", abandoned.groupby('Product_Name').size().sort_values(ascending=False).head(10))
print("\nMost ordered products:\n", orders.merge(products, on='Product_ID').groupby('Product_Name').size().sort_values(ascending=False).head(10))

# ============================================================
# Script 10 - Family Carts Summary
# ============================================================
print("=" * 60)
print("SCRIPT 10: Family Carts Summary")
print("=" * 60)

fam_carts_summary = cart_cust_seg.loc['Family']
print("Family Carts:", fam_carts_summary)

print("\n" + "=" * 60)
print("ALL 10 SCRIPTS EXECUTED SUCCESSFULLY")
print("=" * 60)
