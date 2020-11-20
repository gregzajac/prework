import os
from flask import jsonify, abort, current_app, send_file, request, url_for, \
                    render_template, redirect
from werkzeug.utils import secure_filename
from pathlib import Path

from myrent_app import db
from myrent_app.pictures import pictures_bp
from myrent_app.models import Picture, Flat, PictureSchema, picture_schema
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

    pictures = PictureSchema(many=True).dump(flat.pictures)

    return jsonify({
        'success': True,
        'data': pictures
    })


@pictures_bp.route('/pictures/<int:picture_id>', methods=['GET'])
def get_picture(picture_id: int):
    picture = Picture.query.get_or_404(picture_id, 
                description=f'Picture with id {picture_id} not found')

    return jsonify({
        'success': True,
        'data': picture_schema.dump(picture)
    })


#only landlord
@pictures_bp.route('/flats/<int:flat_id>/pictures', methods=['POST'])
def add_picture(flat_id: int):
    flat = Flat.query.get_or_404(flat_id, description=f'Flat with id {flat_id} not found')

    file = request.files['picture']
    description = request.form.get('description')

    if file.filename == '':
        abort(422, description=f'Picture is not attached')

    if not allowed_picture(file.filename):
        extensions = [e for e in current_app.config.get('ALLOWED_EXTENSIONS')]
        abort(422, description=f'Not allowed picture extension ({extensions})')

    picture_with_this_filename = Picture.query.filter(Picture.name == file.filename).first()
    if picture_with_this_filename is not None:
        abort(409, description=f'Picture with name {file.filename} already exists')

    filename = secure_filename(file.filename)
    target = current_app.config.get('UPLOAD_FOLDER') / filename

    picture = Picture(name=filename, path=str(target), flat_id=flat_id)    
    if description is not None:
        picture.description = description

    db.session.add(picture)
    db.session.commit()
    file.save(target)

    return jsonify({
        'success': True,
        'data': picture_schema.dump(picture)
    }), 201


#only landlord
@pictures_bp.route('/pictures/<int:picture_id>', methods=['DELETE'])
def delete_picture(picture_id: int):
    picture = Picture.query.get_or_404(picture_id, 
                                description=f'Picture with id {picture_id} not found')

    db.session.delete(picture)
    db.session.commit()

    if os.path.isfile(picture.path):
        os.remove(picture.path)

    return jsonify({
        'success': True,
        'data': f'Picture with id {picture_id} has been deleted'
    })