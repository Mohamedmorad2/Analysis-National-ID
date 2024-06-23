from flask import Flask, request, jsonify, render_template
from datetime import date

app = Flask(__name__)

Governorate_code = [
    '1', '2', '3', '4', '11', '12', '13', '14', '15', '16', '17', '18', '19',
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '31', '32', '33', '34', '35', '88'
]

Governorate_code_values = {
    1: 'Cairo', 
    2: 'Alexandria',
    3: 'Port Said', 
    4: 'Suez', 
    11: 'Damietta', 
    12: 'Dakahlia', 
    13: 'Eastern', 
    14: 'Qalyubia', 
    15: 'Kafr El-Sheikh', 
    16: 'Western', 
    17: 'Menoufia', 
    18: 'Behera', 
    19: 'Ismailia', 
    21: 'Giza', 
    22: 'Beni-Suef', 
    23: 'Fayoum', 
    24: 'Menia', 
    25: 'Asyout', 
    26: 'Suhag', 
    27: 'Qena', 
    28: 'Aswan', 
    29: 'Luxor', 
    31: 'Red Sea', 
    32: 'ElWadi ElGidid', 
    33: 'Matrouh', 
    34: 'North Sinai', 
    35: 'South Sinai', 
    88: 'Outside the Republic'
}

def validate_national_id(national_id):
    national_id = national_id.replace(" ", "")
    
    if not national_id.isdigit():
        return False, "Invalid input. Please enter digits only."
    
    if len(national_id) != 14:
        return False, "Invalid National ID number: Not 14 digits."
    
    if national_id[0] not in ['2', '3']:
        return False, "Invalid National ID number: Incorrect format for date of birth."
    
    if national_id[7:9] not in Governorate_code:
        return False, "Invalid National ID number: Incorrect Governorate code."
    
    return True, "National ID is valid."

def analysis_national_id(national_id):
    birth_year = int(national_id[1:3])
    birth_month = int(national_id[3:5])
    birth_day = int(national_id[5:7])

    if national_id[0] == '3':  # If the first digit is 3, it's in the 2000s
        birth_year += 2000
    else:  # Otherwise, it's in the 1900s
        birth_year += 1900

    today = date.today()
    age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))

    Governorate_code_value = int(national_id[7:9])
    Governorate = Governorate_code_values.get(Governorate_code_value, "Unknown")
    
    Gender = int(national_id[-2])
    Gender = "Male" if Gender % 2 == 1 else "Female"

    return {
        "birthYear": birth_year,
        "birthMonth": birth_month,
        "birthDay": birth_day,
        "age": age,
        "gender": Gender,
        "governorate": Governorate
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    national_id = data.get('nationalId')
    
    is_valid, message = validate_national_id(national_id)
    if is_valid:
        analysis_data = analysis_national_id(national_id)
        return jsonify({
            'valid': True,
            **analysis_data
        })
    else:
        return jsonify({
            'valid': False,
            'message': message
        })

if __name__ == '__main__':
    app.run(debug=True)
