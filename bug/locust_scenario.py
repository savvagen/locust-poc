from locust import TaskSet, task, HttpLocust


class Scenario(TaskSet):

    @task
    def success_task(self):
        self.client.get("/users/1")

    @task
    def failure_test(self):
        self.client.get("/users/fail")

class LocustRunner(HttpLocust):
    task_set = Scenario
    host = "http://jsonplaceholder.typicode.com"
    min_wait = 500
    max_wait = 1000