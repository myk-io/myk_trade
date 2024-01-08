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
        default="6775bc68-f6a0-46ea-802c-0d2b5664a60f",
        help="Wallet UUID 3",
    )
    parser.add_argument(
        "--wallet4",
        is_secret=False,
        default="0c940e35-ebd3-4014-8c8a-07ab566a17aa",
        help="Wallet UUID 4",
    )


class TestTranscations(HttpUser):
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

        first_pair = [
            self.environment.parsed_options.wallet1,
            self.environment.parsed_options.wallet2,
        ]

        second_pair = [
            self.environment.parsed_options.wallet3,
            self.environment.parsed_options.wallet4,
        ]

        self.client.post(
            "/api/transactions/create",
            json={
                "sender_wallet_uuid": random.choice(first_pair),
                "recipient_wallet_uuid": random.choice(second_pair),
                "amount": random.randint(1, 100),
            },
        )
