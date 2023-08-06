import json

from faker import Faker

from locust import HttpUser, between, task

fake = Faker()


def make_fake():
    return fake.json(
        data_columns={"Spec": "@1.0.1", "ID": "pyint", "Details": {"Name": "name", "Address": "address"}},
        num_rows=1,
    )


class PerformanceTests(HttpUser):
    wait_time = between(0, 3)

    @task(1)
    def testPostFastApi(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.client.post("/dumps", data=json.dumps(make_fake()), headers=headers)

    @task(5)
    def testGetFastApi(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.client.get(f"/dumps/57000", headers=headers)
