
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Atlas setup
client = MongoClient('mongodb+srv://1:1@cluster0.gwaownt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['recharge_db']
users_collection = db['users']
orders_collection = db['orders']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({'name': name, 'password': hashed_password})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = users_collection.find_one({'name': name})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            return redirect(url_for('my_orders'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/recharge', methods=['POST'])
def recharge():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    operator = request.form['operator']
    circle = request.form['circle']
    mobile = request.form['mobile']
    amount = request.form['amount']
    payment_method = request.form['payment_method']
    order_id = orders_collection.insert_one({
        'user_id': ObjectId(user_id),
        'operator': operator,
        'circle': circle,
        'mobile': mobile,
        'amount': amount,
        'payment_method': payment_method,
        'status': 'Pending'
    }).inserted_id

    return redirect(url_for('order_success', order_id=order_id))

@app.route('/order_success/<order_id>')
def order_success(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    order = orders_collection.find_one({'_id': ObjectId(order_id)})
    return render_template('order_success.html', order=order)

@app.route('/my_orders')
def my_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    orders = orders_collection.find({'user_id': ObjectId(user_id)})
    return render_template('my_orders.html', orders=orders)

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    orders = orders_collection.find()
    users = users_collection.find()
    return render_template('admin.html', orders=orders, users=users)

@app.route('/update_status/<order_id>', methods=['POST'])
def update_status(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    status = request.form['status']
    payment_received = request.form.get('payment_received') == 'on'
    orders_collection.update_one({'_id': ObjectId(order_id)}, {'$set': {'status': status, 'payment_received': payment_received}})
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
