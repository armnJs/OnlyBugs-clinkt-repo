aov_city = orders.merge(customers, on='Customer_ID').groupby(['Order_ID', 'City'])['Total_Amount'].sum().groupby('City').mean()
print("AOV by City:\n", aov_city)

print("Orders count by city:\n", orders.merge(customers, on='Customer_ID').groupby('City')['Order_ID'].nunique())