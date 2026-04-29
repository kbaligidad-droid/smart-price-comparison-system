# Smart Price Comparison System 🛍️💰

A complete Flask-based Smart Price Comparison System with **Price Tracking**, **Price Drop Indicators**, **Best Deal Highlighting**, and **Price History Charts**.

## ✨ Key Features

### 1. **Price Drop Indicator** 📉
- Tracks `current_price` and `previous_price` for each store
- Displays price changes:
  - **"Price Dropped ₹X"** in green (savings!)
  - **"Price Increased ₹X"** in red (price rise)
  - **"No Change"** when price stays same
- Automatic history recording on every price update

### 2. **Best Deal Tag** 🎯
- Compares prices across **Flipkart, Amazon, Meesho**
- Highlights lowest price as "BEST DEAL"
- Shows savings compared to other platforms
- One-click access to the best store

### 3. **Price History Chart** 📊
- Interactive line chart using **Chart.js**
- Shows price trends over time
- Separate history tracking for each store
- View historical data for any product/store combination
- Visual trend analysis (price movements, peaks, valleys)

### 4. **Comparison Table** 📋
- Side-by-side price comparison from multiple platforms
- Current price + Previous price display
- Price change indicators
- Availability status
- Direct store links

### 5. **Admin Features** 🔧
- **Add/Edit/Delete Products**
- **Manage Store Prices** with automatic `current→previous` price migration
- **View Price History** for any product/store
- Product filtering and status management
- Trending product management

### 6. **User Features** 👤
- Browse products with price comparison
- Add products to cart
- View detailed product info with all store prices
- See price trends and history
- Get alerts on best deals

---

## 🗄️ Database Schema

### **Products Table**
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT,
    description TEXT,
    image_url TEXT,
    category_id INTEGER,
    rating REAL DEFAULT 4.0,
    is_trending BOOLEAN DEFAULT 0
);
```

### **Store Prices Table** (Price Tracking)
```sql
CREATE TABLE store_prices (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    store_name TEXT,
    current_price REAL,          -- Current price
    previous_price REAL DEFAULT 0, -- For drop detection
    store_link TEXT,
    availability TEXT,
    updated_at TIMESTAMP
);
```

### **Price History Table** (For Charts)
```sql
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    store_name TEXT,
    price REAL,
    recorded_date TIMESTAMP
);
```

---

## 🚀 Installation & Setup

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Run the Application**
```bash
python app.py
```

The app will start at: **http://127.0.0.1:5000**

### 3. **Initial Login**
- **Admin Credentials:**
  - Username: `admin`
  - Password: `admin123`

---

## 🎯 How to Use

### **For Users:**

1. **Browse Products**
   - Visit homepage to see trending products
   - Use search or category filters
   - Click on any product to see detailed comparison

2. **Compare Prices**
   - View all store prices in one table
   - See **Best Deal** highlighted in green
   - Check price drops/increases
   - Click "View Price History Chart" to see trends

3. **View Price Trends**
   - Select a store from dropdown
   - Chart displays 10-day price history
   - Hover over points for exact prices
   - Identify best time to buy

### **For Admin:**

1. **Add Products**
   - Go to: `/admin/add_product`
   - Enter product details (name, brand, description)
   - Add initial prices for Flipkart, Amazon, Meesho
   - Submit to create product

2. **Edit Prices**
   - Go to: `/admin/dashboard`
   - Click **"Prices"** button next to any product
   - Enter new prices for stores
   - Submit to update (current→previous automatic)
   - New prices auto-recorded in history

3. **View Price History**
   - Click **"History"** button next to product
   - See all past prices for that store
   - Track high/low prices
   - Analyze price trends

4. **Manage Products**
   - Delete products as needed
   - Mark as trending
   - Update descriptions/ratings

---

## 📊 User Interface Components

### **Home Page**
- Trending products carousel
- Category filters
- Search functionality
- Quick pricing overview

### **Product Detail Page**
- Product image and specifications
- Brand information
- Star ratings
- **Best Deal Alert** (prominent box)
- **Price Comparison Table** showing:
  - Store names
  - Current prices
  - Price changes (drop/increase)
  - Previous prices

### **Price Comparison Page**
- **Comparison Table** with all store prices
- **Interactive Chart** with price history
- Store selector dropdown
- Statistics (highest, lowest, latest prices)

### **Admin Dashboard**
- Product inventory table
- Quick actions (Edit, Delete, View History)
- Price overview with drop indicators
- Best price highlighting

---

## 🛠️ API Endpoints

### **Public Routes**
```
GET  /                      # Home page
GET  /dashboard             # Product search & browse
GET  /product/<id>          # Product details with comparison
GET  /compare/<id>          # Price history chart page
GET  /login                 # User login
GET  /register              # User registration
POST /login                 # Process login
POST /register              # Process registration
```

### **User Routes (Login Required)**
```
GET  /cart                  # View cart
GET  /add_to_cart/<id>      # Add product to cart
GET  /remove_from_cart/<id> # Remove from cart
```

### **Admin Routes (Admin Login Required)**
```
GET  /admin/login                    # Admin login page
GET  /admin/dashboard                # Admin dashboard
GET  /admin/add_product              # Add product form
POST /admin/add_product              # Process add product
GET  /admin/edit_prices/<product_id> # Edit prices form
POST /admin/edit_prices/<product_id> # Process price update
GET  /admin/delete_product/<id>      # Delete product
GET  /admin/price_history/<id>/<store> # View price history
```

### **API Routes (JSON)**
```
GET  /api/price-history/<product_id>/<store_name>  # Get price history data (for Chart.js)
```

---

## 💾 Sample Data

The system initializes with **sample products**:

| Product | Brand | Flipkart | Amazon | Meesho | Best Deal |
|---------|-------|----------|--------|--------|-----------|
| iPhone 15 | Apple | ₹50,000 | ₹51,000 | ₹49,000 | Meesho ✓ |
| Samsung S24 | Samsung | Price | Price | Price | ... |
| MacBook Air M3 | Apple | Price | Price | Price | ... |
| Sony WH-1000XM5 | Sony | Price | Price | Price | ... |

Sample price history is pre-populated for demonstration.

---

## 🎨 Styling & UI

- **Bootstrap 5** for responsive design
- **Chart.js** for interactive price charts
- **FontAwesome Icons** for visual elements
- **Custom CSS** with gradients and animations
- **Glass-morphism** effects for modern look
- Mobile-responsive layout

---

## 🔐 Security Features

- ✅ Password hashing with Werkzeug
- ✅ Strong password validation (8+ chars, letters + numbers)
- ✅ Session-based authentication
- ✅ Admin-only routes protection
- ✅ User login required for cart access

---

## 📱 Responsive Design

- Desktop: Full layout with sidebars
- Tablet: Optimized columns
- Mobile: Stacked layout with collapsible menus
- All tables are responsive with horizontal scroll

---

## 🐛 Troubleshooting

### Database Not Initializing?
```bash
python -c "import models; models.init_db()"
```

### Flask Not Starting?
```bash
# Check Python version (3.7+)
python --version

# Install all requirements
pip install -r requirements.txt --upgrade
```

### Chart Not Displaying?
- Ensure JavaScript is enabled
- Check browser console for errors
- Verify price history data exists

---

## 📈 Features Implemented

- ✅ Price tracking (current + previous)
- ✅ Price drop indicators
- ✅ Best deal highlighting
- ✅ Price history storage
- ✅ Interactive Chart.js visualization
- ✅ Admin price management
- ✅ Automatic price history recording
- ✅ Comparison table display
- ✅ User authentication
- ✅ Product search & filtering
- ✅ Responsive Bootstrap UI
- ✅ Price statistics (high/low/latest)

---

## 🎯 Future Enhancements

- Price alerts via email
- Wishlist functionality
- User reviews & ratings
- Advanced analytics dashboard
- Price prediction using trends
- Multiple currency support
- Real-time price updates

---

##  Screenshots 
- Home(https://github.com/kbaligidad-droid/smart-price-comparison-system/blob/main/Screenshot%202026-04-29%20200729.png?raw=true)
- Login(https://github.com/kbaligidad-droid/smart-price-comparison-system/blob/main/Screenshot%202026-04-29%20220734.png?raw=true)
- Comparison page(https://github.com/kbaligidad-droid/smart-price-comparison-system/blob/main/Screenshot%202026-04-29%20200814.png?raw=true)
- Admin Dashboard(https://github.com/kbaligidad-droid/smart-price-comparison-system/blob/main/Screenshot%202026-04-29%20201005.png?raw=true)
- Price history chart(

## 📝 File Structure

```
price_compare/
├── app.py                 # Main Flask application
├── models.py              # Database initialization
├── requirements.txt       # Python dependencies
├── database.db            # SQLite database
├── static/
│   ├── css/
│   │   └── style.css      # Custom styling
│   ├── js/
│   │   └── script.js      # JavaScript functionality
│   └── images/            # Product images
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Home page
    ├── product_detail.html # Product with comparison
    ├── price_comparison.html # Chart & history
    ├── dashboard.html     # Product browse
    ├── admin_dashboard.html # Admin panel
    ├── add_product.html   # Add product form
    ├── edit_prices.html   # Edit prices form
    ├── price_history.html # Price history view
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── cart.html          # Shopping cart
    └── ...other templates
```

---

## 📞 Support

For issues or questions, check:
1. Browser console for JavaScript errors
2. Flask terminal for server errors
3. Database file permissions
4. Port 5000 availability

---

## 📄 License

This project is open-source and free to use.

**Happy Shopping! 🛍️**
