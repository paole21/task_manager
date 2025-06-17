from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config.config import current_config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(current_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # テスト用エンドポイント
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Task Manager API is running'
        })

    with app.app_context():
        db.create_all()

    return app 