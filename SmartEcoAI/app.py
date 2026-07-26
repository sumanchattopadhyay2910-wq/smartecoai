from flask import Flask
from backend.routes.home import home_bp
from backend.routes.camera import camera_bp
from backend.routes.detection import detection_bp
from backend.routes.violations import violations_bp
from backend.routes.reports import reports_bp
from backend.routes.dashboard import dashboard_bp
from backend.database.database import init_db
from backend.utils.logger import setup_logger
from config import Config


def create_app():
    app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
    app.config.from_object(Config)

    setup_logger(app)
    init_db(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(camera_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(violations_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(dashboard_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
