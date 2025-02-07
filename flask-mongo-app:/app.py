from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# MongoDB URI (make sure this is correct)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"

# Initialize PyMongo
mongo = PyMongo(app)

# Test MongoDB connection
try:
    mongo.cx.server_info()  # This will raise an exception if the connection fails
    print("MongoDB connection successful!")
except ConnectionFailure:
    print("MongoDB connection failed. Please check your MongoDB server.")

# Home Route: Displays Insert Data Form
@app.route('/')
def index():
    return render_template('index.html')

# Route to Insert Data (Insert Form)
@app.route('/insert_page')
def insert_page():
    return render_template('insert.html')

# Route to Handle Insert Data
@app.route('/insert', methods=['POST'])
def insert_data():
    name = request.form.get('name')
    age = request.form.get('age')
    dob = request.form.get('dob')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip')
    occupation = request.form.get('occupation')
    marital_status = request.form.get('marital_status')
    wife_name = request.form.get('wife_name') if marital_status == "Married" else None

    # Create a dictionary with all the data
    user_data = {
        "name": name,
        "age": age,
        "dob": dob,
        "email": email,
        "phone": phone,
        "address": address,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "occupation": occupation,
        "marital_status": marital_status,
        "wife_name": wife_name
    }

    # Insert data into MongoDB collection
    collection = mongo.db.mycollection
    collection.insert_one(user_data)

    return redirect(url_for('view_data'))  # Redirect to view data page after insertion

# Route to Display All Data from MongoDB
@app.route('/view')
def view_data():
    collection = mongo.db.mycollection
    data = collection.find()  # Retrieve all documents from the collection
    return render_template('view.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
