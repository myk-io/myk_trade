from piccolo.apps.migrations.auto.migration_manager import MigrationManager

ID = "2023-11-23T22:49:33:979876"
VERSION = "0.117.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID,
        app_name="myk_trade_db",
        description=DESCRIPTION,
    )

    manager.rename_column(
        table_class_name="TransactionModel",
        tablename="transaction_model",
        old_column_name="date",
        new_column_name="created_at",
        old_db_column_name="date",
        new_db_column_name="created_at",
    )

    return manager
