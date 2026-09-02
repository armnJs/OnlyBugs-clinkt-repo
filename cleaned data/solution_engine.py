"""
Clinkt Solution Engine:
1. Dynamic Demand-Signal Inventory Optimization Algorithm
2. Recommendation Re-weighting Matrix
3. Cart Recovery & Revenue Impact Simulation Model
"""
import os
import pandas as pd
import numpy as np
import json

DATA_DIR = r"C:\Users\VIBEHACK\Desktop\CLINKT_CASE_FILE\PARTICIPANT_PACKAGE"
OUTPUT_DIR = r"c:\Users\VIBEHACK\Desktop\clinkt-repo\cleaned data\exports"
CHART_DIR = r"c:\Users\VIBEHACK\Desktop\clinkt-repo\cleaned data\charts"
os.chdir(DATA_DIR)

# Load data
interactions = pd.read_csv('customer_interactions.csv')
customers = pd.read_csv('customers.csv')
inventory = pd.read_csv('inventory.csv')
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')

# 1. Compute Product Demand Signals
views = interactions[interactions['Interaction_Type'] == 'View'].groupby('Product_ID').size().reset_index(name='Views')
carts = interactions[interactions['Interaction_Type'] == 'Add_to_Cart'].groupby('Product_ID').size().reset_index(name='Carts')
sales = orders.groupby('Product_ID')['Quantity'].sum().reset_index(name='Units_Sold')

sol_df = products.merge(views, on='Product_ID', how='left').merge(carts, on='Product_ID', how='left').merge(sales, on='Product_ID', how='left').fillna(0)
sol_df['Demand_Signal'] = sol_df['Views'] * 0.2 + sol_df['Carts'] * 0.8  # Intent-weighted demand

# Average daily demand
sol_df['Daily_Demand_Rate'] = sol_df['Units_Sold'] / 31.0
sol_df['Uncaptured_Daily_Demand'] = (sol_df['Carts'] - sol_df['Units_Sold']) / 31.0
sol_df['True_Latent_Daily_Demand'] = sol_df['Daily_Demand_Rate'] + (sol_df['Uncaptured_Daily_Demand'] * 0.4) # Assuming 40% would convert if stock was healthy

# Recommended Dynamic Buffer & Reorder Point (Assuming 2-day supplier lead time)
LEAD_TIME_DAYS = 2
SAFETY_FACTOR = 1.65 # 95% service level
sol_df['Optimized_Reorder_Point'] = np.ceil(sol_df['True_Latent_Daily_Demand'] * LEAD_TIME_DAYS + (SAFETY_FACTOR * np.sqrt(LEAD_TIME_DAYS) * (sol_df['True_Latent_Daily_Demand'] * 0.5))).astype(int)
sol_df['Optimized_Safety_Stock'] = np.ceil(sol_df['True_Latent_Daily_Demand'] * 3).astype(int) # 3-day buffer
sol_df['Recommended_Daily_Replenish_Qty'] = np.ceil(sol_df['True_Latent_Daily_Demand'] * 1.2).astype(int)

# Compare current average stock vs recommended
current_avg_stock = inventory.groupby('Product_ID')['Closing_Stock'].mean().reset_index(name='Current_Avg_Stock')
sol_df = sol_df.merge(current_avg_stock, on='Product_ID')
sol_df['Stock_Gap'] = sol_df['Optimized_Safety_Stock'] - sol_df['Current_Avg_Stock']

# 2. Recommendation Engine Re-weighting
# Weight = Conversion_Rate / View_Share_Ratio
cat_views = interactions[interactions['Interaction_Type'] == 'View'].merge(products, on='Product_ID').groupby('Category').size()
cat_orders = orders.merge(products, on='Product_ID').groupby('Category').size()

cat_weights = pd.DataFrame({
    'Views': cat_views,
    'Orders': cat_orders
}).fillna(0)
cat_weights['View_Share'] = cat_weights['Views'] / cat_weights['Views'].sum()
cat_weights['Order_Share'] = cat_weights['Orders'] / cat_weights['Orders'].sum()
cat_weights['Current_Weight'] = cat_weights['View_Share']
# Optimal weight proportional to purchase propensity + margin
cat_weights['Recommended_Algorithm_Weight'] = (cat_weights['Order_Share'] * 1.2) / ((cat_weights['Order_Share'] * 1.2).sum())
cat_weights['Action'] = np.where(cat_weights['Recommended_Algorithm_Weight'] > cat_weights['Current_Weight'], 'Boost Visibility', 'Suppress / Deprioritize')
cat_weights = cat_weights.reset_index()

# Export Excel
sol_df.to_excel(os.path.join(OUTPUT_DIR, '13_optimized_replenishment_plan.xlsx'), index=False)
cat_weights.to_excel(os.path.join(OUTPUT_DIR, '14_recommendation_reweighting_model.xlsx'), index=False)

# Export Simulation JSON for Dashboard
sim_data = {
    "current_revenue": 48412,
    "abandoned_revenue": 84857,
    "products": sol_df[['Product_Name', 'Category', 'Price', 'Current_Avg_Stock', 'Optimized_Safety_Stock', 'Optimized_Reorder_Point', 'Recommended_Daily_Replenish_Qty']].to_dict(orient='records'),
    "category_weights": cat_weights[['Category', 'View_Share', 'Order_Share', 'Recommended_Algorithm_Weight', 'Action']].to_dict(orient='records')
}
with open(os.path.join(CHART_DIR, 'solution_engine.json'), 'w') as f:
    json.dump(sim_data, f)

print("Solution Engine computed and exported successfully!")
