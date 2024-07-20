from flask import jsonify, request, abort
from app import app, db
from app.models import Content, Device, ProtectionSystem
from utils.encryption import encrypt_data, decrypt_data

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify that the service is running.
    Returns a JSON response with status 'ok'.
    """
    return jsonify({'status': 'ok'}), 200

@app.route('/contents', methods=['GET'])
def get_contents():
    """
    Retrieves all contents that are associated with the protection systems used by devices.
    Decrypts the payload of each content before returning it.
    Returns a JSON response with the list of contents.
    """
    device_protection_systems = Device.query.with_entities(Device.protection_system).distinct().all()
    protection_system_ids = [ps[0] for ps in device_protection_systems]

    contents = Content.query.filter(Content.protection_system.in_(protection_system_ids)).all()

    if not contents:
        return jsonify([]), 200

    result = []
    for content in contents:
        protection_system = ProtectionSystem.query.get(content.protection_system)
        if protection_system is None:
            continue

        encryption_mode = protection_system.encryption_mode
        encryption_key = content.encryption_key
        encrypted_payload = content.encrypted_payload

        try:
            decrypt_data(encryption_mode, encryption_key, encrypted_payload)
            result.append({
                'id': content.id,
                'protection_system': content.protection_system,
                'encrypted_payload': encrypted_payload
            })
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return jsonify(result)

@app.route('/contents/<int:content_id>', methods=['GET'])
def get_content_by_id(content_id):
    """
    Retrieves a specific content by its ID.
    Decrypts the payload of the content before returning it.
    Returns a JSON response with the content data.
    """
    content = Content.query.get(content_id)
    if content is None:
        return jsonify({'error': 'Content not found'}), 404

    protection_system = ProtectionSystem.query.get(content.protection_system)
    if protection_system is None:
        return jsonify({'error': 'Protection system not found'}), 404

    encryption_mode = protection_system.encryption_mode
    encryption_key = content.encryption_key
    encrypted_payload = content.encrypted_payload

    try:
        decrypt_data(encryption_mode, encryption_key, encrypted_payload)
        return jsonify({
            'id': content.id,
            'protection_system': content.protection_system,
            'encrypted_payload': encrypted_payload
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/contents/<int:content_id>', methods=['PUT'])
def update_content(content_id):
    """
    Updates a specific content by its ID.
    Encrypts the payload if it is updated.
    Returns a JSON response with the updated content data.
    """
    content = Content.query.get(content_id)
    if content is None:
        abort(404)
    if not request.json:
        abort(400)
    
    protection_system_id = request.json.get('protection_system', content.protection_system)
    encryption_key = request.json.get('encryption_key', content.encryption_key)
    plaintext_payload = request.json.get('plaintext_payload')

    protection_system = ProtectionSystem.query.get(protection_system_id)
    if protection_system is None:
        abort(404, description="Protection system not found")

    if plaintext_payload is not None:
        encryption_mode = protection_system.encryption_mode
        try:
            encrypted_payload = encrypt_data(encryption_mode, encryption_key, plaintext_payload)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    else:
        encrypted_payload = content.encrypted_payload

    content.protection_system = protection_system_id
    content.encryption_key = encryption_key
    content.encrypted_payload = encrypted_payload
    
    db.session.commit()
    return jsonify({
        'id': content.id,
        'protection_system': content.protection_system,
        'encryption_key': content.encryption_key,
        'encrypted_payload': content.encrypted_payload
    })

@app.route('/contents', methods=['POST'])
def create_content():
    """
    Creates a new content entry.
    Encrypts the payload before saving.
    Returns a JSON response with the created content data.
    """
    if not request.json or not 'protection_system' in request.json or not 'encryption_key' in request.json or not 'plaintext_payload' in request.json:
        abort(400)
    
    protection_system_id = request.json['protection_system']
    encryption_key = request.json['encryption_key']
    plaintext_payload = request.json['plaintext_payload']

    protection_system = ProtectionSystem.query.get(protection_system_id)
    if protection_system is None:
        abort(404, description="Protection system not found")

    encryption_mode = protection_system.encryption_mode

    try:
        encrypted_payload = encrypt_data(encryption_mode, encryption_key, plaintext_payload)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    new_content = Content(
        protection_system=protection_system_id,
        encryption_key=encryption_key,
        encrypted_payload=encrypted_payload
    )

    db.session.add(new_content)
    db.session.commit()

    return jsonify({
        'id': new_content.id,
        'protection_system': new_content.protection_system,
        'encrypted_payload': new_content.encrypted_payload
    }), 201

@app.route('/contents/<int:content_id>', methods=['DELETE'])
def delete_content(content_id):
    """
    Deletes a specific content by its ID.
    Returns a JSON response with a result indicating the success of the operation.
    """
    content = Content.query.get(content_id)
    if content is None:
        abort(404)
    db.session.delete(content)
    db.session.commit()
    return jsonify({'result': True})
