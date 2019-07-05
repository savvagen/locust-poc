from locust import HttpLocust, TaskSet, task

class MyTaskSet(TaskSet):
    @task
    def get_user_userId(self):
        self.client.get("/svc-gateway/svc-user/user/{0}".format("undefined"), name="/user/{userId}")

    @task
    def get_user_guid_publicUserGuid(self):
        self.client.get("/svc-gateway/svc-user/user/guid/{0}".format("undefined"), name="/user/guid/{publicUserGuid}")

    @task
    def get_user_userId_employment(self):
        self.client.get("/svc-gateway/svc-user/user/{0}/employment".format("undefined"), name="/user/{userId}/employment")

    @task
    def get_user_userId_employmentdetails(self):
        self.client.get("/svc-gateway/svc-user/user/{0}/employmentdetails".format("undefined"), name="/user/{userId}/employmentdetails")

    @task
    def get_user_userId_employer(self):
        self.client.get("/svc-gateway/svc-user/user/{0}/employer".format("undefined"), name="/user/{userId}/employer")

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 1000
    max_wait = 3000

