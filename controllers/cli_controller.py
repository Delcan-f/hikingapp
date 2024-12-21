from flask import Blueprint

from init import db
from models.equipment import Equipment
from models.hike_review import HikeReview
from models.hiker import Hiker
from models.trail_equipment import TrailEquipment
from models.trail import Trail

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():

    hikers = [
        Hiker(
            first_name="John",
            last_name="Smith",
            email="johnsmith@email.com",
            phone_number="0456789123"
        ),
        Hiker(
            first_name="Brett",
            last_name="Stevens",
            email="brettstevens@email.com",
            phone_number="0411225689"
        ),
        Hiker(
            first_name="Jessica",
            last_name="Grant",
            email="jessicagrant@email.com",
            phone_number="0489123477"
        )
    ]

    db.session.add_all(hikers)

    db.session.commit()

    trails = [
        Trail(
            trail_name="Cape to Cape Track",
            location="Margaret River Region",
            distance="130km",
            difficulty="Moderate"
        ),
        Trail(
            trail_name="Overland Track",
            location="Cradle Mountain-Lake",
            distance="65km",
            difficulty="Difficult"
        ),
        Trail(
            trail_name="Larapinta Trail",
            location="The West MacDonnell Ranges",
            distance="223km",
            difficulty="Moderate"
        )
    ]

    db.session.add_all(trails)
    db.session.commit()

    equipments = [
        Equipment(
            equipment_name="Backpack",
            equipment_type="Storage",
            weight="0.8kg",
            description="A standard hiking backpack with a built in 30L water bladder"
        ),
        Equipment(
            equipment_name="Hiking Boots",
            equipment_type="Clothing/Apparel",
            weight="1.1kg",
            description="Standard high grip hiking boots build for rough terrain and completely waterproof"
        ),
        Equipment(
            equipment_name="Trekking Poles",
            equipment_type="Accessory/Assistance",
            weight="0.6kg",
            description="Collapsable trekking poles to assist in high elevation hikes"
        )
    ]

    db.session.add_all(equipments)

    db.session.commit()

    hike_reviews = [
        HikeReview(
            review_date="2024-06-23",
            rating=8,
            comments="The Cape to Cape Track offers an exhilarating mix of coastal cliffs, cave networks, breezy forests and sandy beaches. Each day will feel like a new adventure as you weave through the breathtaking Margaret River region.",
            hiker_id=hikers[0].id,
            trail_id=trails[0].id
        ),
        HikeReview(
            review_date="2022-01-19",
            rating=9,
            comments="Tasmania is spoiled with incredible walking trails, but few are as iconic as the Overland Track. The trail weaves through mossy woods and past towering bluffs over six thrilling, picture-perfect days. Head off on your own for flexibility, or take on the Overland Track in style with the Cradle Mountain Signature Walk – complete with cosy private huts to retire to at the end of tiring days.",
            hiker_id=hikers[0].id,
            trail_id=trails[1].id
        ),
        HikeReview(
            review_date="2023-02-28",
            rating=9,
            comments="One of Australia’s most epic outback treks, the Larapinta Trail follows the spine of the rugged West MacDonnell Ranges in the Northern Territory. Expect towering red rock escarpments, refreshing waterholes and steep terrain, as well as the opportunity to visit sacred Aboriginal sites.",
            hiker_id=hikers[1].id,
            trail_id=trails[1].id
        )
    ]

    db.session.add_all(hike_reviews)

    trail_equipments = [
        TrailEquipment(
            required_equipment="Backpack and Hiking Boots",
            recommended_equipment="Backpack, Hiking Boots, Tent",
            trail_id=trails[0].id,
            equipment_id=equipments[0,1].id
        ),
        TrailEquipment(
            required_equipment="Hiking Boots",
            recommended_equipment="Hiking Boots",
            trail_id=trails[2].id,
            equipment_id=equipments[1].id
        ),
        TrailEquipment(
            required_equipment="Backpack",
            recommended_equipment="Backpack, Hiking Boots",
            trail_id=trails[0].id,
            equipment_id=equipments[0].id
        )
    ]

    db.session.add_all(trail_equipments)

    db.session.commit()

    print("Tables seeded")