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
        "--sender-wallet-uuid",
        is_secret=False,
        default="a0df3a39-e12e-4812-97e8-241898390daf",
        help="Sender wallet UUID",
    )
    parser.add_argument(
        "--recipient-wallet-uuid",
        is_secret=False,
        default="747c69b6-8da4-45cf-9bfb-db54c40a82a1",
        help="Recipient wallet UUID",
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
        self.client.post(
            "/api/transactions/create",
            json={
                "sender_wallet_uuid": self.environment.parsed_options.sender_wallet_uuid,
                "recipient_wallet_uuid": self.environment.parsed_options.recipient_wallet_uuid,
                "amount": random.randint(1, 100),
            },
        )
