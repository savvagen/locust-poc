import locust
import os, sys
from locust import TaskSet, Locust, HttpLocust, task, events

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, "../..")))

from hooks.listeners import *


cwd = os.getcwd()
json_path = "{}/scenarios/test_data".format(cwd)
base_uri = "https://jsonplaceholder.typicode.com"


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



"""
Create Test Structure

1. Main Scenario:
    a. UserScenario
    b. AdminScenario
    
here is one important thing to note about the above example, 
and that is the call to self.interrupt() in the UserScenario’s and AdminScenario's stop method. 
What this does is essentially to stop executing the UserScenarios task set 
and the execution will continue in the MainScenario instance.
If we didn’t have a call to the interrupt() method somewhere in UserScenario, 
the Locust would never stop running the UserScenario task once it has started. 
But by having the interrupt function, we can—together with task weighting—define 
how likely it is that a simulated user leaves the scenarios.
"""

class UsersScenario(TaskSet):

    @task(1)
    def get_posts(self):
        get_posts(self)

    @task(2)
    class PostBehavior(TaskSet):
        @task(1)
        def get_post(self):
            get_post(self, 1)

        @task(2)
        def edit_post(self):
            update_post(self, 1, {"id": 1, "title": 'foo', "body": 'bar', "userId": 1})

    @task(1)
    def stop(self):
        self.interrupt()



class AdminScenario(TaskSet):

    @task(1)
    def patch_post(self):
        patch_post(self, 1, {"title": "Post Title Changed"})

    @task(10)
    def create_post(self):
        create_post(self, {"id": 1, "title": 'foo', "body": 'bar', "userId": 1})

    @task(5)
    def stop(self):
        self.interrupt()



class MainScenario(TaskSet):
    tasks = {
        UsersScenario: 1,
        AdminScenario: 2
    }

    @task
    def task(self):
        pass






class LoadTests(HttpLocust):
    host = base_uri
    task_set = MainScenario
    min_wait = 1000
    max_wait = 2000

