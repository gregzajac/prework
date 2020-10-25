from flask import jsonify, abort
from webargs.flaskparser import use_args
from myrent_app import app, db
from myrent_app.models import Landlord, LandlordSchema, landlord_schema, landlord_update_password_schema


@app.route('/api/v1/landlords', methods=['GET'])
def get_all_landlords():
    data = Landlord.query.all()
    landlord_schema = LandlordSchema(many=True)

    return jsonify({
        'success': True,
        'data': landlord_schema.dump(data)
    })


@app.route('/api/v1/landlords/<int:landlord_id>', methods=['GET'])
def get_one_landlord(landlord_id: int):
    landlord = Landlord.query.get_or_404(landlord_id, description=f'Landlord with id {landlord_id} not found')

    return jsonify({
        'success': True,
        'data': landlord_schema.dump(landlord)
    })


@app.route('/api/v1/landlords', methods=['POST'])
@use_args(landlord_schema)
def create_landlord(args: dict):
    landlord = Landlord(**args)
    db.session.add(landlord)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'create new landlord'
    })


@app.route('/api/v1/landlords/<int:landlord_id>', methods=['PUT'])
@use_args(landlord_update_password_schema)
def update_landlord_password(args: dict, landlord_id: int):
    landlord = Landlord.query.get_or_404(landlord_id, description=f'Landlord with id {landlord_id} not found')

    if not landlord.is_password_valid(args['current_password']):
        abort(401, description='Invalid password')

    landlord.password = args['new_password']
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': f'update user with id {landlord_id}'
    })


@app.route('/api/v1/landlords/<int:landlord_id>', methods=['DELETE'])
def delete_landlord(landlord_id: int):
    landlord = Landlord.query.get_or_404(landlord_id, description=f'Landlord with id {landlord_id} not found')
    db.session.delete(landlord)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'delete user with id {landlord_id}'
    })

