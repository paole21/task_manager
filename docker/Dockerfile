# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# 環境変数を設定
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# ポートを公開
EXPOSE 5000

# アプリケーションを実行
CMD ["flask", "run", "--host=0.0.0.0"] 