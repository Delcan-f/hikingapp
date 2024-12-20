from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.trail import Trail, trail_schema, trails_schema

trails_bp = Blueprint("trails", __name__, url_prefix="/trails")

# Read one trail
@trails_bp.route("/<int:trail_id>")
def get_trail(trail_id):
    stmt = db.select(Trail).filter_by(id=trail_id)
    trail = db.session.scalar(stmt)
    if trail:
        return trail_schema.dump(trail)
    else: 
        return {"message": f"Trail {trail.trail_name} does not exist in the database"}, 404

# Read all trails
@trails_bp.route("/")
def get_trails():
    stmt = db.select(Trail)
    trails_list = db.session.scalars(stmt)
    return trails_schema.dump(trails_list)

# Create trail
@trails_bp.route("/<int:trail_id>", methods=["POST"])
def create_trail():
    body_data = trail_schema.load(request.get_json())
    trail = Trail(
        trail_name=body_data.get("trail_name"),
        location=body_data.get("location"),
        distance=body_data.get("distance"),
        difficulty=body_data.get("difficulty")
    )
    db.session.add()
    db.session.commit()
    return trail_schema.dump(trail), 201

# Delete trail
@trails_bp.route("/<int:trail_id>", methods=["DELETE"])
def delete_trail(trail_id):
    stmt = db.select(Trail).filter_by(id=trail_id)
    trail = db.session.scalar(stmt)
    if trail:
        db.session.delete(trail)
        db.session.commit()
        return {"message": f"Trail {trail.trail_name} has been deleted successfully"}
    else: 
        return {"message": f"Trail {trail.trail_name} does not exist"}, 404
    
# Update trail 
@trails_bp.route("/<int:trail_id>", methods=["PUT", "PATCH"])
def update_trail(trail_id):
    stmt = db.select(Trail).filter_by(id=trail_id)
    trail = db.session.scalar(stmt)
    body_data = trail_schema.load(request.get_json(), partial=True)
    if trail:
        trail.trail_name = body_data.get("trail_name") or trail.trail_name
        trail.location = body_data.get("location") or trail.location
        trail.distance = body_data.get("distance") or trail.distance
        trail.difficulty = body_data.get("difficulty") or trail.difficulty
        db.session.commit()
        return trail_schema.dump(trail)
    else:
        return {"message": f"Trail {trail.trail_name} does not exist"}, 404