from flask import Flask, render_template

from config import Config
from .extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import models

        if app.config.get("AUTO_CREATE_SCHEMA"):
            db.create_all()
            from .seed.seed_data import update_demo_passwords

            update_demo_passwords()

        @login_manager.user_loader
        def load_user(user_id):
            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                return None
            return db.session.get(models.User, user_id)

    from .routes.auth_routes import auth_bp
    from .routes.main_routes import main_bp
    from .routes.student_routes import student_bp
    from .routes.faculty_routes import faculty_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    return app
