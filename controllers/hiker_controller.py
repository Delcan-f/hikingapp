from flask import Blueprint, request

from init import db
from models.hiker import Hiker, hiker_schema, hikers_schema

hikers_bp = Blueprint("hikers", __name__, url_prefix="/hikers")

# Read one
@hikers_bp.route("/<int:hiker_id>")
def get_hiker(hiker_id):
    stmt = db.select(Hiker).filter_by(id=hiker_id)
    hiker = db.session.scalar(stmt)
    if hiker:
        return hiker_schema.dump(hiker)
    else:
        return {"message": f"Hiker with id {hiker_id} does not exist"}, 404
    
# Read all
@hikers_bp.route("/")
def get_hikers():
    stmt = db.select(Hiker)
    hikers_list = db.session.scalars(stmt)
    return hikers_schema.dump(hikers_list)

# Create
@hikers_bp.route("/", methods=["POST"])
def create_hiker():
    body_data = hiker_schema.load(request.get_json())
    hiker = Hiker(
        first_name=body_data.get("first_name"),
        last_name=body_data.get("last_name"),
        
    )