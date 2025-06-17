import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# これはAlembicの設定オブジェクトで、
# 使用中の.iniファイル内の値にアクセスするために使用されます。
config = context.config

# Pythonのロギング設定を解釈します。
# この行は基本的にロガーを設定します。
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # Flask-SQLAlchemy<3とAlchemicalで動作します
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # Flask-SQLAlchemy>=3で動作します
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# ここにモデルのMetaDataオブジェクトを追加します
# 'autogenerate'サポートのために必要です
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

# 設定ファイルから他の値を取得できます：
# my_important_option = config.get_main_option("my_important_option")
# ... など


def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """オフラインモードでマイグレーションを実行します。

    これは、EngineをスキップしてURLのみでコンテキストを設定します。
    ただし、Engineもここで受け入れ可能です。
    Engineの作成をスキップすることで、
    DBAPIが利用可能である必要さえありません。

    ここでのcontext.execute()の呼び出しは、
    与えられた文字列をスクリプト出力に出力します。
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """オンラインモードでマイグレーションを実行します。

    このシナリオでは、Engineを作成し、
    コンテキストと接続を関連付ける必要があります。
    """

    # このコールバックは、スキーマに変更がない場合に
    # 自動マイグレーションが生成されるのを防ぐために使用されます
    # 参照: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('スキーマの変更は検出されませんでした。')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
