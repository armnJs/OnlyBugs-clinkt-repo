print("Total Ordered Revenue:", orders['Total_Amount'].sum())

# Wait, what if we check time taken from "View" to "Add_to_Cart"?
print(interactions.head())
interactions['Timestamp'] = pd.to_datetime(interactions['Timestamp'])
# maybe there's high abandonment because they just don't checkout?

# What did quick commerce fail at?
# Based on the search:
# 1. High delivery cost per order vs low Average Order Value (AOV).
# 2. Safety and high attrition rate of drivers.
# 3. Breaking down in less dense cities.

print("Average Order Value (AOV) overall:", orders.groupby('Order_ID')['Total_Amount'].sum().mean())
print("AOV by segment:\n", orders.merge(customers, on='Customer_ID').groupby(['Order_ID', 'Customer_Segment'])['Total_Amount'].sum().groupby('Customer_Segment').mean())
print("Cities covered:\n", customers['City'].value_counts())