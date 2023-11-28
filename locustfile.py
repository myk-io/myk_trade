import os
import random

from locust import HttpUser, task


class TestTranscationsGet(HttpUser):
    @task
    def get_transaction(self):
        self.client.get("/api/transactions/")

    @task
    def get_dashboard(self):
        self.client.get("/ui/")

    @task
    def do_transaction(self):
        self.client.headers = {"Authorization": f"Bearer f{os.environ['TOKEN']}"}
        self.client.post(
            "/api/transactions/create",
            json={
                "sender_wallet_uuid": "a0df3a39-e12e-4812-97e8-241898390daf",
                "recipient_wallet_uuid": "747c69b6-8da4-45cf-9bfb-db54c40a82a1",
                "amount": random.randint(1, 100),
            },
        )
