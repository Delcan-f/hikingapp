from init import db, ma

class Trail(db.Model):
    __tablename__ = "trails"

    id = db.Column(db.Integer, primary_key=True)
    trail_name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    hike_reviews = db.relationship("HikeReview", back_populates="trails", cascade="all, delete")
    trail_equipments = db.relationship("TrailEquipment", back_populates="trails", cascade="all, delete")

class TrailSchema(ma.Schema):
    class Meta:
        fields = ("id", "trail_name", "location", "distance", "difficulty")

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)