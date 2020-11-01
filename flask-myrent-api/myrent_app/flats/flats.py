from flask import jsonify

from myrent_app import db
from myrent_app.flats import flats_bp
from myrent_app.models import Flat, FlatSchema, flat_schema
from myrent_app.utils import apply_order, apply_filter, get_pagination, validate_json_content_type, get_schema_args


@flats_bp.route('/flats', methods=['GET'])
def get_all_flats():
    query = Flat.query
    query = apply_order(Flat, query)
    query = apply_filter(Flat, query)
    items, pagination = get_pagination(query, 'flats.get_all_flats')
    
    schema_args = get_schema_args(Flat)
    flats = FlatSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': flats,
        'number_of_records': len(flats),
        'pagination': pagination
    })


@flats_bp.route('/flats/<int:flat_id>', methods=['GET'])
def get_one_flat(flat_id: str):

    return jsonify({
        'success': True,
        'data': f'Mieszkanie o id: {flat_id}'
    })


@flats_bp.route('/landlords/<int:landlord_identifier>/flats', methods=['GET'])
def get_all_landlord_flats(landlord_identifier: str):

    return jsonify({
        'success': True,
        'data': f'Wszystkie mieszkania właściciela: {landlord_identifier}'
    })


# landlord_token_required
@flats_bp.route('/landlords/<string:landlord_identifier>/flats', methods=['POST'])
def create_flat(landlord_identifier: str):

    return jsonify({
        'success': True,
        'data': f'create flat for landlord_identifier: {landlord_identifier}'
    })


# landlord_token_required
@flats_bp.route('/flats/<int:flat_id>', methods=['PUT'])
def update_flat(flat_id: str):

    return jsonify({
        'success': True,
        'data': f'Aktualizacja mieszkania o id: {flat_id}'
    })


# landlord_token_required
@flats_bp.route('/flats/<int:flat_id>', methods=['DELETE'])
def delete_flat(flat_id: str):

    return jsonify({
        'success': True,
        'data': f'Usunięcie mieszkania o id: {flat_id}'
    })
    