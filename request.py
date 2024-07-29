from flask import Flask, request, jsonify
from flask_cors import CORS
import openpyxl

app = Flask(__name__)
CORS(app)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    nom = request.form.get('nom')
    email = request.form.get('email')
    adresse = request.form.get('adresse')
    phone = request.form.get('phone')

    if not all([name, nom, email, adresse, phone]):
        return jsonify({'message': 'All fields are required!'}), 400

    data = {
        'name': name,
        'email': email,
        'nom': nom,
        'adresse': adresse,
        'phone': phone
    }
    
    file_path = 'data.xlsx'
    try:
        workbook = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.append(['Name', 'Email', 'Nom', 'Adresse', 'Phone'])
    else:
        worksheet = workbook.active

    new_row = [data["name"], data['email'], data['nom'], data['adresse'], data['phone']]
    worksheet.append(new_row)
    workbook.save(file_path)
    
    return jsonify({'message': 'Data saved successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
