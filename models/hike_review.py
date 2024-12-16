from datetime import date

from init import db, ma

class HikeReview(db.Model):
    __tablename__ = "hike_review"

    id = db.Column(db.Integer, primary_key=True)
    review_date = db.Column(db.Date)
    rating = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(200), nullable=True)

    hiker_id = db.Column(db.Integer, db.ForeignKey("hiker.id"), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey("trail.id"), nullable=False)

    hiker = db.relationship("Hiker", back_populates="hike_reviews")
    trail = db.relationship("Trails", back_populates="hike_reviews")

class HikeReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "review_date", "rating", "comments", "hiker_id", "trail_id", "hiker", "trail")

hike_review_schema = HikeReviewSchema()
hike_review_schemas = HikeReviewSchema(many=True)