import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Sample dataset
data = {
    "InvoiceNo": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015],
    "StockCode": ["A101", "A102", "B101", "B102", "C101", "A101", "A103", "B101", "C102", "D101", "A102", "B103", "C103", "D102", "E101"],
    "Description": ["Widget", "Gadget", "Thingamajig", "Doohickey", "Contraption", "Widget", "Doodad", "Thingamajig", "Whatchamacallit", "Gizmo", "Gadget", "Whatsit", "Doohickey", "Gadgetizer", "Thingummy"],
    "Quantity": [10, 5, 2, 7, 3, 12, 8, 6, 3, 15, 4, 9, 11, 7, 2],
    "InvoiceDate": ["2024-01-15", "2024-02-20", "2024-03-05", "2024-04-10", "2024-05-25", "2024-06-15", "2024-07-20", "2024-08-05", "2024-09-10", "2024-10-25", "2024-01-20", "2024-02-25", "2024-03-10", "2024-04-15", "2024-05-30"],
    "UnitPrice": [9.99, 15.99, 7.49, 20.00, 12.50, 9.99, 13.49, 7.49, 10.00, 19.99, 15.99, 8.99, 22.50, 18.75, 6.99],
    "CustomerID": [12345, 12346, 12347, 12348, 12349, 12345, 12350, 12347, 12351, 12352, 12346, 12353, 12354, 12348, 12355],
    "Country": ["USA", "Canada", "UK", "Germany", "France", "USA", "Australia", "UK", "Italy", "Spain", "Canada", "Netherlands", "Brazil", "Germany", "Mexico"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("ecommerce_data.csv", index=False)

print("CSV file 'ecommerce_data.csv' created successfully.")

# Load the dataset
df = pd.read_csv("ecommerce_data.csv")

# Data Cleaning
df.drop_duplicates(inplace=True)
df.dropna(subset=['CustomerID'], inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Calculating Total Sales
df['TotalSales'] = df['Quantity'] * df['UnitPrice']

# Monthly Sales Trend
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
monthly_sales = df.groupby(['Year', 'Month'])['TotalSales'].sum().reset_index()
pivot_sales = monthly_sales.pivot(index='Month', columns='Year', values='TotalSales')

# Customer Revenue Calculation
customer_revenue = df.groupby('CustomerID')['TotalSales'].sum().reset_index()
customer_revenue['SpendingCategory'] = pd.cut(customer_revenue['TotalSales'], bins=[0, 500, 1000, 5000, np.inf], labels=['Low', 'Medium', 'High', 'Premium'])

# Top Products
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

# Visualization
plt.figure(figsize=(12, 6))
sns.lineplot(data=pivot_sales, markers=True)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.grid(True)
plt.legend(title="Year")
plt.show()

# Bar Chart for Customer Spending
plt.figure(figsize=(10, 6))
customer_revenue['SpendingCategory'].value_counts().plot(kind='bar', color='skyblue')
plt.title("Customer Spending Categories")
plt.xlabel("Spending Category")
plt.ylabel("Count of Customers")
plt.show()

# Top Products Visualization
plt.figure(figsize=(10, 6))
top_products.plot(kind='bar', color='orange')
plt.title("Top 10 Most Frequently Purchased Products")
plt.xlabel("Product")
plt.ylabel("Quantity Purchased")
plt.show()

print("E-commerce Data Analysis Completed Successfully.")
