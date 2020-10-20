from flask import Blueprint, request, jsonify, current_app
from .database import db
from .models import *

api = Blueprint('api', __name__, url_prefix='/api')


def validate_nfc_id(nfc_id):
    if not isinstance(nfc_id, str):
        return False
    if len(nfc_id) != 8:
        return False
    try:
        int(nfc_id, 16)
        return True
    except ValueError:
        return False


@api.route('/users', methods=['POST'])
def register_user():
    logger = current_app.logger
    json = request.get_json()
    if json is None:
        return jsonify({"status": "Bad Request"}), 400

    nfc_id = json.get('nfc_id')
    name = json.get('name')

    if nfc_id is None or name is None or not validate_nfc_id(nfc_id):
        return jsonify({"status": "Bad Request"}), 400

    user = User(name, nfc_id, name)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logger.warning(e)

    return jsonify({"status": "Created", "user": {"id": user.id}}), 201
