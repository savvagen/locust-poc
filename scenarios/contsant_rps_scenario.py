import locust
from statistics import median
import os, sys, random, json
from locust import TaskSet, Locust, HttpLocust, task, events, runners

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, "../..")))

from hooks.listeners import *

cwd = os.getcwd()
json_path = "{}/scenarios/test_data".format(cwd)

# base_uri = "https://jsonplaceholder.typicode.com" ## Live JSON_PLACEHOLDER
base_uri = "http://localhost:3000"


def register_user(l, payload):
    return l.client.post("/users", payload)


def get_user(l, uuid):
    return l.client.get('/users/{}'.format(uuid))


def get_posts(l):
    return l.client.get("/posts")


def get_post(l, post_id):
    return l.client.get("/posts/{}".format(post_id))


def create_post(l, paylaod):
    return l.client.post("/posts", data=paylaod)


def update_post(l, post_id, payload):
    return l.client.put("/posts/{}".format(post_id), data=payload)


def patch_post(l, post_id, payload):
    return l.client.patch("/posts/{}".format(post_id), data=payload)


def delete_user(l, uuid):
    return l.client.delete('/users/{}'.format(uuid))


def delete_post(l, post_id):
    return l.client.delete('/posts/{}'.format(post_id))


class UserScenario(TaskSet):
    uuid = 1
    post_id = 1

    # is called once when task-set is starting
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

    tasks = {get_posts: 2}

    @task(1)
    def get_post(self):
        get_post(self, 1)

    @task(3)
    def create_post(self):
        create_post(self, {"title": 'foo', "body": 'bar', "userId": self.uuid})

    @task(3)
    def update_post(self):
        update_post(self, self.post_id, {"id": self.post_id, "title": 'foo', "body": 'bar', "userId": self.uuid})

    @task(3)
    def patch_post(self):
        patch_post(self, self.post_id, {"body": "bar."})





# Add listeners for Stress Tests quiting
# events.request_success += my_response_time_handler
# events.request_failure += my_error_handler
# events.request_success += my_requests_number_handler

# RPS listeners WORKING ONLY WITH ONE NODE and MASTER mode
# events.report_to_master += on_report_to_master
# events.slave_report += on_slave_report
# events.slave_report += on_slave_report_latency_handler




class LoadTests(HttpLocust):
    host = base_uri
    task_set = UserScenario
    # min_wait = 1000
    # max_wait = 1000
    wait_function = lambda self: self.fixed_rps_wait_function(100)
    # wait_function = lambda t: 900 if runners.global_stats.total.current_rps < 100 else 1100

    def __init__(self):
        super(LoadTests, self).__init__()
        self.my_wait = 1000

    def fixed_rps_wait_function(self, desired_rps):
        # Will increase and decrease tasks wait time in range of 99.8 - 100.7 rps
        current_rps = runners.global_stats.total.current_rps
        if current_rps < desired_rps - 0.2:
            # the minimum wait is 10 ms
            if self.my_wait > 10:
                self.my_wait -= 4
        elif current_rps > desired_rps + 0.7:
            self.my_wait += 4
        # print("Current RPS: {}".format(current_rps))
        # print("Default wait is: {}".format(self.my_wait))
        return self.my_wait