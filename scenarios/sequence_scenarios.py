import locust
import os, sys
from locust import HttpLocust, task, events, seq_task, TaskSequence

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from hooks.listeners import *
cwd = os.getcwd()
json_path = "{}/scenarios/test_data".format(cwd)





# base_uri = "https://jsonplaceholder.typicode.com" ## Live JSON_PLACEHOLDER
base_uri = "http://localhost:3000"


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
        print("Request: POST {} | Status Code: {}".format(resp.url, resp.status_code))
        print("Registered user: {}.".format(self.uuid))


    def teardown(self):
        resp1 = self.client.delete('/users/{}'.format(self.uuid))
        print("Request: DELETE {} | Status Code: {}".format(resp1.url, resp1.status_code))
        print("Deleting User: {}".format(self.uuid))
        resp2 = self.client.delete("/posts/{}".format(self.post_id))
        print("Request: DELETE {} | Status Code: {}".format(resp2.url, resp2.status_code))
        print("Deleting Post: {}".format(self.post_id))


    @seq_task(1)
    def get_all_posts(self):
        resp = self.client.get("/posts")
        print("Request: GET {} | Status Code: {}".format(resp.url, resp.status_code))

    @seq_task(2)
    def create_custom_post(self):
        resp = self.client.post("/posts", {"title": 'foo', "body": 'bar', "author": self.uuid})
        print("Request: POST {} | Status Code: {}".format(resp.url, resp.status_code))
        self.post_id = resp.json()['id']

    @seq_task(3)
    @task(10)
    def watch_post(self):
        resp = self.client.get("/posts/1")
        print("Request: GET {} | Status Code: {}".format(resp.url, resp.status_code))


    @seq_task(4)
    def update_your_post(self):
        resp = self.client.put(f"/posts/1", data={"id": 1, "title": 'foo', "body": 'bar', "author": self.uuid})
        print("Request: PUT {} | Status Code: {}".format(resp.url, resp.status_code))


    @seq_task(5)
    def patch_your_post(self):
        resp = self.client.patch(f"/posts/{self.post_id}", data={"body": "bar."})
        print("Request: PATCH | Status Code: {}".format(resp.url, resp.status_code))



class LoadTests(HttpLocust):
    # host = base_uri
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
    stop_timeout = 30


# Add listeners for Stress Tests quiting
events.request_success += my_response_time_handler
events.request_failure += my_error_handler
events.request_success += my_requests_number_handler


class StressTests(HttpLocust):
    # host = base_uri
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
