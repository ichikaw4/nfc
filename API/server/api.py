from flask import Blueprint, request, jsonify, current_app
from .database import db
from .models import *
from datetime import datetime

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
        db.session.rollback()
        logger.warning(e)
        return jsonify({"status", "Internal server error"}), 500

    return jsonify({"status": "Created", "user": {"id": user.id}}), 201


@api.route('/read', methods=["POST"])
def read_nfc():
    logger = current_app.logger
    json = request.get_json()
    if json is None:
        return jsonify({"status": "Bad Request"}), 400

    nfc_id = json.get('nfc_id')

    if nfc_id is None or not validate_nfc_id(nfc_id):
        return jsonify({"status": "Bad Request"}), 400

    try:
        user = User.query.filter(User.nfc_id == nfc_id).one()
    except Exception as e:
        return jsonify({"status", "User not found"}), 404

    try:
        today = datetime.now()
        today = today.replace(minute=0, hour=0, second=0, microsecond=0)
        record = Record.query.filter(
            Record.user_id == user.id).filter(
            Record.is_active).filter(
            Record.created_at >= today).first()
    except Exception as e:
        logger.warning(e)
        return jsonify({"status", "Internal server error"}), 500

    if record is None:
        try:
            record = Record(user.id, user.name)
            db.session.add(record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.warning(e)
            return jsonify({"status", "Internal server error"}), 500
        return jsonify({"status": "Created", "record": {
            "created_at": record.created_at.strftime("%Y/%m/%d %H:%M:%S")
        }}), 201

    record.is_active = False
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.warning(e)
        return jsonify({"status", "Internal server error"}), 500
    return jsonify({"status": "Updated", "record": {
        "updated_at": record.created_at.strftime("%Y/%m/%d %H:%M:%S")
    }}), 200
