from locust import HttpUser, task, between


class Service1User(HttpUser):
    wait_time = between(0.1, 1)

    @task
    def call_service1(self) -> None:
        self.client.get("/")
