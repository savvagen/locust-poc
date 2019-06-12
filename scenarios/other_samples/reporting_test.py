from locust import HttpLocust, task, TaskSet, events




class SampleTest(TaskSet):

    @task(1)
    def get_all_posts(self):
        resp = self.client.get("/posts")
        print("Request: GET {} | Status Code: {}".format(resp.url, resp.status_code))

    @task(2)
    def create_custom_post(self):
        resp = self.client.post("/posts", {"title": 'foo', "body": 'bar', "userId": 1})
        print("Request: POST {} | Status Code: {}".format(resp.url, resp.status_code))

    @task(1)
    def watch_post(self):
        resp = self.client.get("/posts/1")
        print("Request: GET {} | Status Code: {}".format(resp.url, resp.status_code))





request_success_stats = [list()]
request_fail_stats = [list()]

def hook_request_success(request_type, name, response_time, response_length):
    request_success_stats.append([name, request_type, response_time])

def hook_request_fail(request_type, name, response_time, exception):
    request_fail_stats.append([name, request_type, response_time, exception])

def hook_locust_quit():
    save_success_stats()

def save_success_stats():
    import csv
    with open('success_req_stats.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for value in request_success_stats:
            writer.writerow(value)

events.request_success += hook_request_success
events.request_failure += hook_request_fail
events.quitting += hook_locust_quit

class LocustUser(HttpLocust):
    task_set = SampleTest
    min_wait = 1000
    max_wait = 1000

