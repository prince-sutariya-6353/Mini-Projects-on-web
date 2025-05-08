from flask import Flask, render_template, request, redirect, url_for, Response
from pymongo import MongoClient
from urllib.parse import quote_plus
import csv
from io import StringIO
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# MongoDB Connection Setup using .env
username = os.getenv("MONGO_USERNAME")
password = quote_plus(os.getenv("MONGO_PASSWORD"))
cluster = os.getenv("MONGO_CLUSTER")
app_name = os.getenv("MONGO_APP_NAME")

MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName={app_name}"
try:
    client = MongoClient(MONGO_URI)
    client.server_info()  # Test connection
    print("Connected to MongoDB Atlas successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {e}")
    raise e

db = client["contacts_db"]
contacts_collection = db["contacts"]

@app.route('/')
def index():
    contacts = list(contacts_collection.find())
    print("Fetched contacts:", contacts)  # Debug line to verify data fetching
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    category = request.form.get('category', 'none')

    if name and phone and email:
        contacts_collection.insert_one({
            'name': name,
            'phone': phone,
            'email': email,
            'category': category
        })
        return redirect(url_for('index', added=True))
    else:
        return redirect(url_for('index', error=True))

@app.route('/update/<string:contact_id>', methods=['POST'])
def update_contact(contact_id):
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    category = request.form.get('category', 'none')

    if name and phone and email:
        contacts_collection.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {
                'name': name,
                'phone': phone,
                'email': email,
                'category': category
            }}
        )
        return redirect(url_for('index', updated=True))
    else:
        return redirect(url_for('index', error=True))

@app.route('/delete/<string:contact_id>')
def delete_contact(contact_id):
    contacts_collection.delete_one({'_id': ObjectId(contact_id)})
    return redirect(url_for('index', deleted=True))

@app.route('/export')
def export_contacts():
    contacts = list(contacts_collection.find())
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Name', 'Phone', 'Email', 'Category'])
    for c in contacts:
        cw.writerow([c['name'], c['phone'], c['email'], c.get('category', 'none')])
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=contacts.csv"}
    )

@app.route('/import', methods=['POST'])
def import_contacts():
    file = request.files.get('file')
    if file and file.filename.endswith('.csv'):
        content = file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(content))
        next(csv_data, None)  # Skip header
        imported = 0
        for row in csv_data:
            if len(row) >= 3:
                contacts_collection.insert_one({
                    'name': row[0],
                    'phone': row[1],
                    'email': row[2],
                    'category': row[3] if len(row) > 3 else 'none'
                })
                imported += 1
        return redirect(url_for('index', imported=imported))
    else:
        return redirect(url_for('index', error=True))

if __name__ == '__main__':
    app.run(debug=True)