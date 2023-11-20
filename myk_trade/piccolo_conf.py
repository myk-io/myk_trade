from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

from myk_trade.settings import settings

DB = PostgresEngine(
    config={
        "database": settings.db_base,
        "user": settings.db_user,
        "password": settings.db_pass,
        "host": settings.db_host,
        "port": settings.db_port,
    },
)


APP_REGISTRY = AppRegistry(
    apps=["myk_trade.db.app_conf"],
)
