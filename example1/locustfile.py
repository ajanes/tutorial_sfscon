from locust import HttpUser, task

class SimpleUser(HttpUser):

    @task
    def view_homepage(self):
        self.client.get("/")

    @task(5)
    def view_users(self):
        self.client.get("/users")