import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import geopandas as gpd
import pycountry

# Connect to the SQLite database
conn = sqlite3.connect('sample.sqlite')

# Helper function to execute a query and return a DataFrame
def query_to_dataframe(query):
    return pd.read_sql_query(query, conn)

# Helper function to display table description in a pretty table
def display_table_description(table_name, description_df):
    table = PrettyTable()
    table.field_names = ["Column Name", "Type", "Nullable"]

    for _, row in description_df.iterrows():
        table.add_row([row['name'], row['type'], "YES" if row['notnull'] == 0 else "NO"])

    print(f"Description of {table_name} table:")
    print(table)

def convert_iso_alpha2_to_alpha3(alpha2_code):
    try:
        country = pycountry.countries.get(alpha_2=alpha2_code)
        return country.alpha_3 if country else None
    except LookupError:
        return None

def convert_iso_alpha2_to_country(alpha2_code):
    try:
        country = pycountry.countries.get(alpha_2=alpha2_code)
        return country.name if country else None
    except LookupError:
        return None

# Question 1: Give a short description of datasets
query1 = "PRAGMA table_info(account);"
description_account = query_to_dataframe(query1)
display_table_description("account", description_account)

query2 = "PRAGMA table_info(account_date_session);"
description_account_date_session = query_to_dataframe(query2)
display_table_description("account_date_session", description_account_date_session)

query3 = "PRAGMA table_info(iap_purchase);"
description_iap_purchase = query_to_dataframe(query3)
display_table_description("iap_purchase", description_iap_purchase)

print("Description of account table:")
print(description_account)
print("\nDescription of account_date_session table:")
print(description_account_date_session)
print("\nDescription of iap_purchase table:")
print(description_iap_purchase)

# Question 2: Analyze the daily active users
# Compare DAU changes over time
query_dau = "SELECT date, SUM(session_count) as total_sessions, SUM(session_duration_sec) as total_duration FROM account_date_session GROUP BY date;"
dau_data = query_to_dataframe(query_dau)
dau_data['date'] = pd.to_datetime(dau_data['date'])
dau_data.set_index('date', inplace=True)

# Plot DAU changes over time by session
plt.figure(figsize=(15, 6))
plt.plot(dau_data.index, dau_data['total_sessions'], marker='o', linestyle='-')
plt.title('Daily active users over time by sessions')
plt.xlabel('Date')
plt.ylabel('Total Sessions')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()


# Plot DAU changes over time by duration
plt.figure(figsize=(15, 6))
plt.plot(dau_data.index, dau_data['total_duration'], marker='o', linestyle='-')
plt.title('Daily active users over time by duration')
plt.xlabel('Date')
plt.ylabel('Total Sessions')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

# New Question: Visualize the Cumulative Sum of Created Accounts Over Time
query_created_accounts = "SELECT created_time, COUNT(account_id) as created_accounts FROM account GROUP BY created_time;"
created_accounts_data = query_to_dataframe(query_created_accounts)
created_accounts_data['created_time'] = pd.to_datetime(created_accounts_data['created_time'])

# Calculate the cumulative sum of created accounts
created_accounts_data['cumulative_created_accounts'] = created_accounts_data['created_accounts'].cumsum()

# Plot the cumulative sum of created accounts over time
plt.figure(figsize=(15, 6))
plt.plot(created_accounts_data['created_time'], created_accounts_data['cumulative_created_accounts'], marker='o', linestyle='-')
plt.title('Cumulative Sum of Created Accounts Over Time')
plt.xlabel('Date of Account Creation')
plt.ylabel('Cumulative Created Accounts')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

print("\nDescription of daily active users over time:")
print(created_accounts_data)

# Question 3: Analyze sales
# Analyze the geographic split of revenue and users
query_geo = "SELECT a.country_code, SUM(i.iap_price_usd_cents) as total_revenue, COUNT(DISTINCT i.account_id) as total_users FROM iap_purchase i LEFT JOIN account a ON i.account_id = a.account_id GROUP BY a.country_code;"
geo_data = query_to_dataframe(query_geo)

# Calculate average revenue per user per market
geo_data['avg_revenue_per_user'] = geo_data['total_revenue'] / geo_data['total_users']
geo_data['country'] = geo_data['country_code'].apply(convert_iso_alpha2_to_country)
# Display the geographic split of revenue and users
print("\nGeographic Split of Revenue and Users:")
print(geo_data.sort_values(by=['avg_revenue_per_user']))

# Plot average revenue per user per market
plt.figure(figsize=(10, 6))
plt.bar(geo_data['country_code'].astype(str), geo_data['avg_revenue_per_user'])
plt.title('Average Revenue per User per Market')
plt.xlabel('Country Code')
plt.ylabel('Average Revenue per User')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

# Plot revenue per market
plt.figure(figsize=(10, 6))
plt.bar(geo_data['country_code'].astype(str), geo_data['total_revenue'])
plt.title('Total Revenue per Market')
plt.xlabel('Country Code')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()


# Analyze the geographic split of revenue and users
query_geo = "SELECT a.country_code, AVG(i.iap_price_usd_cents) as avg_revenue_per_user FROM iap_purchase i LEFT JOIN account a ON i.account_id = a.account_id GROUP BY a.country_code;"
geo_data = query_to_dataframe(query_geo)
geo_data['country_code_iso3'] = geo_data['country_code'].apply(convert_iso_alpha2_to_alpha3)

# Load the world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the world map with the ARPU data
merged_data = world.merge(geo_data, left_on='iso_a3', right_on='country_code_iso3', how='left')
merged_data['avg_revenue_per_user'] = merged_data['avg_revenue_per_user'].fillna(0)

# Plot the choropleth map
fig, ax = plt.subplots(1, 1, figsize=(15, 8))
merged_data.plot(column='avg_revenue_per_user', cmap='YlGnBu', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
ax.set_title('Average Revenue Per User (ARPU) by Country')
ax.set_axis_off()  # Turn off the axis for better visualization
plt.show()

# Close the database connection
conn.close()
