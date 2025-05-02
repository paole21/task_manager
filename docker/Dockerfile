# 1. Pythonの公式イメージをベースにする
FROM python:3.10

# 2. 作業ディレクトリを作成
WORKDIR /app

# 3. 必要なファイルをコンテナにコピー
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. アプリのソースコードをコピー
COPY . .

# 5. Flaskアプリを起動するコマンド
CMD ["flask", "run", "--host=0.0.0.0"] 