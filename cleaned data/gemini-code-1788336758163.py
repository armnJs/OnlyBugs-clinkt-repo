import os
import pandas as pd
import glob

print("Files in working dir:", os.listdir('.'))

files = ['customer_interactions.csv', 'customers.csv', 'inventory.csv', 'orders.csv', 'products.csv']
for f in files:
    if os.path.exists(f):
        df = pd.read_csv(f)
        print(f"--- {f} ---")
        print("Shape:", df.shape)
        print("Columns & Types:\n", df.dtypes)
        print("Missing values:\n", df.isnull().sum())
        print("Head:\n", df.head(3))
        print("\n")