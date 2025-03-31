import csv
import psycopg2

DB_NAME = "AXION_DB"
DB_USER = "AXION_USER"
DB_PASS = "PASSWORD123"
DB_HOST = "localhost"
DB_PORT = "5434"

conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
)
cursor = conn.cursor()


def insert_csv(csv_file, table_name, columns):
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            placeholders = ",".join(["%s"] * len(columns))
            query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
            values = [row[col] for col in columns]
            cursor.execute(query, values)

    print(f"OK - Insertados datos de {csv_file} en {table_name}")


# 1) USERS
insert_csv(
    csv_file="users.csv",
    table_name="users_user",
    columns=[
        "user_id",
        "username",
        "full_name",
        "email",
        "password",
        "address",
        "role",
    ],
)

# 2) CATEGORIES
insert_csv(
    csv_file="categories.csv",
    table_name="products_category",
    columns=["category_id", "name"],
)

# 3) PRODUCTS
insert_csv(
    csv_file="products.csv",
    table_name="products_product",
    columns=[
        "product_id",
        "name",
        "category_id",
        "description",
        "price",
        "stock",
        "series",
    ],
)

# 4) ATTRIBUTES
insert_csv(
    csv_file="attributes.csv",
    table_name="products_attribute",
    columns=["attribute_id", "name"],
)

# 5) PRODUCT ATTRIBUTES
insert_csv(
    csv_file="product_attributes.csv",
    table_name="products_productattribute",
    columns=["product_attribute_id", "product_id", "attribute_id", "value"],
)

# 6) CART ITEM
insert_csv(
    csv_file="cart_item.csv",
    table_name="cart_cartitem",
    columns=["cart_item_id", "cart_id", "product_id", "quantity", "price", "subtotal"],
)

# 7) CART
insert_csv(
    csv_file="cart.csv",
    table_name="cart_cart",
    columns=["cart_id", "customer_id"],
)

# 8) ORDER ITEM
insert_csv(
    csv_file="order_item.csv",
    table_name="orders_orderitem",
    columns=[
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "price",
        "subtotal",
    ],
)

# 9) ORDERS
insert_csv(
    csv_file="orders.csv",
    table_name="orders_order",
    columns=["order_id", "customer_id", "order_date", "status"],
)


# 10) SHIPMENTS
insert_csv(
    csv_file="shipments.csv",
    table_name="orders_shipment",
    columns=["shipment_id", "order_id", "shipment_date"],
)

conn.commit()
cursor.close()
conn.close()

print("Carga de CSV finalizada con éxito.")
