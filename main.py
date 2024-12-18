import os

from flask import Flask

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.equipment_controller import equipments_bp
from controllers.hike_review_controller import hike_reviews_bp
from controllers.hiker_controller import hikers_bp
from controllers.trail_controller import trails_bp
from controllers.trail_equipment_controller import trail_equipments_bp


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    app.json.sort_keys = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(equipments_bp)
    app.register_blueprint(hike_reviews_bp)
    app.register_blueprint(hikers_bp)
    app.register_blueprint(trails_bp)
    app.register_blueprint(trail_equipments_bp)

    return app