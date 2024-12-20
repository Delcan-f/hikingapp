from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.hike_review import HikeReview, hike_review_schema, hike_review_schemas

hike_reviews_bp = Blueprint("hike_reviews", __name__, url_prefix="/hike_reviews")

# Read one
@hike_reviews_bp.route("/<int:hike_review_id>")
def get_hike_review(hike_review_id):
    stmt = db.select(HikeReview).filter_by(id=hike_review_id)
    hike_review = db.session.scalar(stmt)
    if hike_review:
        return hike_review_schema.dump(hike_review)
    else: # finish writing response message
        return {"message": f"write something here"}
    
# Read all
@hike_reviews_bp.route("/")
def get_hike_reviews():
    stmt = db.select(HikeReview)
    hike_reviews_list = db.session.scalars(stmt)
    return hike_review_schema.dump(hike_reviews_list)

# Create hike review
@hike_reviews_bp.route("/<int:hike_review_id>", methods=["POST"])
def create_hike_review():
    try:
        body_data = hike_review_schema.load(request.get_json())
        hike_review = HikeReview(
            review_date=body_data.get("review_date"),
            rating=body_data.get("rating"),
            comments=body_data.get("comments"),
            hiker_id=body_data.get("hiker_id"),
            trail_id=body_data.get("trail_id")
        )
        db.session.add(hike_review)
        db.session.commit()
        return hike_review_schema.dump(hike_review), 201
    
    except IntegrityError as err:
        if err.otig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"{err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 409

# Delete hike review 
@hike_reviews_bp.route("/<int:hike_review_id>", methods=["DELETE"])
def delete_hike_review(hike_review_id):
    stmt = db.select(HikeReview).filter_by(id=hike_review_id)
    hike_review = db.session.scalar(stmt)
    if hike_review:
        db.session.delete(hike_review)
        db.session.commit()
        return {"message": f"Hike review written by {hike_review.hiker_id} about trail {hike_review.trail_id} has been deleted successfully"}
    else: 
        return {"message": f"Hike review written by {hike_review.hiker_id} about trail {hike_review.trail_id} does not exist"}, 404
    
# Update hike review 
@hike_reviews_bp.route("/<int:hike_review_id>", methods=["PUT", "PATCH"])
def update_hike_review(hike_review_id):
    stmt = db.select(HikeReview).filter_by(id=hike_review_id)
    hike_review = db.session.scalar(stmt)
    body_data = hike_review_schema.load(request.get_json(), partial=True)
    if hike_review:
        hike_review.review_date = body_data.get("review_date") or hike_review.review_date
        hike_review.rating = body_data.get("rating") or hike_review.rating
        hike_review.comments = body_data.get("comments") or hike_review.comments
        hike_review.hiker_id = body_data.get("hiker_id") or hike_review.hiker_id
        hike_review.trail_id = body_data.get("trail_id") or hike_review.trail_id
        db.session.commit()
        return hike_review_schema.dump(hike_review)
    else:
        return {"message": f"Hike review written by {hike_review.hiker_id} about trail {hike_review.trail_id} does not exist"}, 404