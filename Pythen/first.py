import sqlite3
import random
import datetime
from faker import Faker

# Initialize Faker
fake = Faker()

# Connect to SQLite database (or create it)
conn = sqlite3.connect('foodshop_ecommerce.db')
cursor = conn.cursor()

# Create tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL,
    category_id INTEGER,
    image_url TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT NOT NULL,
    status TEXT,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_person TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    supplier_id INTEGER,
    quantity INTEGER NOT NULL,
    last_restock_date TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
''')

# Populate categories
categories = [(fake.word(), fake.sentence()) for _ in range(10)]
cursor.executemany('INSERT INTO categories (name, description) VALUES (?, ?)', categories)

# Populate suppliers
suppliers = [(fake.company(), fake.name(), fake.phone_number(), fake.email(), fake.address(), fake.city(), fake.state(), fake.zipcode()) for _ in range(10)]
cursor.executemany('INSERT INTO suppliers (name, contact_person, phone, email, address, city, state, zip_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', suppliers)

# Populate products
products = [(fake.word(), fake.sentence(), round(random.uniform(5.0, 100.0), 2), random.randint(1, 100), random.randint(1, 10), fake.image_url()) for _ in range(100)]
cursor.executemany('INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) VALUES (?, ?, ?, ?, ?, ?)', products)

# Populate customers
customers = [(fake.first_name(), fake.last_name(), fake.email(), fake.phone_number(), fake.address(), fake.city(), fake.state(), fake.zipcode()) for _ in range(100)]
cursor.executemany('INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', customers)

# Populate orders
orders = [(random.randint(1, 100), fake.date_time_this_year().isoformat(), random.choice(['pending', 'completed', 'shipped']), round(random.uniform(20.0, 500.0), 2)) for _ in range(100)]
cursor.executemany('INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)', orders)

# Populate order items
order_items = [(random.randint(1, 100), random.randint(1, 100), random.randint(1, 10), round(random.uniform(5.0, 100.0), 2)) for _ in range(100)]
cursor.executemany('INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)', order_items)

# Populate inventory
inventory = [(random.randint(1, 100), random.randint(1, 10), random.randint(1, 100), fake.date_time_this_year().isoformat()) for _ in range(100)]
cursor.executemany('INSERT INTO inventory (product_id, supplier_id, quantity, last_restock_date) VALUES (?, ?, ?, ?)', inventory)

# Populate payments
payments = [(random.randint(1, 100), fake.date_time_this_year().isoformat(), round(random.uniform(20.0, 500.0), 2), random.choice(['credit_card', 'paypal', 'cash'])) for _ in range(100)]
cursor.executemany('INSERT INTO payments (order_id, payment_date, amount, payment_method) VALUES (?, ?, ?, ?)', payments)

# Commit and close
conn.commit()
conn.close()