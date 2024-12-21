from marshmallow import fields, validates

from init import db, ma

class TrailEquipment(db.Model):
    __tablename__ = "trail_equipment"

    id = db.Column(db.Integer, primary_key=True)
    required_equipment = db.Column(db.String(100), nullable=False)
    recommended_equipment = db.Column(db.String(100), nullable=True)

    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.id"), nullable=False)

    equipment_id = db.relationship("Equipment", back_populates="trail_equipment")
    trail_id = db.relationship("Trail", back_populates="trail_equipment")

class TrailEquipmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "required_equipment", "recommended_equipment", "hiker_id", "trail_id", "hiker", "trail")

trail_equipment_schema = TrailEquipmentSchema()
trail_equipments_schema = TrailEquipmentSchema(many=True)