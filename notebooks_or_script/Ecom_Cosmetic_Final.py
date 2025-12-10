"""

Project: E-commerce Cosmetics Revenue & Profit Analysis
Author: Tyler Dawson
Tech: Python (Pandas, Matplotlib, Seaborn)

Goal:
- Analyze sales & profitability by category, subcategory, product and customer.
- Understand discount impact and identify under-performing products.

"""

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sb

df = pd.read_excel("Ecom_Cosmetic.xlsx")


print(df)

df.columns


subcategory_profit = df.groupby('Subcategory')['Profit'].sum().sort_values(ascending=False).reset_index()

avg_profit_per_order = (df.groupby('Subcategory').agg({'Profit': 'sum', 'Order ID': pd.Series.nunique}).assign(AvgProfitPerOrder=lambda x: x['Profit'] / x['Order ID']).sort_values(by='AvgProfitPerOrder', ascending=False))

product_profit = (df.groupby(['Subcategory','Product'])['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False))

product_profit = df.groupby('Product')['Profit'].sum().sort_values(ascending=False).reset_index()

df['Product'].nunique()

top20_products = product_profit.head(20)

top220_products = product_profit.head(220)


product_profit = (df.groupby('Product')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False).reset_index(drop=True))

product_profit['Group'] = (product_profit.index // 250) + 1

group_profit = (product_profit.groupby('Group')['Profit'].sum().reset_index().sort_values(by='Group'))

print(group_profit)

total_profit = group_profit['Profit'].sum()
group_profit['% of Total Profit'] = (group_profit['Profit'] / total_profit * 100).round(2)

print(group_profit)

print(subcategory_profit)

print(avg_profit_per_order)

print(top20_products)

print(product_profit)

product_subcat_counts = df.groupby('Product')['Subcategory'].nunique()

print(product_subcat_counts)


discount_impact = df.groupby('Subcategory')[['Discount', 'Profit']].mean().sort_values(by='Discount', ascending=False)
print(discount_impact)


negative_products = (df.groupby('Product')['Profit'].sum().reset_index().query('Profit < 0').sort_values(by='Profit'))

print(negative_products.head(10))



sb.set(style="whitegrid")

plt.figure(figsize=(10, 6))
sb.barplot(data=subcategory_profit, x='Profit', y='Subcategory', palette='viridis')

plt.title('Total Profit by Subcategory')
plt.xlabel('Total Profit')
plt.ylabel('Subcategory')
plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 7))
sb.barplot(data=top20_products, x='Profit', y='Product', palette='magma')

plt.title('Top 20 Products by Profit')
plt.xlabel('Total Profit')
plt.ylabel('Product')
plt.tight_layout()
plt.show()



plt.figure(figsize=(12,7))
sb.scatterplot(data=top220_products, x='Profit', y='Product', color='skyblue', s=100)

plt.title('Top 220 Products by profit')
plt.xlabel('Total Profit')
plt.ylabel('Product')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,6))
sb.barplot(data=group_profit, x='Group', y='Profit', palette='coolwarm')
plt.title('Total Profit by Product Group (Every 250 Products)')
plt.xlabel('Product Group')
plt.ylabel('Total Profit')
plt.tight_layout()
plt.show()


df.sort_values('Order Date', ascending=False)


country_profit = (df.groupby('Country')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False))

print(country_profit.head(10))


top10_countries = country_profit.head(10)

plt.figure(figsize=(10, 6))
sb.barplot(data=top10_countries, x='Profit', y='Country', palette='coolwarm')

plt.title('Top 10 Countries by Profit')
plt.xlabel('Total Profit')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

country_sales = (df.groupby('Country')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False))

orders_per_country = (df.groupby('Country')['Order ID'].nunique().reset_index().sort_values(by='Order ID', ascending=False))
top10_order_per_country = orders_per_country.head(10)



df_country_metrics = (country_profit.merge(country_sales, on='Country').merge(orders_per_country, on='Country'))

df_country_metrics['AvgOrderValue'] = df_country_metrics['Sales'] / df_country_metrics['Order ID']
df_country_metrics['AvgProfitPerOrder'] = df_country_metrics['Profit'] / df_country_metrics['Order ID']

'''
top_orders = df_country_metrics.sort_values(by='Order ID', ascending=False).head(10)

plt.figure(figsize=(10,6))
sb.barplot(data=top_orders, x='Order ID', y='Country', palette='Blues')
plt.title('Top 10 Countries by Number of Orders')
plt.xlabel('Number of Orders')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

print(top_orders)
'''


print(orders_per_country.head(10))

plt.figure(figsize=(10,6))
sb.barplot(data=top10_order_per_country, x='Order ID', y='Country', palette='Blues')
plt.title('Top 10 Countries by Number of Orders')
plt.xlabel('Number of Orders')
plt.ylabel('Country')
plt.tight_layout()
plt.show()


top_avg_profit = df_country_metrics.sort_values(by='AvgProfitPerOrder', ascending=False).head(10)

plt.figure(figsize=(10,6))
sb.barplot(data=top_avg_profit, x='AvgProfitPerOrder', y='Country', palette='Greens')
plt.title('Top 10 Countries by Avg Profit per Order')
plt.xlabel('Avg Profit per Order ($)')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12,7))
sb.scatterplot(data=df_country_metrics, x='Order ID', y='AvgProfitPerOrder', color='skyblue', s=100)

plt.title('Orders vs. Avg Profit per Order (by Country)')
plt.xlabel('Number of Orders')
plt.ylabel('Avg Profit per Order ($)')
plt.tight_layout()
plt.show()

top_countries = df_country_metrics.sort_values(by='Order ID', ascending=False).head(30)

plt.figure(figsize=(10, 6))
sb.scatterplot(data=top_countries, x='Order ID', y='AvgProfitPerOrder', s=100)

plt.title('Top 30 Countries: Orders vs. Avg Profit per Order')
plt.xlabel('Number of Orders')
plt.ylabel('Avg Profit per Order ($)')
plt.tight_layout()
plt.show()


df['Order Date'] = pd.to_datetime(df['Order Date'])


df['Month'] = df['Order Date'].dt.to_period('M')

df['Year'] = df['Order Date'].dt.to_period('Y')

yearly_metrics = df.groupby('Year')[['Sales','Profit']].sum().reset_index()
print(yearly_metrics)

orders_per_year =df.groupby('Year')['Order ID'].nunique().reset_index()

customers_per_year = df.groupby('Year')['Customer ID'].nunique().reset_index()

monthly_metrics = df.groupby('Month')[['Sales', 'Profit']].sum().reset_index()
print(monthly_metrics)

monthly_metrics = monthly_metrics.sort_values(by='Month')
print(monthly_metrics)

orders_per_month = df.groupby('Month')['Order ID'].nunique().reset_index()

customers_per_month = df.groupby('Month')['Customer ID'].nunique().reset_index()

monthly_metrics['Month'] = monthly_metrics['Month'].dt.to_timestamp()

plt.figure(figsize=(12, 6))
plt.plot(monthly_metrics['Month'], monthly_metrics['Sales'], label='Sales', marker='o')
plt.plot(monthly_metrics['Month'], monthly_metrics['Profit'], label='Profit', marker='o')

plt.title('Monthly Sales and Profit Trend')
plt.xlabel('Month')
plt.ylabel('Amount ($)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

segment_profit = (df.groupby('Segment')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False))

df.groupby('Segment')['Order ID'].nunique()

segment_profit = (df.groupby('Segment')['Profit'].sum().reset_index())

orders_per_segment = (df.groupby('Segment')['Order ID'].nunique().reset_index())

df_segment_metrics = segment_profit.merge(orders_per_segment, on='Segment')
df_segment_metrics['AvgProfitPerOrder'] = df_segment_metrics['Profit'] / df_segment_metrics['Order ID']

print(df_segment_metrics)

print(segment_profit)

plt.figure(figsize=(12, 8))
sb.barplot(data=segment_profit, x='Profit', y='Segment', palette='pastel')

plt.title('Profit by Customer Segment')
plt.xlabel('Total Profit ($)')
plt.ylabel('Segment')
plt.tight_layout()
plt.show()

df['Sales'].sum()
df['Profit'].sum()
df['Order ID'].nunique()
df['Customer ID'].nunique()
df['Order Date'].min(), df['Order Date'].max()







