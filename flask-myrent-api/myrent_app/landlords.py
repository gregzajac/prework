from flask import jsonify, abort
from webargs.flaskparser import use_args
from myrent_app import app, db
from myrent_app.models import Landlord, LandlordSchema, landlord_schema, landlord_update_password_schema
from myrent_app.utils import validate_json_content_type, token_landlord_required


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


@app.route('/api/v1/landlords/register', methods=['POST'])
@validate_json_content_type
@use_args(landlord_schema, error_status_code=400)
def register(args: dict):
    if Landlord.query.filter(Landlord.identifier == args['identifier']).first():
        abort(409, description=f'Landlord with identifier {args["identifier"]} already exists')

    if Landlord.query.filter(Landlord.email == args['email']).first():
        abort(409, description=f'Landlord with email {args["email"]} already exists') 
    
    args['password'] = Landlord.generate_hashed_password(args['password'])
    
    new_landlord = Landlord(**args)
    db.session.add(new_landlord)
    db.session.commit()

    token = new_landlord.generate_jwt()

    return jsonify({
        'success': True,
        'token': token.decode()
    }), 201


@app.route('/api/v1/landlords/login', methods=['POST'])
@validate_json_content_type
@use_args(LandlordSchema(only=['identifier', 'password']), error_status_code=400)
def login(args: dict):
    landlord = Landlord.query.filter(Landlord.identifier == args['identifier']).first()

    if not landlord:
        abort(401, description='Invalid credentials')

    if not landlord.is_password_valid(args['password']):
        abort(401, description='Invalid credentials')

    token =landlord.generate_jwt()

    return jsonify({
        'success': True,
        'token': token.decode()
    })


@app.route('/api/v1/landlords/update/password', methods=['PUT'])
@validate_json_content_type
@token_landlord_required
@use_args(landlord_update_password_schema, error_status_code=400)
def update_landlord_password(identifier: str, args: dict):
    landlord = Landlord.query.filter(Landlord.identifier == identifier).first()

    if landlord is None:
        abort(404, description=f'Landlord with identifier {identifier} not found')

    if not landlord.is_password_valid(args['current_password']):
        abort(401, description='Invalid password')

    landlord.password = landlord.generate_hashed_password(args['new_password'])
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': landlord_schema.dump(landlord)
    })


@app.route('/api/v1/landlords/me', methods=['GET'])
@token_landlord_required
def get_current_landlord(identifier: str):
    landlord = Landlord.query.filter(Landlord.identifier == identifier).first()

    if landlord is None:
        abort(404, description=f'Landlord with identifier {identifier} not found')

    return jsonify({
        'success': True,
        'data': landlord_schema.dump(landlord)
    })    
 