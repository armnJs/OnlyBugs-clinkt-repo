import pandas as pd
import numpy as np

interactions = pd.read_csv('customer_interactions.csv')
customers = pd.read_csv('customers.csv')
inventory = pd.read_csv('inventory.csv')
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')

# Derived column 1: Conversion / abandoned cart
# interactions has Product_ID, Session_ID, Interaction_Type ('View', 'Add_to_Cart')
add_to_cart = interactions[interactions['Interaction_Type'] == 'Add_to_Cart'].copy()
# merge with orders to see if ordered
order_prod = orders[['Session_ID', 'Product_ID']].drop_duplicates()
order_prod['Ordered'] = 1
cart_analysis = add_to_cart.merge(order_prod, on=['Session_ID', 'Product_ID'], how='left')
cart_analysis['Ordered'] = cart_analysis['Ordered'].fillna(0)
print(f"Total Adds to Cart: {len(cart_analysis)}, Actually Ordered: {cart_analysis['Ordered'].sum()}")

# What about stockouts?
# Join inventory with products to see which categories have low stock
inventory = inventory.merge(products[['Product_ID', 'Product_Name', 'Category']], on='Product_ID')
print("Stock Status counts:\n", inventory['Stock_Status'].value_counts())

# Join orders with inventory? No, inventory is daily. Let's check stock status for ordered products.
orders['Order_Date'] = pd.to_datetime(orders['Order_Timestamp']).dt.date.astype(str)
inventory['Date'] = inventory['Date'].astype(str)
orders_inv = orders.merge(inventory, left_on=['Product_ID', 'Order_Date'], right_on=['Product_ID', 'Date'], how='left')
print("Orders joined with inventory Stock Status:\n", orders_inv['Stock_Status'].value_counts())

# Let's check if the un-ordered add_to_carts are due to out of stock
add_to_cart_date = add_to_cart.copy()
add_to_cart_date['Date'] = pd.to_datetime(add_to_cart_date['Timestamp']).dt.date.astype(str)
cart_inv = add_to_cart_date.merge(order_prod, on=['Session_ID', 'Product_ID'], how='left')
cart_inv['Ordered'] = cart_inv['Ordered'].fillna(0)
cart_inv = cart_inv.merge(inventory, on=['Product_ID', 'Date'], how='left')
abandoned = cart_inv[cart_inv['Ordered'] == 0]
print("Abandoned carts stock status:\n", abandoned['Stock_Status'].value_counts())

# Wait, maybe there's a big issue with out of stock?
print(abandoned.groupby('Stock_Status')['Interaction_ID'].count())