import sqlite3
import datetime
from werkzeug.security import generate_password_hash

DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 1. USERS TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    );
    ''')

    # 2. CATEGORIES TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        icon TEXT
    );
    ''')

    # 3. PRODUCTS TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        brand TEXT DEFAULT 'Generic',
        description TEXT,
        image_url TEXT,
        category_id INTEGER,
        rating REAL DEFAULT 4.0,
        is_trending BOOLEAN DEFAULT 0,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    );
    ''')

    # 4. STORE PRICES TABLE (WITH CURRENT AND PREVIOUS PRICE TRACKING)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS store_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        store_name TEXT NOT NULL,
        current_price REAL,
        previous_price REAL DEFAULT 0,
        store_link TEXT,
        availability TEXT DEFAULT 'In Stock',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id)
    );
    ''')

    # 5. PRICE HISTORY TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        store_name TEXT NOT NULL,
        price REAL NOT NULL,
        recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id)
    );
    ''')

    # 6. ORDERS TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        mobile TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        pincode TEXT NOT NULL,
        total_price REAL NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    ''')

    # CLEAR OLD DATA (ONLY FOR TESTING)
    cursor.execute('DELETE FROM price_history')
    cursor.execute('DELETE FROM store_prices')
    cursor.execute('DELETE FROM products')
    cursor.execute('DELETE FROM categories')

    # INSERT CATEGORIES
    categories = [
        ("Mobiles", "fa-mobile-alt"),
        ("Laptops", "fa-laptop"),
        ("Fashion", "fa-tshirt"),
        ("Electronics", "fa-plug"),
        ("Shoes", "fa-shoe-prints"),
        ("Watches", "fa-clock"),
        ("Home Appliances", "fa-blender"),
        ("Kitchen", "fa-utensils"),
        ("Books", "fa-book"),
        ("Gaming", "fa-gamepad"),
        ("Sports", "fa-football-ball"),
        ("Beauty", "fa-spa"),
        ("Furniture", "fa-couch")
    ]
    cursor.executemany('INSERT INTO categories (name, icon) VALUES (?, ?)', categories)

    # GET CATEGORY IDs
    cursor.execute('SELECT id, name FROM categories')
    cat_map = {name: id for id, name in cursor.fetchall()}

    # SAMPLE PRODUCTS
    products_data = [
        ("iPhone 15", "Apple", "Latest flagship with A17 Pro chip", "https://images.unsplash.com/photo-1551163813-2f1b4d2e40f7?auto=format&fit=crop&w=800&q=80", "Mobiles", 4.8, 1, 99999),
        ("Samsung Galaxy S24", "Samsung", "Premium smartphone with AI camera", "https://images.unsplash.com/photo-1523473827532-0e7d2e5e5f7b?auto=format&fit=crop&w=800&q=80", "Mobiles", 4.7, 1, 83999),
        ("OnePlus 12", "OnePlus", "Fast performance and clean OxygenOS", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80", "Mobiles", 4.6, 0, 44999),
        ("Xiaomi Redmi Note 13", "Xiaomi", "Affordable 5G smartphone with long battery", "https://images.unsplash.com/photo-1542751110-97427bbecf20?auto=format&fit=crop&w=800&q=80", "Mobiles", 4.4, 0, 16999),
        ("Google Pixel 8", "Google", "Pure Android phone with excellent camera", "https://images.unsplash.com/photo-1532705829623-fba12c273989?auto=format&fit=crop&w=800&q=80", "Mobiles", 4.7, 0, 59999),
        ("Poco F6", "Poco", "Value flagship with strong battery life", "https://images.unsplash.com/photo-1598032895326-62288c9bcc09?auto=format&fit=crop&w=800&q=80", "Mobiles", 4.5, 0, 27999),
        ("MacBook Air M3", "Apple", "M3 chip laptop for professionals", "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80", "Laptops", 4.9, 1, 124999),
        ("Dell XPS 15", "Dell", "Slim laptop with OLED display", "https://source.unsplash.com/featured/?dell+laptop", "Laptops", 4.7, 0, 114999),
        ("HP Pavilion 15", "HP", "Everyday laptop with strong battery life", "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80", "Laptops", 4.5, 0, 57999),
        ("ASUS ROG Strix", "ASUS", "Gaming laptop with high refresh-rate screen", "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80", "Laptops", 4.6, 1, 189999),
        ("Lenovo ThinkPad X1", "Lenovo", "Business laptop with durable chassis", "https://images.unsplash.com/photo-1504274066651-8d31a536b11a?auto=format&fit=crop&w=800&q=80", "Laptops", 4.8, 0, 139999),
        ("Sony WH-1000XM5", "Sony", "Wireless noise-cancelling headphones", "https://images.unsplash.com/photo-1512314889357-e157c22f938d?auto=format&fit=crop&w=800&q=80", "Electronics", 4.8, 1, 24999),
        ("Bose SoundLink Revolve", "Bose", "Portable Bluetooth speaker with 360° sound", "https://source.unsplash.com/featured/?portable+speaker", "Electronics", 4.6, 0, 17999),
        ("Kindle Paperwhite", "Amazon", "Waterproof e-reader with built-in light", "https://source.unsplash.com/featured/?kindle", "Electronics", 4.7, 0, 12999),
        ("DJI Mini 4 Pro", "DJI", "Compact drone with 4K camera", "https://images.unsplash.com/photo-1519183071298-a2962cc1bb25?auto=format&fit=crop&w=800&q=80", "Electronics", 4.7, 0, 56999),
        ("Samsung Frame TV", "Samsung", "Smart TV with art mode and 4K color", "https://images.unsplash.com/photo-1553456558-aff63285bdd4?auto=format&fit=crop&w=800&q=80", "Electronics", 4.8, 0, 89999),
        ("JBL Flip 6", "JBL", "Rugged Bluetooth speaker with punchy bass", "https://source.unsplash.com/featured/?bluetooth+speaker", "Electronics", 4.5, 0, 9999),
        ("Nike Air Max 270", "Nike", "Comfortable sneakers with air cushioning", "https://images.unsplash.com/photo-1528701800489-20b1f5a129-1?auto=format&fit=crop&w=800&q=80", "Shoes", 4.6, 0, 10999),
        ("Adidas Ultraboost", "Adidas", "Responsive running shoes with energy return", "https://images.unsplash.com/photo-1503596470-1d20c8c67f81?auto=format&fit=crop&w=800&q=80", "Shoes", 4.8, 1, 15999),
        ("Skechers GOwalk", "Skechers", "Lightweight walking shoes for all-day comfort", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80", "Shoes", 4.5, 0, 4499),
        ("New Balance 574", "New Balance", "Classic sneakers with retro style", "https://images.unsplash.com/photo-1516920630294-1bbd5b5e1419?auto=format&fit=crop&w=800&q=80", "Shoes", 4.4, 0, 7499),
        ("Puma RS-X", "Puma", "Modern sports shoes with bold design", "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80", "Shoes", 4.3, 0, 8999),
        ("Reebok Classic", "Reebok", "Timeless sneaker for everyday style", "https://images.unsplash.com/photo-1519741491600-27f1b6a945f6?auto=format&fit=crop&w=800&q=80", "Shoes", 4.4, 0, 6999),
        ("Ray-Ban Wayfarer", "Ray-Ban", "Iconic sunglasses with timeless design", "https://images.unsplash.com/photo-1536291962884-5cb8ebaa6bd1?auto=format&fit=crop&w=800&q=80", "Fashion", 4.7, 1, 5999),
        ("Levi's 501 Jeans", "Levi's", "Classic straight-fit denim jeans", "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=800&q=80", "Fashion", 4.5, 0, 4999),
        ("Zara Denim Jacket", "Zara", "Casual denim jacket for everyday wear", "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=800&q=80", "Fashion", 4.4, 0, 5999),
        ("H&M Cotton Shirt", "H&M", "Soft cotton shirt for daily wear", "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80", "Fashion", 4.2, 0, 1799),
        ("Gucci Leather Belt", "Gucci", "Premium leather belt with signature buckle", "https://images.unsplash.com/photo-1495121605193-b116b5b9c5d4?auto=format&fit=crop&w=800&q=80", "Fashion", 4.6, 0, 12999),
        ("Apple Watch Series 9", "Apple", "Smartwatch with health monitoring and GPS", "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?auto=format&fit=crop&w=800&q=80", "Watches", 4.9, 1, 29999),
        ("Fossil Gen 6", "Fossil", "Stylish smartwatch with fitness tracking", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80", "Watches", 4.5, 0, 17999),
        ("Samsung Galaxy Watch 6", "Samsung", "Premium wearable with AMOLED display", "https://images.unsplash.com/photo-1557180295-76eee20ae8aa?auto=format&fit=crop&w=800&q=80", "Watches", 4.6, 0, 21999),
        ("Garmin Forerunner 265", "Garmin", "Advanced running watch with GPS", "https://images.unsplash.com/photo-1502415398388-9e22f5372cd1?auto=format&fit=crop&w=800&q=80", "Watches", 4.7, 0, 24999),
        ("Philips Air Fryer", "Philips", "Healthy frying with fast air circulation", "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80", "Home Appliances", 4.5, 0, 9999),
        ("LG Refrigerator", "LG", "Smart inverter refrigerator with fresh cooling", "https://images.unsplash.com/photo-1599058917763-1ec9e957a8d0?auto=format&fit=crop&w=800&q=80", "Home Appliances", 4.7, 0, 45999),
        ("Bosch Washing Machine", "Bosch", "Front-load washing machine with quick wash", "https://images.unsplash.com/photo-1577032225875-ada185b8c037?auto=format&fit=crop&w=800&q=80", "Home Appliances", 4.6, 0, 38999),
        ("Dyson V12 Vacuum", "Dyson", "Cordless vacuum with high suction power", "https://source.unsplash.com/featured/?vacuum+cleaner", "Home Appliances", 4.8, 1, 44999),
        ("IFB Microwave Oven", "IFB", "Convection microwave for modern kitchens", "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=800&q=80", "Home Appliances", 4.4, 0, 12999),
        ("Mi Air Purifier", "Mi", "Compact air purifier with smart control", "https://images.unsplash.com/photo-1577623372987-bfd428d1f68b?auto=format&fit=crop&w=800&q=80", "Home Appliances", 4.3, 0, 9999),
        ("Prestige Pressure Cooker", "Prestige", "Durable pressure cooker for home cooking", "https://images.unsplash.com/photo-1525301897439-8d6c6b5a2704?auto=format&fit=crop&w=800&q=80", "Kitchen", 4.5, 0, 3999),
        ("Tefal Nonstick Pan Set", "Tefal", "Premium cookware with long-lasting nonstick", "https://images.unsplash.com/photo-1517673132405-8158a72e8c2e?auto=format&fit=crop&w=800&q=80", "Kitchen", 4.4, 0, 6499),
        ("KitchenAid Mixer", "KitchenAid", "Stand mixer for baking and cooking", "https://images.unsplash.com/photo-1511688878355-1f7203e9e1f9?auto=format&fit=crop&w=800&q=80", "Kitchen", 4.8, 1, 27999),
        ("NutriBullet Blender", "NutriBullet", "High-speed blender for smoothies", "https://images.unsplash.com/photo-1586201375761-83865001e16d?auto=format&fit=crop&w=800&q=80", "Kitchen", 4.6, 0, 7499),
        ("Havells Electric Kettle", "Havells", "Fast boiling kettle with safety features", "https://images.unsplash.com/photo-1511381939415-dfa7df31fc83?auto=format&fit=crop&w=800&q=80", "Kitchen", 4.4, 0, 2499),
        ("Atomic Habits", "Book", "Bestselling self-improvement guide", "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=800&q=80", "Books", 4.8, 0, 449),
        ("The Alchemist", "Book", "Inspirational novel by Paulo Coelho", "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=800&q=80", "Books", 4.7, 0, 399),
        ("Educated", "Book", "Memoir by Tara Westover", "https://images.unsplash.com/photo-1496104679561-38d05c7308d2?auto=format&fit=crop&w=800&q=80", "Books", 4.6, 0, 499),
        ("Rich Dad Poor Dad", "Book", "Classic personal finance book", "https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=800&q=80", "Books", 4.5, 0, 399),
        ("PlayStation 5", "Sony", "Latest console for gaming and entertainment", "https://images.unsplash.com/photo-1606813902542-1d5a94b50b24?auto=format&fit=crop&w=800&q=80", "Gaming", 4.9, 1, 49999),
        ("Xbox Series X", "Microsoft", "Powerful console with 4K gaming", "https://source.unsplash.com/featured/?xbox+series+x", "Gaming", 4.8, 0, 49999),
        ("Nintendo Switch", "Nintendo", "Portable hybrid gaming console", "https://images.unsplash.com/photo-1541508183-7ecfadc156f1?auto=format&fit=crop&w=800&q=80", "Gaming", 4.7, 0, 34999),
        ("Razer DeathAdder V2", "Razer", "Gaming mouse with optical sensor", "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=800&q=80", "Gaming", 4.6, 0, 6999),
        ("Logitech G502", "Logitech", "Programmable mouse with tunable weight", "https://source.unsplash.com/featured/?gaming+mouse", "Gaming", 4.5, 0, 6499),
        ("Corsair K70 Keyboard", "Corsair", "Gaming keyboard with RGB lighting", "https://source.unsplash.com/featured/?mechanical+keyboard", "Gaming", 4.6, 0, 12999),
        ("Decathlon Football", "Nike", "Durable match football for training", "https://images.unsplash.com/photo-1521412644187-c49fa049e84d?auto=format&fit=crop&w=800&q=80", "Sports", 4.5, 0, 1499),
        ("Puma Cricket Bat", "Puma", "Lightweight bat for performance", "https://images.unsplash.com/photo-1509223197845-458d87318791?auto=format&fit=crop&w=800&q=80", "Sports", 4.4, 0, 7499),
        ("Yonex Badminton Racket", "Yonex", "High-tension racket for control", "https://images.unsplash.com/photo-1508609349937-5ec4ae374ebf?auto=format&fit=crop&w=800&q=80", "Sports", 4.6, 0, 3999),
        ("Adidas Fitness Band", "Adidas", "Monitors activity and heart rate", "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80", "Sports", 4.5, 0, 2999),
        ("Reebok Yoga Mat", "Reebok", "Non-slip mat for studio workouts", "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=800&q=80", "Sports", 4.4, 0, 1499),
        ("L'Oreal Revitalift Serum", "L'Oreal", "Anti-aging serum for smoother skin", "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=800&q=80", "Beauty", 4.7, 0, 1299),
        ("Maybelline Fit Me Foundation", "Maybelline", "Buildable foundation with natural finish", "https://images.unsplash.com/photo-1507572503492-6c11bddcd779?auto=format&fit=crop&w=800&q=80", "Beauty", 4.5, 0, 699),
        ("Neutrogena Sunscreen", "Neutrogena", "Broad spectrum SPF protection", "https://source.unsplash.com/featured/?sunscreen", "Beauty", 4.6, 0, 899),
        ("Lakme Lipstick", "Lakme", "Long-lasting colour for every occasion", "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?auto=format&fit=crop&w=800&q=80", "Beauty", 4.4, 0, 499),
        ("IKEA Study Table", "IKEA", "Minimal study desk with storage", "https://images.unsplash.com/photo-1493666438817-866a91353ca9?auto=format&fit=crop&w=800&q=80", "Furniture", 4.5, 0, 15999),
        ("Urban Ladder Sofa", "Urban Ladder", "Comfortable sofa with premium upholstery", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80", "Furniture", 4.7, 0, 44999),
        ("Home Centre Dining Set", "Home Centre", "Dining table set for 4 with modern design", "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=800&q=80", "Furniture", 4.6, 0, 32999),
        ("Wakefit Mattress", "Wakefit", "Comfort foam mattress for restful sleep", "https://source.unsplash.com/featured/?mattress", "Furniture", 4.5, 0, 12999),
        ("Nilkamal Storage Unit", "Nilkamal", "Durable storage organizer for home", "https://source.unsplash.com/featured/?storage+unit", "Furniture", 4.4, 0, 7999),
        ("Pepperfry Wardrobe", "Pepperfry", "Spacious wardrobe with sleek finish", "https://source.unsplash.com/featured/?wardrobe", "Furniture", 4.3, 0, 29999),
        ("AmazonBasics TV Unit", "AmazonBasics", "Modern TV console with storage", "https://source.unsplash.com/featured/?tv+unit", "Furniture", 4.2, 0, 8999),
        ("Godrej Office Chair", "Godrej", "Ergonomic chair for home office comfort", "https://source.unsplash.com/featured/?office+chair", "Furniture", 4.5, 0, 8999)
    ]

    for name, brand, desc, img, cat_name, rate, trend, base_price in products_data:
        cursor.execute('''
        INSERT INTO products (name, brand, description, image_url, category_id, rating, is_trending)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, brand, desc, img, cat_map[cat_name], rate, trend))

        pid = cursor.lastrowid
        query_name = name.replace(' ', '+')
        price = int(base_price)

        stores = [
            ("Flipkart", price, int(price * 1.04), f"https://www.flipkart.com/search?q={query_name}"),
            ("Amazon", int(price * 1.02), int(price * 1.05), f"https://www.amazon.in/s?k={query_name}&ref=nb_sb_noss"),
            ("Meesho", int(price * 0.97), int(price * 0.99), f"https://www.meesho.com/search?q={query_name}")
        ]

        if cat_name == 'Books':
            stores = [
                ("Flipkart", int(price * 1.00), int(price * 1.05), f"https://www.flipkart.com/search?q={query_name}"),
                ("Amazon", int(price * 0.98), int(price * 1.02), f"https://www.amazon.in/s?k={query_name}&ref=nb_sb_noss"),
                ("Meesho", int(price * 0.95), int(price * 0.97), f"https://www.meesho.com/search?q={query_name}")
            ]
        elif cat_name == 'Kitchen':
            stores = [
                ("Flipkart", price, int(price * 1.06), f"https://www.flipkart.com/search?q={query_name}"),
                ("Amazon", int(price * 1.03), int(price * 1.04), f"https://www.amazon.in/s?k={query_name}&ref=nb_sb_noss"),
                ("Meesho", int(price * 0.95), int(price * 0.98), f"https://www.meesho.com/search?q={query_name}")
            ]
        elif cat_name == 'Sports':
            stores = [
                ("Flipkart", price, int(price * 1.05), f"https://www.flipkart.com/search?q={query_name}"),
                ("Amazon", int(price * 1.02), int(price * 1.04), f"https://www.amazon.in/s?k={query_name}&ref=nb_sb_noss"),
                ("Meesho", int(price * 0.96), int(price * 0.97), f"https://www.meesho.com/search?q={query_name}")
            ]
        elif cat_name == 'Beauty':
            stores = [
                ("Flipkart", price, int(price * 1.05), f"https://www.flipkart.com/search?q={query_name}"),
                ("Amazon", int(price * 1.01), int(price * 1.03), f"https://www.amazon.in/s?k={query_name}&ref=nb_sb_noss"),
                ("Meesho", int(price * 0.93), int(price * 0.96), f"https://www.meesho.com/search?q={query_name}")
            ]
        elif cat_name == 'Furniture':
            stores = [
                ("Flipkart", price, int(price * 1.07), f"https://www.flipkart.com/search?q={query_name}"),
                ("Amazon", int(price * 1.04), int(price * 1.06), f"https://www.amazon.in/s?k={query_name}&ref=nb_sb_noss"),
                ("Meesho", int(price * 0.95), int(price * 0.98), f"https://www.meesho.com/search?q={query_name}")
            ]

        for s_name, curr_price, prev_price, s_link in stores:
            cursor.execute('''
            INSERT INTO store_prices (product_id, store_name, current_price, previous_price, store_link)
            VALUES (?, ?, ?, ?, ?)
            ''', (pid, s_name, curr_price, prev_price, s_link))

    # ADD PRICE HISTORY FOR EVERY PRODUCT
    cursor.execute('SELECT id FROM products')
    all_products = cursor.fetchall()
    history_rows = []
    for product_row in all_products:
        pid = product_row[0]
        for store_name in ['Flipkart', 'Amazon', 'Meesho']:
            price_row = cursor.execute(
                'SELECT current_price, previous_price FROM store_prices WHERE product_id = ? AND store_name = ?',
                (pid, store_name)
            ).fetchone()
            if not price_row:
                continue
            current_price, previous_price = price_row
            if previous_price is None:
                previous_price = current_price
            diff = current_price - previous_price
            for index, days_ago in enumerate([20, 15, 10, 5, 0]):
                price_value = int(previous_price + diff * ((index + 1) / 5.0))
                history_rows.append((pid, store_name, price_value, datetime.date.today() - datetime.timedelta(days=days_ago)))
    cursor.executemany('''
        INSERT INTO price_history (product_id, store_name, price, recorded_date)
        VALUES (?, ?, ?, ?)
    ''', history_rows)

    # ADMIN USER
    admin_pass = generate_password_hash('admin123')

    cursor.execute('''
    INSERT OR IGNORE INTO users (username, email, password, is_admin)
    VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@gmail.com', admin_pass, 1))

    conn.commit()
    conn.close()

    print("✅ Database Initialized with Price Tracking & History Features!")



if __name__ == '__main__':
    init_db()
