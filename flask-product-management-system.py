from flask import Flask, request, redirect, url_for
import sqlite3
app = Flask(__name__)
# Database initialization
def init_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
# Create table if it doesn't exist 
    c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')
    conn.commit()
    conn.close()
    #  init when program starts
    init_db()
    # Home route
@app.route('/')
def home():
    return """<h1>Product Management System</h1>
<p><a href="/add_product">Add Product</a> | <a href="/view_products">View Products</a></p>"""
# Add product route
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        # simple validation
        if name == "" or price == "":
            return "please fill in all fields! <br><a href='/add_product'>Go back</a>"
# Insert product into database
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('view_products'))
    return """<h1>product added successfully!</h3><a href="/"> Add another product</a> | <a href="/view_products">View Products</a>"""
# HTML FORM (
    return """<h2>Add Product</h2>
<form method="post">
product name: <input type="text" name="name"><br>
price:<input type ="number"step="0.01" name="price"><br>
<button type="submit">Add Product</button>
</form>
<a href="/">Back to Home</a>"""
# view product route
@app.route('/products')
def view_products():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close() 
 # build HTML table 
    table = """ <h2>All product </h2>
    <table border = "1" cellpadding="8">
    <tr><th>ID</th><th>Name</th></tr>"""
    for p in products:
        table += f"""<tr><td>{p[0]}</td><td>{p[1]}</td></tr>{p[2]}</tr>"""
        table += """</table><br><a href="/">Back to Home</a> | <a href="/add_product">Add Product</a>"""
    return table
# debug mode
if __name__== '__main__':
    app.run(debug=True)