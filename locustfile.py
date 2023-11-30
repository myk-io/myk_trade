import random

from locust import HttpUser, events, task


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument(
        "--api-token",
        is_secret=True,
        default="secret",
        help="API token",
    )

    parser.add_argument(
        "--wallet1",
        is_secret=False,
        default="a0df3a39-e12e-4812-97e8-241898390daf",
        help="Wallet UUID 1",
    )
    parser.add_argument(
        "--wallet2",
        is_secret=False,
        default="747c69b6-8da4-45cf-9bfb-db54c40a82a1",
        help="Wallet UUID 2",
    )
    parser.add_argument(
        "--wallet3",
        is_secret=False,
        default="7c38af71-a61a-427b-b163-4e7e7f753c95",
        help="Wallet UUID 3",
    )
    parser.add_argument(
        "--wallet4",
        is_secret=False,
        default="38ad0c1f-e6d9-44ee-842a-86d5a739e1b7",
        help="Wallet UUID 4",
    )


class TestTranscationsGet(HttpUser):
    @task
    def get_transaction(self):
        self.client.get("/api/transactions/")

    @task
    def get_dashboard(self):
        self.client.get("/ui/")

    @task
    def do_transaction(self):
        self.client.headers = {
            "Authorization": f"Bearer {self.environment.parsed_options.api_token}",
        }

        wallets = [
            self.environment.parsed_options.wallet1,
            self.environment.parsed_options.wallet2,
            self.environment.parsed_options.wallet3,
            self.environment.parsed_options.wallet4,
        ]

        sender_wallet_uuid = random.choice(wallets)
        wallets.remove(sender_wallet_uuid)

        recipient_wallet_uuid = random.choice(wallets)

        self.client.post(
            "/api/transactions/create",
            json={
                "sender_wallet_uuid": sender_wallet_uuid,
                "recipient_wallet_uuid": recipient_wallet_uuid,
                "amount": random.randint(1, 100),
            },
        )
