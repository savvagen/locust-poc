import locust
import os, sys
from locust import TaskSet, Locust, HttpLocust, task, events
from hooks.listeners import *

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, "../..")))

cwd = os.getcwd()
json_path = "{}/scenarios/test_data".format(cwd)
base_uri = "https://jsonplaceholder.typicode.com"



def register_user(l, payload):
    return l.client.post("/users", payload)

def get_user(l, uuid):
    return l.client.get(f'/users/{uuid}')

def get_posts(l):
    return l.client.get("/posts")

def get_post(l, post_id):
    return l.client.get(f"/posts/{post_id}")

def create_post(l, paylaod):
    return l.client.post("/posts", data=paylaod)

def update_post(l, post_id, payload):
    return l.client.put(f"/posts/{post_id}", data=payload)

def patch_post(l, post_id, payload):
    return l.client.patch(f"/posts/{post_id}", data=payload)

def delete_user(l, uuid):
    return l.client.delete(f'/users/{uuid}')

def delete_post(l, post_id):
    return l.client.delete(f'/posts/{post_id}')




class UserScenario(TaskSet):
    uuid = 1
    post_id = 1

    def setup(self):
        print("Setup Data!")
        self.uuid = register_user(self, open("{}/user.json".format(json_path))).json()['id']
        print(f"Registered user: {self.uuid}.")
        self.post_id = create_post(self, {"title": 'foo', "body": 'bar', "userId": self.uuid}).json()['id']
        print(f"Registered Post: {self.post_id}.")

    def teardown(self):
        print(f"Deleting User: {self.uuid}")
        delete_user(self, self.uuid)
        print(f"Deleting Post: {self.post_id}")
        delete_post(self, self.post_id)

    def on_start(self):
        print("Task Started!")

    def on_stop(self):
        print("Task Stoped!")


    tasks = {get_posts: 2}

    @task(1)
    def get_post(self):
        get_post(self, 1)

    @task(3)
    def create_post(self):
        create_post(self, {"title": 'foo', "body": 'bar', "userId": self.uuid})

    @task(3)
    def update_post(self):
        update_post(self, 1, {"id": 1, "title": 'foo', "body": 'bar', "userId": self.uuid})

    @task(3)
    def patch_post(self):
        patch_post(self, self.post_id, {"body": "bar."})


class LoadTests(HttpLocust):
    host = base_uri
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
    stop_timeout = 20




# Add listeners for Stress Tests quiting
events.request_success += my_success_handler
events.request_failure += my_error_handler
events.request_success += my_requests_number_handler


class StressTests(HttpLocust):
    host = base_uri
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
