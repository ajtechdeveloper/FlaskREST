from flask import Flask, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'python':
        return 'flask'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

employees = [
    {
        'id': 1,
        'name': 'Jane',
        'department': 'Technology',
        'salary': 20000
    },
    {
        'id': 2,
        'name': 'John',
        'department': 'HR',
        'salary': 15000
    }
]
    
@app.route('/employee', methods = ['GET'])
@auth.login_required
def get_employees():
    return jsonify({ 'employees': employees})

@app.route('/employee/<int:id>', methods = ['GET'])
@auth.login_required
def get_employee(id):
    employee = [employee for employee in employees if employee['id'] == id]
    if len(employee) == 0:
        abort(404)
    return jsonify( { 'employee': employee[0] } )

@app.route('/employee', methods = ['POST'])
@auth.login_required
def create_employee():
    if not request.json or not 'name' in request.json:
        abort(400)
    employee = {
        'id': employees[-1]['id'] + 1,
        'name': request.json['name'],
        'department': request.json.get('department', ""),
        'salary': request.json['salary']
    }
    employees.append(employee)
    return jsonify( { 'employee': employee } ), 201

@app.route('/employee/<int:id>', methods = ['PUT'])
@auth.login_required
def update_employee(id):
    employee = [employee for employee in employees if employee['id'] == id]
    if len(employee) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    if 'department' in request.json and type(request.json['department']) is not str:
        abort(400)
    if 'salary' in request.json and type(request.json['salary']) is not int:
        abort(400)
    employee[0]['name'] = request.json.get('name', employee[0]['name'])
    employee[0]['department'] = request.json.get('department', employee[0]['department'])
    employee[0]['salary'] = request.json.get('salary', employee[0]['salary'])
    return jsonify( { 'employee': employee[0] } )
    
@app.route('/employee/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_employee(id):
    employee = [employee for employee in employees if employee['id'] == id]
    if len(employee) == 0:
        abort(404)
    employees.remove(employee[0])
    return jsonify( { 'status': 'success' } )
    
if __name__ == '__main__':
    app.run(debug = True)