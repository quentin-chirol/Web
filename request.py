from flask import Flask, request, render_template, send_from_directory, jsonify
import openpyxl
import os 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def form():
    return render_template('index.html')

@app.route('/app')
def app_page():
    return render_template('app.html')

@app.route('/download')
def download_file():
    return send_from_directory('static/files', 'data.xlsx', as_attachment=True)

# Route for handling form submission
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
    
    file_path = os.path.join('static', 'files', 'data.xlsx')
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