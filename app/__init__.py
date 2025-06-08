from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config.config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # データベース設定
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://user:password@db:3306/task_manager')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
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