import json
from flask import jsonify, abort, current_app, \
                request, render_template, redirect, url_for
from myrent_app import db
from myrent_app.pictures import pictures_bp
from myrent_app.models import Picture, Flat
from myrent_app.utils import allowed_picture


@pictures_bp.route('/', methods=['GET', 'POST'])
def upload_test_file():
    if request.method == 'POST':
        # file = request.files['file']
        # return redirect(url_for('pictures.add_picture', flat_id=1))
        print('post method')
    return render_template('index.html')



@pictures_bp.route('/flats/<int:flat_id>/pictures', methods=['GET'])
def get_pictures(flat_id: int):
    flat = Flat.query.get_or_404(flat_id, description=f'Flat with id {flat_id} not found')
    pictures = flat.pictures
    print(pictures)
    all_pictures = [p for p in pictures]
    return jsonify({
        'success': True,
        'data': f'List of all pictures for flat id {flat_id} - {all_pictures}'
    })


@pictures_bp.route('/pictures/<int:picture_id>', methods=['GET'])
def get_picture(picture_id: int):
    # flat = Flat.query.get_or_404(flat_id, description=f'Flat with id {flat_id} not found')

    return jsonify({
        'success': True,
        'data': f'Picture id {picture_id} details'
    })


#only landlord
@pictures_bp.route('/flats/<int:flat_id>/pictures', methods=['POST'])
def add_picture(flat_id: int):
    flat = Flat.query.get_or_404(flat_id, description=f'Flat with id {flat_id} not found')
    file = request.files['picture']

    if file.filename == '':
        abort(422, description=f'Picture is not attached')

    if not allowed_picture(file.filename):
        extensions = [e for e in current_app.config.get('ALLOWED_PICTURE_EXTENSIONS')]
        abort(422, description=f'Not allowed picture extension ({extensions})')

    picture = Picture(name=file.filename, data=file.read(), flat_id=flat_id)

    description = request.form.get('description')
    if description is not None:
        picture.description = description

    # print(picture.data)
    # print(len(picture.data))
    
    db.session.add(picture)
    db.session.commit()

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