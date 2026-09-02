# Family segment cart contents
fam_carts = cart_cust[cart_cust['Customer_Segment'] == 'Family']
print("Family Segment Product Categories:\n", fam_carts['Category'].value_counts())

# What about total amount / cart size?
cart_sizes = cart_cust.groupby(['Session_ID', 'Customer_Segment'])['Product_ID'].count().reset_index()
print("Average items added to cart per session by segment:\n", cart_sizes.groupby('Customer_Segment')['Product_ID'].mean())

# Order cart sizes
order_sizes = orders.merge(customers, on='Customer_ID', how='left').groupby(['Order_ID', 'Customer_Segment'])['Quantity'].sum().reset_index()
print("Average items actually ordered per session by segment:\n", order_sizes.groupby('Customer_Segment')['Quantity'].mean())