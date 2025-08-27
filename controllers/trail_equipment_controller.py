from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.trail_equipment import TrailEquipment, trail_equipment_schema, trail_equipments_schema

trail_equipments_bp = Blueprint("trail_equipments", __name__, url_prefix="/trail_equipments")

# Read one
@trail_equipments_bp.route("/int:trail_equipment_id>")
def get_trail_equipment(trail_equipment_id):
    stmt = db.select(TrailEquipment).filter_by(id=trail_equipment_id)
    trail_equipment = db.session.scalar(stmt)
    if trail_equipment:
        return trail_equipment_schema.dump(trail_equipment)
    else: # finish writing error response 
        return {"message": f"Trail Equipment written by {trail_equipment.hiker_id} about trail {trail_equipment.trail_id} does not exist"}
    
# Read all
@trail_equipments_bp.route("/")
def get_trail_equipments():
    stmt = db.select(TrailEquipment)
    trail_equipment_list = db.session.scalars(stmt)
    return trail_equipments_schema.dump(trail_equipment_list)

# Create trail equipment
@trail_equipments_bp.route("/<int:trail_equipment_id>", methods=["POST"])
def create_trail_equipment():
    try:
        body_data = trail_equipment_schema.load(request.get_json())
        trail_equipment = TrailEquipment(
            required_equipment=body_data.get("required_equipment"),
            recommended_equipment=body_data.get("recommended_equipment"),
            hiker_id=body_data.get("hiker_id"),
            trail_id=body_data.get("trail_id")
        )
        db.session.add(trail_equipment)
        db.session.commit()
        return trail_equipment_schema.dump(trail_equipment), 201
    
    except IntegrityError as err:
            if err.otig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {"message": f"{err.orig.diag.column_name} is required"}
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {"message": err.orig.diag.message_detail}, 409

# Delete trail equipment 
@trail_equipments_bp.route("/<int:trail_equipment_id>", methods=["DELETE"])
def delete_trail_equipment(trail_equipment_id):
    stmt = db.select(TrailEquipment).filter_by(id=trail_equipment_id)
    trail_equipment = db.session.scalar(stmt)
    if trail_equipment:
        db.session.delete(trail_equipment)
        db.session.commit()
        return {"message": f"Trail equipment written by {trail_equipment.hiker_id} about trail {trail_equipment.trail_id} has been deleted successfully"}
    else: 
        return {"message": f"Trail equipment written by {trail_equipment.hiker_id} about trail {trail_equipment.trail_id} does not exist"}
    
# Update trail equipment
@trail_equipments_bp.route("/<int:trail_equipment_id>", methods=["PUT", "PATCH"])
def update_trail_equipment(trail_equipment_id):
    stmt = db.select(TrailEquipment).filter_by(id=trail_equipment_id)
    trail_equipment = db.session.scalar(stmt)
    body_data = trail_equipment_schema.load(request.get_json(), partail=True)
    if trail_equipment:
        trail_equipment.required_equipment = body_data.get("required_equipment") or trail_equipment.required_equipment
        trail_equipment.recommended_equipment = body_data.get("recommended_equipment") or trail_equipment.recommended_equipment
        trail_equipment.hiker_id = body_data.get("hiker_id") or trail_equipment.hiker_id
        trail_equipment.trail_id = body_data.get("trail_id") or trail_equipment.trail_id
        db.session.commit()
        return trail_equipment_schema.dump(trail_equipment)
    else: 
        return {"message": f"Trail equipment about trail {trail_equipment.trail_id} does not exist"}, 404
    