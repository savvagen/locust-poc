from locust_fixed_interval import FixedIntervalTaskSet
from locust import HttpLocust, TaskSet, task


class UsersBhavior(FixedIntervalTaskSet):
    def setup(self):
        self.interval = 100

    @task(1)
    def get_users(self):
        self.client.get('/users')

    @task(2)
    def get_user(self):
        self.client.get('/users/1')

class LocustRunner(HttpLocust):
    task_set = UsersBhavior
    host = "http://localhost:3000"
