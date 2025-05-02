# MySQLのDockerセットアップに関するTips

## 1. docker-composeでMySQLを使う場合の事前準備
- 基本的に特別な事前準備は不要。
- docker-compose.ymlのdbサービスでMYSQL_DATABASE、MYSQL_USER、MYSQL_PASSWORD、MYSQL_ROOT_PASSWORDなどを指定しておくと、初回起動時に自動でデータベースやユーザーが作成される。

## 2. 永続化（ボリューム）
- volumes: でdb_data:/var/lib/mysqlを指定している場合、MySQLのデータはコンテナを消しても残る。

## 3. 初期データ投入
- テーブルの初期化SQLやサンプルデータを自動投入したい場合は、docker-entrypoint-initdb.dという仕組みを使う。
- 例：dbサービスのvolumesに「./initdb:/docker-entrypoint-initdb.d」を追加し、initdbディレクトリに.sqlファイルを置く。

## 4. 接続情報の確認
- FlaskアプリからMySQLに接続するための情報（ホスト名、ユーザー名、パスワード、DB名）は.envやdocker-compose.ymlで指定したものを使う。
- ホスト名はdb（docker-composeのサービス名）でOK。

## 5. まとめ
- docker-composeでMySQLを使う場合、特別な事前準備は不要。
- 起動時に自動でDB・ユーザーが作成される。
- 必要に応じて初期化SQLも自動実行できる。 