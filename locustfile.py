from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(0, 1)

    def on_start(self):
        self.client.headers['User-Agent'] = "Mozilla/5.0"

    @task
    def index_page(self):
        self.client.get("/")