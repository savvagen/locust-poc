import locust
import os, sys, random
from locust import TaskSet, Locust, HttpLocust, task, events, runners

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, "../..")))

from hooks.listeners import *
cwd = os.getcwd()
json_path = "{}/test_data".format(cwd)

base_uri = "http://localhost:3000"


# Add listeners for Stress Tests quiting
events.request_success += my_response_time_handler
events.request_failure += my_error_handler
events.request_success += my_requests_number_handler
events.quitting += validate_results

# RPS listeners WORKING ONLY WITH ONE NODE and MASTER mode
# events.report_to_master += on_report_to_master
# events.slave_report += on_slave_report
# events.slave_report += on_slave_report_latency_handler




class UserScenario(TaskSet):
    uuid = 1
    post_id = 1


    def setup(self):
        print("Setup Data!")
        self.uuid = self.client.post("/users", open("{}/user.json".format(json_path))).json()['id']
        self.post_id = self.client.post("/posts", {"title": 'foo', "body": 'bar', "userId": self.uuid}).json()['id']

    def teardown(self):
        self.client.delete("/users/{}".format(self.uuid))
        self.client.delete('/posts/{}'.format(self.client.get("/posts").json()[-1]['id']))


    @task(3)
    def get_publications(self):
        self.client.get("/posts")

    @task(2)
    def get_post(self):
        self.client.get("/posts/1")

    @task(1)
    def create_post(self):
        self.client.post("/posts", data={"title": 'foo', "body": 'bar', "userId": self.uuid})

    @task(1)
    def update_post(self):
        self.client.put("/posts/{}".format(self.post_id),
                        {"id": self.post_id, "title": 'foo', "body": 'bar', "userId": self.uuid})

    @task(1)
    def patch_post(self):
        self.client.patch("/posts/{}".format(self.post_id), {"body": "bar."})


class LoadTests(HttpLocust):
    host = base_uri
    task_set = UserScenario
    # min_wait = 1000
    # max_wait = 1000
    wait_function = lambda self: self.fixed_rps_wait_function(500)
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
                self.my_wait -= 10
        elif current_rps > desired_rps + 0.7:
            self.my_wait += 10
        # print("Current RPS: {}".format(current_rps))
        # print("Default wait is: {}".format(self.my_wait))
        return self.my_wait
