import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

class Config:
    """基本設定クラス"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """開発環境用の設定"""
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///task_manager.db'

class ProductionConfig(Config):
    """本番環境用の設定"""
    DEBUG = False
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://user:password@localhost/task_manager'

# 環境に応じて設定を選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# 現在の環境に応じた設定を取得
current_config = config[os.environ.get('FLASK_ENV', 'development')] 