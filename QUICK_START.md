# 🚀 Quick Start Guide

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Run the Application
```bash
python app.py
```

You'll see:
```
✅ Database Initialized with Price Tracking & History Features!
 * Running on http://127.0.0.1:5000
```

## Step 3: Open in Browser
Visit: **http://127.0.0.1:5000**

---

## 👤 User Account (Testing)

### Create New Account:
1. Click **"Register"** on homepage
2. Enter username, email, password
3. Password must have: 8+ characters, letters + numbers
4. Login and explore!

### Test Credentials:
- Email: `test@example.com`
- Password: `test123456`

---

## 🔑 Admin Account

### Login:
- URL: `http://127.0.0.1:5000/admin/login`
- Username: **admin**
- Password: **admin123**

### What You Can Do:
1. **Add Products** - Add new products with prices
2. **Edit Prices** - Update store prices (auto-tracks history)
3. **View History** - See price trends for each store
4. **Delete Products** - Remove products

---

## 🛍️ User Features

### 1. **Browse Products**
- Go to "All Products" or search
- Click on any product

### 2. **View Comparison**
- See prices from all stores
- **Green badge** = Best deal
- **Red arrows** = Price increased
- **Green arrows** = Price dropped

### 3. **See Price Trends**
- Click "View Price History Chart"
- Select store from dropdown
- See 10-day price movement chart

### 4. **Add to Cart**
- Click "Add to Cart" button
- View cart to see items

---

## 📊 Sample Data Included

✅ 4 sample products with prices
✅ 3 stores (Flipkart, Amazon, Meesho)
✅ 10 days of price history
✅ Price drop examples

---

## 🎯 Key Pages

| Page | URL | What You See |
|------|-----|--------------|
| Home | `/` | Trending products |
| Browse | `/dashboard` | All products |
| Product | `/product/1` | Prices & comparison |
| Comparison | `/compare/1` | Chart & history |
| Admin Panel | `/admin/dashboard` | Manage products |
| Add Product | `/admin/add_product` | Create new product |
| Edit Prices | `/admin/edit_prices/1` | Update prices |
| Price History | `/admin/price_history/1/Flipkart` | View trends |

---

## ⚡ Try This First

1. **Login as Admin**
   - Go to: `/admin/login`
   - Username: `admin`, Password: `admin123`

2. **Edit a Product Price**
   - Click on "iPhone 15" row
   - Click "Prices" button
   - Change Flipkart price to something different
   - Submit (notice automatic tracking!)

3. **View History**
   - Click "History" button
   - See price changes recorded

4. **Logout & Login as User**
   - Click product link
   - View comparison table
   - Check price change badge
   - Click "View Price History Chart"
   - See the chart with your price update!

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Port 5000 already in use | Change port: `app.run(debug=True, port=5001)` |
| Database locked | Delete `database.db` and restart |
| Chart not showing | Ensure JavaScript is enabled |
| Admin login fails | Use: admin / admin123 |

---

## 💡 Pro Tips

✅ Each price update automatically creates history entry
✅ Best deal is always highlighted green
✅ Price drops shown in green, increases in red
✅ Charts show 10-day trends
✅ Previous price helps track savings

---

## 📚 What's New (Price Comparison Features)

### Price Drop Indicator
```
Flipkart: ₹50,000 → ₹49,500 = ✅ Price Dropped ₹500
Amazon:   ₹51,000 → ₹52,000 = ❌ Price Increased ₹1,000
```

### Best Deal Tag
```
🎯 BEST DEAL at Flipkart - ₹49,500 (Save ₹2,500)
```

### Price History Chart
```
Interactive line graph showing:
- X-axis: Dates (10 days)
- Y-axis: Prices (₹)
- Tooltip: Hover for exact price
```

### Admin Price Management
```
Update → Current becomes Previous → History recorded → Chart updated
```

---

## 🎉 Features Summary

| Feature | Status |
|---------|--------|
| Price Drop Indicator | ✅ Live |
| Best Deal Tag | ✅ Live |
| Price History Chart | ✅ Live |
| Comparison Table | ✅ Live |
| Admin Price Management | ✅ Live |
| Automatic History Tracking | ✅ Live |
| Responsive UI | ✅ Live |
| Bootstrap Cards | ✅ Live |
| Chart.js Integration | ✅ Live |

---

**Ready to go! 🚀**

Need help? Check README.md for detailed documentation.
