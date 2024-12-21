from datetime import date

from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from init import db, ma

class HikeReview(db.Model):
    __tablename__ = "hike_reviews"

    id = db.Column(db.Integer, primary_key=True)
    review_date = db.Column(db.Date)
    rating = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(200), nullable=True)

    hiker_id = db.Column(db.Integer, db.ForeignKey("hikers.id"), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.id"), nullable=False)

    hiker = db.relationship("Hiker", back_populates="hike_reviews")
    trail = db.relationship("Trail", back_populates="hike_reviews")

class HikeReviewSchema(ma.Schema):

    @validates('review_date')
    def validate_review_date(self, value):
        today = date.today()
        if date.fromisoformat(value) > today:
            raise ValidationError("Review date cannot be for a future date")
        
    @validates('rating')
    def validate_rating_max_value(self, value):
        max_rating_value = 10
        min_rating_value = 0
        if float.fromisoformat(value) > max_rating_value:
            raise ValidationError("Maximum rating number is 10")
        
        if float.fromisoformat(value) < min_rating_value:
            raise ValidationError("Minimum rating value is 0")

    class Meta:
        fields = ("id", "review_date", "rating", "comments", "hiker_id", "trail_id", "hiker", "trail")

hike_review_schema = HikeReviewSchema()
hike_review_schemas = HikeReviewSchema(many=True)