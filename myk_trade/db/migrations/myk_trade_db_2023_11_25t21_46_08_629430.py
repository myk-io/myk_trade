from piccolo.apps.migrations.auto.migration_manager import MigrationManager

ID = "2023-11-25T21:46:08:629430"
VERSION = "0.117.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID,
        app_name="myk_trade_db",
        description=DESCRIPTION,
    )

    manager.rename_column(
        table_class_name="WalletModel",
        tablename="wallet_model",
        old_column_name="amount",
        new_column_name="balance",
        old_db_column_name="amount",
        new_db_column_name="balance",
    )

    return manager
