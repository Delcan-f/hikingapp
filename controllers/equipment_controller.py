from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.equipment import Equipment, equipment_schema, equipments_schema

equipments_bp = Blueprint("equipments", __name__, url_prefix="/equipments")

# Read one
@equipments_bp.route("/<int:equipment_id>")
def get_equipment(equipment_id):
    stmt = db.select(Equipment).filter_by(id=equipment_id)
    equipment = db.session.scalar(stmt)
    if equipment:
        return equipment_schema.dump(equipment)
    else:
        return {"message": f"Equipment with id {equipment_id} and name {equipment.equipment_name} does not exist"}, 404
    
# Read all
@equipments_bp.route("/")
def get_equipments():
    stmt = db.select(Equipment)
    equipment_list = db.session.scalars(stmt)
    return equipment_schema.dump(equipment_list)

# Create equipment 
@equipments_bp.route("/<int:equipment_id>", methods=["POST"])
def create_equipment(equipment_id):
    body_data = equipment_schema.load(request.get_json())
    equipment = Equipment(
        equipment_name=body_data.get("equipment_name"),
        equipment_type=body_data.get("equipment_type"),
        weight=body_data.get("weight"),
        description=body_data.get("description")
    )
    db.session.add(equipment)
    db.session.commit()
    return equipment_schema.dump(equipment), 201

# Delete equipment
@equipments_bp.route("/<int:equipment_id>", methods=["DELETE"])
def delete_equipment(equipment_id):
    stmt = db.select(Equipment).filter_by(id=equipment_id)
    equipment = db.session.scalar(stmt)
    if equipment:
        db.session.delete(equipment)
        db.session.commit()
        return {"message": f"Equipment with id {equipment_id} and name {equipment.equipment_name} has been deleted successfully"}
    else:
        {"message": f"Equipment with id {equipment_id} and name {equipment.equipment_name} does not exist"}, 404

# Update equipment
@equipments_bp.route("/<int:equipment_id>", methods=["PUT", "PATCH"])
def update_equipment(equipment_id):
    stmt = db.select(Equipment).filter_by(id=equipment_id)
    equipment = db.session.scalar(stmt)
    body_data = equipment_schema.load(request.get_json(), partial=True)
    if equipment:
        equipment.equipment_name = body_data.get("equipment_name") or equipment.equipment_name
        equipment.equipment_type = body_data.get("equipment_type") or equipment.equipment_type
        equipment.weight = body_data.get("weight") or equipment.weight
        equipment.description = body_data.get("description") or equipment.description
        db.session.commit()
        return equipment_schema.dump(equipment)
    else:
        return {"message": f"Equipment with id {equipment_id} and name {equipment.equipment_name} does not exist"}, 404