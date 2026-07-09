import pandas as pd
import mysql.connector

# -------------------------------
# Step 1: Connect to MySQL
# -------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="xyz",  # your MySQL password
    database="olist_data"
)
cursor = conn.cursor()

# -------------------------------
# Step 2: Load CSV files
# -------------------------------
customers = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\olist_customers_dataset.csv")
geolocation = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\olist_geolocation_dataset.csv")
order_items = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\olist_order_items_dataset.csv")
order_payment = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\olist_order_payments_dataset.csv")
order_reviews = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\olist_order_reviews_dataset.csv")
orders = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\olist_orders_dataset.csv")
products = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\olist_products_dataset.csv")
sellers = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\olist_sellers_dataset.csv")
category_name = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\product_category_name_translation.csv")

# -------------------------------
# Step 3: Function to create table & insert in chunks
# -------------------------------
def load_to_mysql(df, table_name, chunk_size=10000):
    # Create table if not exists
    cols = ", ".join([f"`{col}` TEXT" for col in df.columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})")

    # Prepare insert query
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

    # Insert in chunks to avoid max_allowed_packet errors
    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start:start+chunk_size]
        data = [tuple(x) for x in chunk.values]
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Inserted rows {start} to {start + len(chunk) - 1} into '{table_name}'")

# -------------------------------
# Step 4: Load all Olist tables
# -------------------------------
load_to_mysql(customers, "customers")
load_to_mysql(geolocation, "geolocation")      # large table
load_to_mysql(order_items, "order_items")
load_to_mysql(order_payment, "order_payment")
load_to_mysql(order_reviews, "order_reviews")  # large table
load_to_mysql(orders, "orders")
load_to_mysql(products, "products")
load_to_mysql(sellers, "sellers")
load_to_mysql(category_name, "category_name")

# -------------------------------
# Step 5: Close Connection
# -------------------------------
cursor.close()
conn.close()
print("All database operations completed and connection closed.")
