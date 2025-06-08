from flask import Blueprint, jsonify

auth = Blueprint('auth', __name__)

@auth.route('/auth/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login endpoint'})

@auth.route('/auth/register', methods=['POST'])
def register():
    return jsonify({'message': 'Register endpoint'}) 