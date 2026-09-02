"""
Export all derived/cleaned datasets as separate Excel files.
"""
import os
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\VIBEHACK\Desktop\CLINKT_CASE_FILE\PARTICIPANT_PACKAGE"
OUTPUT_DIR = r"c:\Users\VIBEHACK\Desktop\clinkt-repo\cleaned data\exports"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.chdir(DATA_DIR)

# Load raw data
interactions = pd.read_csv('customer_interactions.csv')
customers = pd.read_csv('customers.csv')
inventory = pd.read_csv('inventory.csv')
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')

# ---- 1. Cart Analysis (add-to-cart vs actually ordered) ----
add_to_cart = interactions[interactions['Interaction_Type'] == 'Add_to_Cart'].copy()
order_prod = orders[['Session_ID', 'Product_ID']].drop_duplicates()
order_prod['Ordered'] = 1
cart_analysis = add_to_cart.merge(order_prod, on=['Session_ID', 'Product_ID'], how='left')
cart_analysis['Ordered'] = cart_analysis['Ordered'].fillna(0).astype(int)
cart_analysis.to_excel(os.path.join(OUTPUT_DIR, '1_cart_analysis.xlsx'), index=False)
print("Saved: 1_cart_analysis.xlsx  ({} rows)".format(len(cart_analysis)))

# ---- 2. Inventory with Product Details ----
inventory_enriched = inventory.merge(products[['Product_ID', 'Product_Name', 'Category']], on='Product_ID')
inventory_enriched.to_excel(os.path.join(OUTPUT_DIR, '2_inventory_enriched.xlsx'), index=False)
print("Saved: 2_inventory_enriched.xlsx  ({} rows)".format(len(inventory_enriched)))

# ---- 3. Orders joined with Inventory Stock Status ----
orders['Order_Date'] = pd.to_datetime(orders['Order_Timestamp']).dt.date.astype(str)
inventory_enriched['Date'] = inventory_enriched['Date'].astype(str)
orders_with_stock = orders.merge(inventory_enriched, left_on=['Product_ID', 'Order_Date'], right_on=['Product_ID', 'Date'], how='left')
orders_with_stock.to_excel(os.path.join(OUTPUT_DIR, '3_orders_with_stock_status.xlsx'), index=False)
print("Saved: 3_orders_with_stock_status.xlsx  ({} rows)".format(len(orders_with_stock)))

# ---- 4. Abandoned Carts with Stock & Product Info ----
add_to_cart_date = add_to_cart.copy()
add_to_cart_date['Date'] = pd.to_datetime(add_to_cart_date['Timestamp']).dt.date.astype(str)
cart_inv = add_to_cart_date.merge(order_prod, on=['Session_ID', 'Product_ID'], how='left')
cart_inv['Ordered'] = cart_inv['Ordered'].fillna(0).astype(int)
cart_inv = cart_inv.merge(inventory_enriched, on=['Product_ID', 'Date'], how='left')
abandoned = cart_inv[cart_inv['Ordered'] == 0].copy()
abandoned = abandoned.merge(products[['Product_ID', 'Price']], on='Product_ID', how='left')
abandoned.to_excel(os.path.join(OUTPUT_DIR, '4_abandoned_carts.xlsx'), index=False)
print("Saved: 4_abandoned_carts.xlsx  ({} rows)".format(len(abandoned)))

# ---- 5. Abandonment Rate by Category ----
cart_inv_cat = cart_inv.groupby(['Category', 'Ordered']).size().unstack(fill_value=0)
cart_inv_cat.columns = ['Not_Ordered', 'Ordered']
cart_inv_cat['Abandonment_Rate'] = cart_inv_cat['Not_Ordered'] / (cart_inv_cat['Not_Ordered'] + cart_inv_cat['Ordered'])
cart_inv_cat = cart_inv_cat.reset_index()
cart_inv_cat.to_excel(os.path.join(OUTPUT_DIR, '5_abandonment_by_category.xlsx'), index=False)
print("Saved: 5_abandonment_by_category.xlsx")

# ---- 6. Abandonment Rate by Customer Segment ----
cart_cust = cart_inv.merge(customers, on='Customer_ID', how='left')
cart_cust_seg = cart_cust.groupby(['Customer_Segment', 'Ordered']).size().unstack(fill_value=0)
cart_cust_seg.columns = ['Not_Ordered', 'Ordered']
cart_cust_seg['Abandonment_Rate'] = cart_cust_seg['Not_Ordered'] / (cart_cust_seg['Not_Ordered'] + cart_cust_seg['Ordered'])
cart_cust_seg = cart_cust_seg.reset_index()
cart_cust_seg.to_excel(os.path.join(OUTPUT_DIR, '6_abandonment_by_segment.xlsx'), index=False)
print("Saved: 6_abandonment_by_segment.xlsx")

# ---- 7. Cart Sizes by Segment ----
cart_sizes = cart_cust.groupby(['Session_ID', 'Customer_Segment'])['Product_ID'].count().reset_index()
cart_sizes.columns = ['Session_ID', 'Customer_Segment', 'Items_Added_to_Cart']
avg_cart = cart_sizes.groupby('Customer_Segment')['Items_Added_to_Cart'].mean().reset_index()
avg_cart.columns = ['Customer_Segment', 'Avg_Items_Added']

order_sizes = orders.merge(customers, on='Customer_ID', how='left').groupby(['Order_ID', 'Customer_Segment'])['Quantity'].sum().reset_index()
avg_order = order_sizes.groupby('Customer_Segment')['Quantity'].mean().reset_index()
avg_order.columns = ['Customer_Segment', 'Avg_Items_Ordered']

cart_vs_order = avg_cart.merge(avg_order, on='Customer_Segment')
cart_vs_order.to_excel(os.path.join(OUTPUT_DIR, '7_cart_vs_order_by_segment.xlsx'), index=False)
print("Saved: 7_cart_vs_order_by_segment.xlsx")

# ---- 8. AOV by City ----
orders_cust = orders.merge(customers, on='Customer_ID', how='left')
aov_city = orders_cust.groupby(['Order_ID', 'City'])['Total_Amount'].sum().groupby('City').mean().reset_index()
aov_city.columns = ['City', 'AOV']
order_count_city = orders_cust.groupby('City')['Order_ID'].nunique().reset_index()
order_count_city.columns = ['City', 'Order_Count']
city_summary = aov_city.merge(order_count_city, on='City')
city_summary.to_excel(os.path.join(OUTPUT_DIR, '8_aov_by_city.xlsx'), index=False)
print("Saved: 8_aov_by_city.xlsx")

# ---- 9. AOV by Segment ----
aov_seg = orders_cust.groupby(['Order_ID', 'Customer_Segment'])['Total_Amount'].sum().groupby('Customer_Segment').mean().reset_index()
aov_seg.columns = ['Customer_Segment', 'AOV']
aov_seg.to_excel(os.path.join(OUTPUT_DIR, '9_aov_by_segment.xlsx'), index=False)
print("Saved: 9_aov_by_segment.xlsx")

# ---- 10. Critical Stock Products ----
critical_stock = inventory_enriched[inventory_enriched['Stock_Status'].isin(['Critical', 'Out of Stock'])].copy()
critical_summary = critical_stock.groupby(['Product_ID', 'Product_Name', 'Category']).agg(
    Critical_Days=('Stock_Status', 'count')
).reset_index().sort_values('Critical_Days', ascending=False)
critical_summary.to_excel(os.path.join(OUTPUT_DIR, '10_critical_stock_products.xlsx'), index=False)
print("Saved: 10_critical_stock_products.xlsx")

# ---- 11. Top Abandoned vs Top Ordered Products ----
top_abandoned = abandoned.groupby(['Product_ID', 'Product_Name']).size().reset_index(name='Abandoned_Count').sort_values('Abandoned_Count', ascending=False)
top_ordered = orders.merge(products, on='Product_ID').groupby(['Product_ID', 'Product_Name']).size().reset_index(name='Order_Count').sort_values('Order_Count', ascending=False)
product_comparison = top_abandoned.merge(top_ordered, on=['Product_ID', 'Product_Name'], how='outer').fillna(0)
product_comparison['Abandoned_Count'] = product_comparison['Abandoned_Count'].astype(int)
product_comparison['Order_Count'] = product_comparison['Order_Count'].astype(int)
product_comparison = product_comparison.sort_values('Abandoned_Count', ascending=False)
product_comparison.to_excel(os.path.join(OUTPUT_DIR, '11_product_abandoned_vs_ordered.xlsx'), index=False)
print("Saved: 11_product_abandoned_vs_ordered.xlsx")

# ---- 12. Abandoned Revenue by Stock Status ----
rev_by_stock = abandoned.groupby('Stock_Status')['Price'].agg(['sum', 'mean', 'count']).reset_index()
rev_by_stock.columns = ['Stock_Status', 'Total_Lost_Revenue', 'Avg_Price', 'Count']
rev_by_stock.to_excel(os.path.join(OUTPUT_DIR, '12_abandoned_revenue_by_stock.xlsx'), index=False)
print("Saved: 12_abandoned_revenue_by_stock.xlsx")

print("\n" + "=" * 60)
print("ALL 12 FILES EXPORTED TO:")
print(OUTPUT_DIR)
print("=" * 60)
