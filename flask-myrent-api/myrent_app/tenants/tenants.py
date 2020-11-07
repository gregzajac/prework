from flask import jsonify
from myrent_app.tenants import tenants_bp
from myrent_app.utils import token_landlord_required
from myrent_app.models import Tenant, TenantSchema


@tenants_bp.route('/tenants/<int:landlord_id>', methods=['GET'])
# @token_landlord_required
def get_landlord_tenants(landlord_id: int):
    tenants = Tenant.query.filter(Tenant.landlord_id == landlord_id).all()
    items = TenantSchema(many=True, exclude=['landlord']).dump(tenants)

    return jsonify({
        'success': True,
        'data': items,
        'number_of_records': len(items)
    })


#only landlord
@tenants_bp.route('/tenants/<int:tenant_id>', methods=['GET'])
def get_landlord_tenant(tenant_id: int):
    return jsonify({
        'success': True,
        'data': f'get_landlord_tenant function (tenant with id: {tenant_id})'
    })


#only landlord
@tenants_bp.route('/tenants', methods=['POST'])
def create_tenant():
    return jsonify({
        'success': True,
        'data': f'create_tenant function'
    })


#only landlord or this tenant
@tenants_bp.route('/tenants/<int:tenant_id>/password', methods=['PUT'])
def update_tenant_password(tenant_id):
    return jsonify({
        'success': True,
        'data': f'update_tenant_password function (tenant id: {tenant_id}'
    })


#only landlord or this tenant
@tenants_bp.route('/tenants/<int:tenant_id>/data', methods=['PUT'])
def update_tenant_data(tenant_id):
    return jsonify({
        'success': True,
        'data': f'update_tenant_data function (tenant id: {tenant_id}'
    })


#only landlord
@tenants_bp.route('/tenants/<int:tenant_id>', methods=['DELETE'])
def delete_tenant(tenant_id):
    return jsonify({
        'success': True,
        'data': f'delete_tenant function (tenant id: {tenant_id}'
    })
