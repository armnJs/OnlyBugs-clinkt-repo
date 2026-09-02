# Calculate out of stock rates
low_stock_days = inventory[inventory['Stock_Status'].isin(['Low Stock', 'Critical', 'Out of Stock'])]
print("Percentage of product-days in sub-optimal stock:", len(low_stock_days) / len(inventory))

print(inventory['Stock_Status'].value_counts())
# How many products face out of stock/critical stock often?
critical = inventory[inventory['Stock_Status'].isin(['Critical', 'Out of Stock'])].groupby('Product_Name').size().sort_values(ascending=False)
print("Most critically low products:\n", critical.head(10))

# What is the lost revenue due to abandonment? Rs 84,857 compared to Rs 48,412 ordered. That's a huge potential revenue loss.
# Is the abandonment driven by stock issues? 
print(abandoned.groupby('Stock_Status')['Price'].sum())