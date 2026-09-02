abandoned = abandoned.merge(products[['Product_ID', 'Price']], on='Product_ID', how='left')
print("Abandoned Revenue by Stock Status:\n", abandoned.groupby('Stock_Status')['Price'].sum())

# Wait, what if abandonment is due to high price or unit price?
# Let's check average price of abandoned vs ordered items
print("Avg price abandoned:", abandoned['Price'].mean())
print("Avg price ordered:", orders['Unit_Price'].mean())