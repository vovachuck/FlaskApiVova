from locust import HttpLocust, TaskSet, task
import json


class UserBehavior(TaskSet):
    # runs one time for each user
    def on_start(self):
        self.client.get("/")

    @task(4)
    def create_player(self):
        headers = {'content-type': 'application/json',
                   'Accept-Encoding': 'gzip'}
        self.client.post("/", data=json.dumps({
            "id":"1",
            "name": "vova", "game": "cs go"
        }),
            headers=headers,
            name="Create a new player")

    @task(5)
    def update_player(self):
        headers = {'content-type': 'application/json',
                   'Accept-Encoding': 'gzip'}
        self.client.post("/update/5", data=json.dumps({
            "name": "name12",
            "game": "cs go"
            
        }),
            headers=headers,
            name="Update an name")

    @task(6)  # chance to run 2/3
    def delete(self):
        self.client.delete('/delete/14')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = 3000