from init import db, ma

class TrailEquipment(db.Model):
    __tablename__ = "trail_equipment"

    id = db.Column(db.Integer, primary_key=True)
    required_equipment = db.Column(db.String(100), nullable=False)
    recommended_equipment = db.Column(db.String(100), nullable=True)

    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey("trail.id"), nullable=False)

    equipment_id = db.relationship("Equipments", back_populates="trail_equipments")
    trail_id = db.relationship("Trails", back_populates="trail_equipments")

class TrailEquipmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "required_equipment", "recommended_equipment", "hiker_id", "trail_id", "hiker", "trail")

trail_equipment_schema = TrailEquipmentSchema()
trail_equipments_schema = TrailEquipmentSchema(many=True)