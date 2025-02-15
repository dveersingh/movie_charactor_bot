
from locust import HttpUser, task, between

class User(HttpUser):
    wait_time = between(0.1, 0.5)  # 10 req/sec per user
    
    @task
    def chat(self):
        self.client.post("/chat", json={
            "character": "Tony Stark",
            "user_message": "what is arc reactor"
        })