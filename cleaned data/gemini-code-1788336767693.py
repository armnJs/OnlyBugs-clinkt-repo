# Check abandonment rate by category
cart_inv_cat = cart_inv.groupby(['Category', 'Ordered']).size().unstack(fill_value=0)
cart_inv_cat['Abandonment_Rate'] = cart_inv_cat[0] / (cart_inv_cat[0] + cart_inv_cat[1])
print("Abandonment by Category:\n", cart_inv_cat)

# Join with customers to see if segment matters
cart_cust = cart_inv.merge(customers, on='Customer_ID', how='left')
cart_cust_seg = cart_cust.groupby(['Customer_Segment', 'Ordered']).size().unstack(fill_value=0)
cart_cust_seg['Abandonment_Rate'] = cart_cust_seg[0] / (cart_cust_seg[0] + cart_cust_seg[1])
print("Abandonment by Segment:\n", cart_cust_seg)

# Are they missing out on revenue because of stockouts? 
# Wait, are there stockouts when they try to order? Out of stock is 7 times in abandoned carts, critical 46.
# What is the revenue lost?
abandoned_revenue = abandoned.merge(products, on='Product_ID')
print("Total Abandoned Revenue:", abandoned_revenue['Price'].sum())

# What is the average delivery time or is that not in the data? 
# The data doesn't have delivery times.

# Any other issues? Let's look at what the 10 min delivery industry failed at:
# High labour costs, rider strikes, 10 min pressure causing accidents, unit economics breaking down outside top cities.
# Zepto, Gorillas, Getir failed/struggled because of dense cities vs sparse, large baskets vs small, etc.