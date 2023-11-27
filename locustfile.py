from locust import HttpUser, task


class TestTranscationsGet(HttpUser):
    @task
    def get_transaction(self):
        self.client.get("/api/transactions/")
