 # Flaskの設定管理の仕組み

## 1. 設定クラスの階層構造

```python
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
```

### 1.1 継承の仕組み
- `Config`クラスが基底クラス（親クラス）
- `DevelopmentConfig`と`ProductionConfig`が子クラス
- 子クラスは親クラスの設定を継承し、必要に応じて上書き可能

### 1.2 設定の優先順位
1. 環境変数（`os.environ.get()`）
2. 子クラスの設定
3. 親クラスの設定
4. デフォルト値（`or`演算子の右側）

## 2. 設定の動的な選択

```python
# 環境に応じて設定を選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# 現在の環境に応じた設定を取得
current_config = config[os.environ.get('FLASK_ENV', 'development')]
```

### 2.1 設定の選択プロセス
1. `os.environ.get('FLASK_ENV', 'development')`
   - 環境変数`FLASK_ENV`の値を取得
   - 値が存在しない場合は'development'をデフォルト値として使用

2. `config[環境名]`
   - 辞書から対応する設定クラスを取得
   - 存在しない環境名の場合は`KeyError`が発生

3. `current_config`
   - 選択された設定クラスのインスタンス
   - アプリケーション全体で使用される設定

## 3. 環境変数の読み込み

```python
from dotenv import load_dotenv
load_dotenv()
```

### 3.1 読み込みプロセス
1. `.env`ファイルの存在確認
2. ファイル内の環境変数を読み込み
3. `os.environ`に設定を追加

### 3.2 環境変数の優先順位
1. システムの環境変数
2. `.env`ファイルの設定
3. コード内のデフォルト値

## 4. アプリケーションでの使用

```python
def create_app():
    app = Flask(__name__)
    app.config.from_object(current_config)
```

### 4.1 設定の適用プロセス
1. `current_config`から設定を取得
2. Flaskアプリケーションの設定として適用
3. 各拡張機能（SQLAlchemy, LoginManager等）が設定を使用

## 5. 設定の変更と拡張

### 5.1 新しい環境の追加
```python
class TestingConfig(Config):
    """テスト環境用の設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config['testing'] = TestingConfig
```

### 5.2 設定の動的な変更
```python
# アプリケーション実行中に設定を変更
app.config['DEBUG'] = True
```

## 6. ベストプラクティス

### 6.1 設定の分離
- 環境ごとに設定を分離
- 機密情報は環境変数で管理
- デフォルト値は安全な値を設定

### 6.2 設定の検証
- 必須の設定が存在するか確認
- 値の型や範囲を検証
- 環境に応じた適切な設定を確認

### 6.3 セキュリティ
- 機密情報は環境変数で管理
- `.env`ファイルはGitに含めない
- 本番環境の設定は慎重に管理