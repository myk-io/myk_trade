from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Float
from piccolo.columns.indexes import IndexMethod

ID = "2023-11-26T20:50:35:124910"
VERSION = "0.117.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID,
        app_name="myk_trade_db",
        description=DESCRIPTION,
    )

    manager.add_column(
        table_class_name="CurrencyModel",
        tablename="currency_model",
        column_name="to_base_rate",
        db_column_name="to_base_rate",
        column_class_name="Float",
        column_class=Float,
        params={
            "default": 1.0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    return manager
