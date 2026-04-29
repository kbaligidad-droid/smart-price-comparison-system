import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('✅ DATABASE TABLES:')
for table in tables:
    print(f'   - {table[0]}')

# Check products
cursor.execute('SELECT COUNT(*) FROM products')
print(f'\n✅ PRODUCTS: {cursor.fetchone()[0]} products loaded')

# Check store prices
cursor.execute('SELECT COUNT(*) FROM store_prices')
print(f'✅ STORE PRICES: {cursor.fetchone()[0]} price records')

# Check price history
cursor.execute('SELECT COUNT(*) FROM price_history')
print(f'✅ PRICE HISTORY: {cursor.fetchone()[0]} history records')

# Sample price tracking
cursor.execute('''
SELECT p.name, sp.store_name, sp.current_price, sp.previous_price
FROM products p
JOIN store_prices sp ON p.id = sp.product_id
LIMIT 3
''')
print('\n✅ SAMPLE PRICE TRACKING:')
for row in cursor.fetchall():
    name, store, curr, prev = row
    print(f'   {name} @ {store}: Current=₹{curr}, Previous=₹{prev}')

conn.close()
print('\n🎉 Database initialized successfully with price tracking!')
