from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.column_types import Date, ForeignKey, Serial, Varchar
from piccolo.columns.defaults.date import DateNow
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class WalletModel(Table, tablename="wallet_model", schema=None):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name="id",
        secret=False,
    )


ID = "2023-11-23T22:31:45:340784"
VERSION = "0.117.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID,
        app_name="myk_trade_db",
        description=DESCRIPTION,
    )

    manager.add_table(
        class_name="TransactionModel",
        tablename="transaction_model",
        schema=None,
        columns=None,
    )

    manager.add_column(
        table_class_name="TransactionModel",
        tablename="transaction_model",
        column_name="sender_wallet_id",
        db_column_name="sender_wallet_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": WalletModel,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="TransactionModel",
        tablename="transaction_model",
        column_name="receiver_wallet_id",
        db_column_name="receiver_wallet_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": WalletModel,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="TransactionModel",
        tablename="transaction_model",
        column_name="amount",
        db_column_name="amount",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 200,
            "default": "",
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

    manager.add_column(
        table_class_name="TransactionModel",
        tablename="transaction_model",
        column_name="currency",
        db_column_name="currency",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 200,
            "default": "",
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

    manager.add_column(
        table_class_name="TransactionModel",
        tablename="transaction_model",
        column_name="date",
        db_column_name="date",
        column_class_name="Date",
        column_class=Date,
        params={
            "default": DateNow(),
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

    manager.add_column(
        table_class_name="TransactionModel",
        tablename="transaction_model",
        column_name="status",
        db_column_name="status",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 200,
            "default": "",
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
