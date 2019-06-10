import locust
import os, sys
from locust import TaskSet, Locust, HttpLocust, task, events, seq_task, TaskSequence

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from hooks.listeners import *


cwd = os.getcwd()
json_path = "{}/scenarios/test_data".format(cwd)
base_uri = "https://jsonplaceholder.typicode.com"




###
# Write a scenario
###



class UserScenario(TaskSequence):
    """
    In the above example, the order is defined to execute get_all_posts(),
     then create_custom_post() and lastly the watch_post() for 10 times.
     Watch official doc:
    https://docs.locust.io/en/stable/writing-a-locustfile.html#tasksequence-class

    """
    uuid = 1
    post_id = 1

    def setup(self):
        print("Setup Data!")
        resp = self.client.post("/users", open("{}/user.json".format(json_path)))
        self.uuid = resp.json()['id']
        print(f"Request: POST {resp.url} | Status Code: {resp.status_code}")
        print(f"Registered user: {self.uuid}.")


    def teardown(self):
        resp1 = self.client.delete(f'/users/{self.uuid}')
        print(f"Request: DELETE {resp1.url} | Status Code: {resp1.status_code}")
        print(f"Deleting User: {self.uuid}")
        resp2 = self.client.delete(f"/posts/{self.post_id}")
        print(f"Request: DELETE {resp2.url} | Status Code: {resp2.status_code}")
        print(f"Deleting Post: {self.post_id}")


    @seq_task(1)
    def get_all_posts(self):
        resp = self.client.get("/posts")
        print(f"Request: GET {resp.url} | Status Code: {resp.status_code}")

    @seq_task(2)
    def create_custom_post(self):
        resp = self.client.post("/posts", {"title": 'foo', "body": 'bar', "userId": self.uuid})
        print(f"Request: POST {resp.url} | Status Code: {resp.status_code}")
        self.post_id = resp.json()['id']

    @seq_task(3)
    @task(10)
    def watch_post(self):
        resp = self.client.get("/posts/1")
        print(f"Request: GET {resp.url} | Status Code: {resp.status_code}")


    @seq_task(4)
    def update_your_post(self):
        resp = self.client.put(f"/posts/1", data={"id": 1, "title": 'foo', "body": 'bar', "userId": self.uuid})
        print(f"Request: PUT {resp.url} | Status Code: {resp.status_code}")


    @seq_task(5)
    def patch_your_post(self):
        resp = self.client.patch(f"/posts/{self.post_id}", data={"body": "bar."})
        print(f"Request: PATCH {resp.url} | Status Code: {resp.status_code}")




###
# Initialize the Load Test
###

class LoadTests(HttpLocust):
    host = base_uri
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
    stop_timeout = 30






###
# Initialize the Stress Test
###


# Add listeners for Stress Tests quiting
events.request_success += my_success_handler
events.request_failure += my_error_handler
events.request_success += my_requests_number_handler


class StressTests(HttpLocust):
    host = base_uri
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
