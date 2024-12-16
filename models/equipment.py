from init import db, ma

class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(100), nullable=False)
    equipment_type = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)

class EquipmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "equipment_name", "equipment_type", "weight", "description")

equipment_schema = EquipmentSchema()
equipments_schema = EquipmentSchema(many=True)