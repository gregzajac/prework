from flask import jsonify, abort
from webargs.flaskparser import use_args
from myrent_app import db
from myrent_app.tenants import tenants_bp
from myrent_app.models import Tenant, TenantSchema, tenant_schema, \
                            tenant_update_password_schema
from myrent_app.utils import token_landlord_required, token_landlord_tenant_required, \
                            validate_json_content_type, generate_hashed_password


@tenants_bp.route('/tenants', methods=['GET'])
@token_landlord_required
def get_landlord_tenants(landlord_id: int):
    tenants = Tenant.query.filter(Tenant.landlord_id == landlord_id).all()
    items = TenantSchema(many=True, exclude=['landlord']).dump(tenants)

    return jsonify({
        'success': True,
        'data': items,
        'number_of_records': len(items)
    })


@tenants_bp.route('/tenants/<int:tenant_id>', methods=['GET'])
@token_landlord_required
def get_landlord_tenant(landlord_id: int, tenant_id: int):
    tenant = Tenant.query.filter(Tenant.landlord_id == landlord_id) \
                        .filter(Tenant.id == tenant_id).first()
    if tenant is None:
        abort(404, description=f'Tenant with id {tenant_id} not found')

    return jsonify({
        'success': True,
        'data': tenant_schema.dump(tenant)
    })


@tenants_bp.route('/tenants', methods=['POST'])
@token_landlord_required
@validate_json_content_type
@use_args(TenantSchema(exclude=['landlord_id']), error_status_code=400)
def create_tenant(landlord_id: int, args: dict):
    tenant = Tenant(landlord_id=landlord_id, **args)

    db.session.add(tenant)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': tenant_schema.dump(tenant)
    })


@tenants_bp.route('/tenants/login', methods=['POST'])
@validate_json_content_type
@use_args(TenantSchema(only=['identifier', 'password']), error_status_code=400)
def login_tenant(args: dict):
    tenant = Tenant.query.filter(Tenant.identifier == args['identifier']).first()

    if not tenant:
        abort(401, description='Invalid credentials')

    if not tenant.is_password_valid(args['password']):
        abort(401, description='Invalid credentials')

    token = tenant.generate_jwt()

    return jsonify({
        'success': True,
        'token': token.decode()
    })


@tenants_bp.route('/tenants/<int:tenant_id>/password', methods=['PUT'])
@token_landlord_tenant_required
@validate_json_content_type
@use_args(tenant_update_password_schema, error_status_code=400)
def update_tenant_password(id_model_tuple: tuple, args: dict, tenant_id: int):
    print('use_args dane: ', use_args)
    print('model: ', id_model_tuple[1])
    if id_model_tuple[1] == 'landlords':
        tenant = Tenant.query.filter(Tenant.landlord_id == id_model_tuple[0]) \
                            .filter(Tenant.id == tenant_id).first()
        if tenant is None:
            abort(404, description=f'Tenant with id {tenant_id} not found')

    if id_model_tuple[1] == 'tenants':
        if id_model_tuple[0] != tenant_id:
            abort(404, description=f'Incorrect tenant id')
        tenant = Tenant.query.get_or_404(tenant_id, 
                                        description=f'Tenant with id {tenant_id} not found')

    if not tenant.is_password_valid(args['current_password']):
        abort(401, description='Invalid password')

    tenant.password = generate_hashed_password(args['new_password'])
    db.session.commit()

    return jsonify({
        'success': True,
        'data': tenant_schema.dump(tenant)
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
