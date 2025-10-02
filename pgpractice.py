import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="spaine", port=5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS products(
    id SERIAL PRIMARY KEY,
    name VARCHAR(250),
    price INT,
    category VARCHAR(255)
);
""")

cur.execute("""INSERT INTO products(id, name, price, category) VALUES
(1, 'chips', 3, 'f'),
(2, 'tooth brush', 2, 'h'),
(3, 'apple juice', 5, 'd')
ON CONFLICT (id) DO NOTHING;
""")

cur.execute("""CREATE TABLE IF NOT EXISTS customers(
    id SERIAL PRIMARY KEY,
    name VARCHAR(250),
    age INT,
    gender CHAR
);
""")

cur.execute("""INSERT INTO customers(id, name, age, gender) VALUES
(1, 'john', 30, 'm'),
(2, 'bob', 67, 'm'),
(3, 'veronica', 21, 'f')
ON CONFLICT (id) DO NOTHING;
""")

cur.execute("""CREATE TABLE IF NOT EXISTS orders(
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product_id INT REFERENCES products(id),
    quantity INT,
    price INT
);
""")

cur.execute("""INSERT INTO orders(id, customer_id, product_id, quantity, price) VALUES
(1, 1, 1, 1, 11),
(2, 1, 1, 1, 11),
(3, 3, 2, 1, 30),      
(4, 3, 2, 1, 30),
(5, 3, 3, 1, 3)
ON CONFLICT (id) DO NOTHING;
""")

#Each order references a customer and a product
#Customers can have multiple orders
#Products can appear in multiple orders

cur.execute("""SELECT products.name, SUM(orders.price)
FROM orders
JOIN products ON orders.product_id = products.id
GROUP BY products.name;
""")
print(cur.fetchall())

cur.execute("""SELECT name, age
FROM customers
WHERE age > (SELECT AVG(age) FROM customers);
""")
print(cur.fetchall())

cur.execute("""SELECT products.name,
(SELECT COUNT(*)
FROM orders
WHERE orders.product_id = products.id) AS order_count
FROM products;
""")
print(cur.fetchall())

cur.execute("""SELECT customers.name
FROM customers WHERE id IN (
            SELECT customer_id
            FROM orders
            WHERE product_id = 1
);
""")
print(f"people who bought chips: {cur.fetchall()}")

conn.commit()

conn.close()

cur.close()
