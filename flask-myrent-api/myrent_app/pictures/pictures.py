from flask import jsonify, abort
from myrent_app import db
from myrent_app.pictures import pictures_bp
from myrent_app.models import Picture, Flat


@pictures_bp.route('/flats/<int:flat_id>/pictures', methods=['GET'])
def get_pictures(flat_id: int):
    # flat = Flat.query.get_or_404(flat_id, description=f'Flat with id {flat_id} not found')

    return jsonify({
        'success': True,
        'data': f'List of all pictures for flat id {flat_id}'
    })


@pictures_bp.route('/pictures/<int:picture_id>', methods=['GET'])
def get_picture(flat_id: int, picture_id: int):
    # flat = Flat.query.get_or_404(flat_id, description=f'Flat with id {flat_id} not found')

    return jsonify({
        'success': True,
        'data': f'Picture id {picture_id} details'
    })


#only landlord
@pictures_bp.route('/flats/<int:flat_id>/pictures', methods=['POST'])
def add_picture(flat_id: int):
    # flat = Flat.query.get_or_404(flat_id, description=f'Flat with id {flat_id} not found')

    return jsonify({
        'success': True,
        'data': f'Picture for flat {flat_id} has been added'
    }), 201


#only landlord
@pictures_bp.route('/pictures/<int:picture_id>', methods=['DELETE'])
def delete_picture(picture_id: int):
    # flat = Flat.query.get_or_404(flat_id, description=f'Flat with id {flat_id} not found')

    return jsonify({
        'success': True,
        'data': f'Picture with id {picture_id} has been deleted'
    })