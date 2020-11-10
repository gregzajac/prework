from flask import jsonify
from myrent_app.agreements import agreements_bp

#landlord or tenant token
@agreements_bp.route('/agreements', methods=['GET'])
def get_agreements():
    return jsonify({
        'success': True,
        'data': 'Lista umow dla danego landlorda'
    })


#landlord or tenant token
@agreements_bp.route('/agreements/<int:agreement_id>', methods=['GET'])
def get_agreement(agreement_id: int):
    return jsonify({
        'success': True,
        'data': f'Umowa nr {agreement_id} dla danego landlorda'
    })


#landlord token
@agreements_bp.route('/agreements/<int:flat_id>/<int:tenant_id>', methods=['POST'])
def create_agreement(flat_id: int, tenant_id: int):
    return jsonify({
        'success': True,
        'data': f'Utwórz umowę dla flat id {flat_id} i tenant id {tenant_id}'
    })


#landlord token
@agreements_bp.route('/agreements/<int:agreement_id>', 
                    methods=['PUT'])
def update_agreement(agreement_id: int):
    return jsonify({
        'success': True,
        'data': f'Aktualizuj umowę dla agreement id {agreement_id}'
    })


#landlord token
@agreements_bp.route('/agreements/<int:agreement_id>', 
                    methods=['DELETE'])
def delete_agreement(agreement_id: int):
    return jsonify({
        'success': True,
        'data': f'Usuń umowę o id {agreement_id}'
    })
