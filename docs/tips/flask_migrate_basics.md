# Flask-Migrateの基本と使用方法

## 1. Flask-Migrateとは
Flask-Migrateは、Flaskアプリケーションでデータベースのマイグレーションを管理するための拡張機能です。SQLAlchemyのデータベースモデルの変更を追跡し、データベーススキーマの更新を安全に行うことができます。

## 2. 主な機能
- データベーススキーマの変更履歴管理
- 変更の自動検出とマイグレーションスクリプトの生成
- ロールバック（変更の取り消し）機能
- チーム開発でのデータベース変更の共有

## 3. セットアップ手順

### 3.1 必要なパッケージのインストール
```bash
pip install Flask-Migrate
```

### 3.2 アプリケーションへの統合
```python
from flask_migrate import Migrate

# アプリケーションの初期化時に追加
migrate = Migrate()
migrate.init_app(app, db)
```

### 3.3 マイグレーション環境の初期化
```bash
# 環境変数の設定
$env:FLASK_APP = "app"  # PowerShellの場合
export FLASK_APP=app    # Bashの場合

# マイグレーション環境の初期化
flask db init
```

## 4. ディレクトリ構造
```
migrations/
├── versions/          # マイグレーションスクリプト
├── alembic.ini        # Alembic設定ファイル
├── env.py            # マイグレーション環境設定
├── README            # 説明書
└── script.py.mako    # スクリプトテンプレート
```

## 5. 基本的なコマンド

### 5.1 マイグレーションの作成
```bash
flask db migrate -m "変更の説明"
```

### 5.2 マイグレーションの適用
```bash
flask db upgrade
```

### 5.3 マイグレーションのロールバック
```bash
flask db downgrade
```

### 5.4 マイグレーション履歴の確認
```bash
flask db history
```

## 6. 開発時のベストプラクティス

### 6.1 マイグレーションの作成
- 変更内容を明確に記述する
- 小さな単位でマイグレーションを作成する
- テスト環境で動作確認を行う

### 6.2 チーム開発での注意点
- マイグレーションファイルをバージョン管理に含める
- マイグレーションの順序を守る
- コンフリクトを避けるため、頻繁に同期する

### 6.3 本番環境での注意点
- バックアップを取ってからマイグレーションを実行
- メンテナンス時間を考慮する
- ロールバック手順を事前に確認

## 7. トラブルシューティング

### 7.1 よくある問題
- マイグレーションの競合
- データの整合性の問題
- 環境変数の設定ミス

### 7.2 解決方法
- マイグレーション履歴の確認
- データベースのバックアップからの復元
- 環境変数の再確認

## 8. 参考リソース
- [Flask-Migrate公式ドキュメント](https://flask-migrate.readthedocs.io/)
- [SQLAlchemyドキュメント](https://docs.sqlalchemy.org/)
- [Alembicドキュメント](https://alembic.sqlalchemy.org/) 