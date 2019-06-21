import sys
import os
from locust import Locust, HttpLocust, events, task, TaskSequence, seq_task, runners


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from hooks.listeners import *
cwd = os.getcwd()
json_path = "{}/scenarios/test_data".format(cwd)




# base_uri = "https://jsonplaceholder.typicode.com" ## Live JSON_PLACEHOLDER
# base_uri = "http://localhost:3000"
base_uri = os.environ.get('BASE_URI', 'BASE_URI variable is not set!')




"""
@trace Decorator is used to return the response data
and method name to the test log.
"""
def trace(func):
    def request_wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        runners.logger.info("Request: {} {} | Status Code: {}".format(func.__name__, r.url, r.status_code))
        return r
    return request_wrapper



@trace
def register_user(l, payload):
    return l.client.post("/users", payload)

@trace
def get_user(l, uuid):
    return l.client.get('/users/{}'.format(uuid))

@trace
def get_posts(l):
    return l.client.get("/posts")

@trace
def get_post(l, post_id):
    return l.client.get("/posts/{}".format(post_id))

@trace
def create_post(l, paylaod):
    return l.client.post("/posts", data=paylaod)

@trace
def update_post(l, post_id, payload):
    return l.client.put("/posts/{}".format(post_id), data=payload)

@trace
def patch_post(l, post_id, payload):
    return l.client.patch("/posts/{}".format(post_id), data=payload)

@trace
def delete_user(l, uuid):
    return l.client.delete('/users/{}'.format(uuid))

@trace
def delete_post(l, post_id):
    return l.client.delete('/posts/{}'.format(post_id))






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
        self.uuid = register_user(self, open("{}/user.json".format(json_path))).json()['id']
        print("Registered user: {}.".format(self.uuid))
        self.post_id = create_post(self, {"title": 'foo', "body": 'bar', "userId": self.uuid}).json()['id']
        print("Registered Post: {}.".format(self.post_id))


    def teardown(self):
        print("Deleting User: {}".format(self.uuid))
        delete_user(self, self.uuid)
        print("Deleting Post: {}".format(get_posts(self).json()[-1]['id']))
        delete_post(self, get_posts(self).json()[-1]['id'])


    @seq_task(1)
    def get_all_posts(self):
        get_posts(self)

    @seq_task(2)
    def create_custom_post(self):
        create_post(self, {"title": 'foo', "body": 'bar', "userId": self.uuid})

    @seq_task(3)
    @task(10)
    def watch_post(self):
        get_post(self, 1)

    @seq_task(4)
    def update_your_post(self):
        resp = self.client.put("/posts/1", data={"id": 1, "title": 'foo', "body": 'bar', "userId": self.uuid})
        print("Request: PUT {} | Status Code: {}".format(resp.url, resp.status_code))

    @seq_task(5)
    def patch_your_post(self):
        resp = self.client.patch("/posts/{}".format(self.post_id), data={"body": "bar."})
        print("Request: PATCH | Status Code: {}".format(resp.url, resp.status_code))



class LoadTests(HttpLocust):
    host = base_uri
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
    stop_timeout = 30


# Add listeners for Stress Tests quiting
events.request_success += my_response_time_handler
events.request_failure += my_error_handler
events.request_success += my_requests_number_handler


class StressTests(HttpLocust):
    host = base_uri
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000





