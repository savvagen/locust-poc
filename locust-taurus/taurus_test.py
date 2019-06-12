import locust
import os, sys
from locust import TaskSet, Locust, HttpLocust, task, events


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

    tasks = {get_posts: 2}

    @task(1)
    def get_post(self):
        resp = get_post(self, 1)
        print("Request: POST {} | Status Code: {}".format(resp.url, resp.status_code))


    @task(3)
    def create_post(self):
        resp = create_post(self, {"title": 'foo', "body": 'bar', "userId": 1})
        print("Request: POST {} | Status Code: {}".format(resp.url, resp.status_code))


    @task(3)
    def update_post(self):
        resp = update_post(self, 1, {"id": 1, "title": 'foo', "body": 'bar', "userId": 1})
        print("Request: POST {} | Status Code: {}".format(resp.url, resp.status_code))


    @task(3)
    def patch_post(self):
        resp = patch_post(self, 1, {"body": "bar."})
        print("Request: POST {} | Status Code: {}".format(resp.url, resp.status_code))



class LoadTests(HttpLocust):
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000


