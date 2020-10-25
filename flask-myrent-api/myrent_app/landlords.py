from flask import jsonify
from myrent_app import app


@app.route('/api/v1/landlords', methods=['GET'])
def get_all_landlords():
    return jsonify({
        'success': True,
        'data': 'all users'
    })


@app.route('/api/v1/landlords/<int:landlord_id>', methods=['GET'])
def get_one_landlord(landlord_id: int):
    return jsonify({
        'success': True,
        'data': f'one user with id {landlord_id}'
    })


@app.route('/api/v1/landlords', methods=['POST'])
def create_landlord():
    return jsonify({
        'success': True,
        'data': f'create new landlord'
    })


@app.route('/api/v1/landlords/<int:landlord_id>', methods=['PUT'])
def update_landlord_password(landlord_id: int):
    return jsonify({
        'success': True,
        'data': f'update user with id {landlord_id}'
    })


@app.route('/api/v1/landlords/<int:landlord_id>', methods=['DELETE'])
def delete_landlord(landlord_id: int):
    return jsonify({
        'success': True,
        'data': f'delete user with id {landlord_id}'
    })
