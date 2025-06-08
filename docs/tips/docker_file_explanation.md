# Dockerfileとdocker-compose.ymlの詳細解説

## 1. Dockerfileの処理内容

### 1.1 基本構造
```dockerfile
# ベースイメージの指定
FROM python:3.11-slim
```
- `python:3.11-slim`: Python 3.11がインストールされた軽量なLinuxイメージ
- `slim`バージョンの特徴：
  - 最小限のパッケージのみを含む
  - イメージサイズが小さい
  - セキュリティリスクの低減

### 1.2 環境構築
```dockerfile
# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
```
- `WORKDIR`: コンテナ内の作業ディレクトリを設定
- `apt-get update`: パッケージリストの更新
- `build-essential`: コンパイルに必要な基本ツール
- `rm -rf /var/lib/apt/lists/*`: キャッシュ削除によるイメージ最適化

### 1.3 依存関係の管理
```dockerfile
# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
- `COPY`: ホストからコンテナへのファイルコピー
- `--no-cache-dir`: pipのキャッシュを使用せず、イメージサイズを最適化

### 1.4 アプリケーションの配置
```dockerfile
# アプリケーションのコピー
COPY . .

# 環境変数の設定
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONPATH=/app
```
- `COPY . .`: カレントディレクトリの全ファイルをコンテナの`/app`にコピー
- `ENV`: 環境変数の設定
  - `FLASK_APP`: アプリケーションのエントリーポイント
  - `FLASK_ENV`: 実行環境の指定
  - `PYTHONPATH`: Pythonのパス設定

### 1.5 実行設定
```dockerfile
# ポートの公開
EXPOSE 5000

# アプリケーションの実行
CMD ["flask", "run", "--host=0.0.0.0"]
```
- `EXPOSE`: コンテナのポートを外部に公開することを宣言
- `CMD`: コンテナ起動時に実行するコマンド
  - `--host=0.0.0.0`: 外部からのアクセスを許可

## 2. docker-compose.ymlのボリュームマウント

### 2.1 ボリュームマウントの基本形式
```yaml
volumes:
  - <ホスト側のパス>:<コンテナ側のパス>
```

### 2.2 アプリケーションのボリュームマウント
```yaml
volumes:
  - ../app:/app/app
  - ../config:/app/config
```
- `../app:/app/app`
  - ホスト側: プロジェクトの`app`ディレクトリ
  - コンテナ側: `/app/app`ディレクトリ
  - 効果: コード変更のリアルタイム反映

- `../config:/app/config`
  - ホスト側: プロジェクトの`config`ディレクトリ
  - コンテナ側: `/app/config`ディレクトリ
  - 効果: 設定ファイルのリアルタイム反映

### 2.3 データベースの永続化
```yaml
volumes:
  mysql_data:
```
- 名前付きボリューム`mysql_data`の作成
- データベースのデータを永続化
- コンテナ削除後もデータを保持

### 2.4 ボリュームマウントの利点
1. **開発効率の向上**
   - コード変更の即時反映
   - 再ビルド不要

2. **データの永続化**
   - データベースのデータ保持
   - コンテナ再作成時のデータ維持

3. **環境の一貫性**
   - 開発環境の統一
   - 依存関係の管理

## 3. ベストプラクティス

### 3.1 Dockerfile
- 軽量なベースイメージの使用
- マルチステージビルドの検討
- キャッシュの最適化
- セキュリティ考慮

### 3.2 docker-compose.yml
- 環境変数の適切な管理
- ボリュームの適切な設定
- サービス間の依存関係の明確化
- リソース制限の設定

### 3.3 開発時の注意点
- 不要なファイルの除外（.dockerignore）
- 環境変数の適切な管理
- ボリュームの適切な使用
- セキュリティ考慮 