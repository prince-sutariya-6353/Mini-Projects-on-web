from flask import Flask, render_template, request, redirect, url_for, flash, Response
import os
import json
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_FILE = 'contacts.json'

def load_contacts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_contacts(contacts):
    with open(DATA_FILE, 'w') as f:
        json.dump(contacts, f, indent=4)

@app.route('/')
def index():
    contacts = load_contacts()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    contacts = load_contacts()
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    category = request.form.get('category', 'none')

    if name and phone and email:
        contacts.append({'name': name, 'phone': phone, 'email': email, 'category': category})
        save_contacts(contacts)
        flash('Contact added successfully.', 'success')
    else:
        flash('All fields are required.', 'danger')
    return redirect(url_for('index'))

@app.route('/update/<int:contact_id>', methods=['POST'])
def update_contact(contact_id):
    contacts = load_contacts()
    if 0 <= contact_id < len(contacts):
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        category = request.form.get('category', 'none')

        if name and phone and email:
            contacts[contact_id] = {
                'name': name,
                'phone': phone,
                'email': email,
                'category': category
            }
            save_contacts(contacts)
            flash('Contact updated successfully.', 'success')
        else:
            flash('All fields are required to update.', 'danger')
    return redirect(url_for('index'))

@app.route('/delete/<int:contact_id>')
def delete_contact(contact_id):
    contacts = load_contacts()
    if 0 <= contact_id < len(contacts):
        contacts.pop(contact_id)
        save_contacts(contacts)
        flash('Contact deleted.', 'warning')
    return redirect(url_for('index'))

@app.route('/export')
def export_contacts():
    contacts = load_contacts()
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
    contacts = load_contacts()
    file = request.files.get('file')

    if file and file.filename.endswith('.csv'):
        content = file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(content))
        next(csv_data, None)  # Skip header
        imported = 0
        for row in csv_data:
            if len(row) >= 3:
                contacts.append({
                    'name': row[0],
                    'phone': row[1],
                    'email': row[2],
                    'category': row[3] if len(row) > 3 else 'none'
                })
                imported += 1
        save_contacts(contacts)
        flash(f'{imported} contacts imported successfully.', 'success')
    else:
        flash('Invalid file or format.', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
