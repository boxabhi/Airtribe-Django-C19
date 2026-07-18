from locust import HttpUser, task, between
import random
from faker import Faker
fake = Faker()
class DjangoAppUser(HttpUser):
    # Simulates a delay between requests for each user (between 1 and 3 seconds)
    wait_time = between(1, 3)

    @task(3)
    def test_homepage(self):
        """Calls the root homepage endpoint"""
        query_params = ["hotel", "booking", "rating", "amenity"]
        selected_param = random.choice(query_params)

        payload = {
            "name" :   fake.name(),
            "email" :  fake.email(),
            "message" : fake.text(),
            "age" : random.randint(18, 65),
        }
        self.client.post("/students/", json=payload)
        self.client.get(f"/?{selected_param}=1")

    @task(2)
    def test_hotels(self):
        """Calls the hotels API list endpoint"""
        self.client.get("/api/hotels/")

    @task(1)
    def test_amenities(self):
        """Calls the amenities API list endpoint"""
        self.client.get("/api/amenities/")