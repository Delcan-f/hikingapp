from init import db, ma

class Hiker(db.Model):
    # Table name 
    __tablename__ = "hikers"

    # 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)

    hike_reviews = db.relationship("HikeReview", back_populates="hikers", cascade="all, delete")

class HikerSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email_address", "phone_number")

hiker_schema = HikerSchema()
hikers_schema = HikerSchema(many=True)