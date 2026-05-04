# this file is the API layer, using Flask to link frontend with backend services and functions
# the general flow looks like:
# HTTP request → route → service → repository → DB → back up → JSON response

from flask import Blueprint, request, jsonify
import postgreSQL.property_service as serv

# groups all property-related endpoints
property_bp = Blueprint("properties", __name__)

# registers a route using the URL /properties and the HTTP method GET
@property_bp.route("/properties", methods=["GET"])
# when a client sends GET /properties, call the function below
def get_properties():
    return jsonify(serv.list_properties()) # jsonify() converts it to JSON + sets correct headers

@property_bp.route("/properties", methods=["POST"])
def add_property():
    data = request.json
    new_id = serv.create_property(data)
    return jsonify({"id": new_id}), 201 # 201 is the HTTP status code for Created