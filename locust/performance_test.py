from string import ascii_lowercase

from locust import HttpUser, task, between
import json
from faker import Faker
import random
from random import randint


def make_fake():
    fake = Faker("en_US")
    return {
        "foo": randint(0, 100),
        "bar": "".join([random.choice(ascii_lowercase) for _ in range(10_000_000)]),
    }


class PerformanceTests(HttpUser):
    wait_time = between(0, 0)

    @task(1)
    def testFastApi(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.client.post("/dumps", data=json.dumps(make_fake()), headers=headers)

    @task(20)
    def testGetFastApi(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.client.get(f"/dumps", headers=headers)
