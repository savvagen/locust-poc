from locust import TaskSet, HttpLocust, task, between, constant_pacing

class TestScenario(TaskSet):

    @task
    def get_users(self):
        self.client.get("/users")

    @task
    def get_user(self):
        self.client.get("/users/null")

class LocustRunner(HttpLocust):
    task_set = TestScenario
    wait_time = between(0.5, 1.0)
    host = "http://localhost:3000"