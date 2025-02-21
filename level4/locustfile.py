
from locust import HttpUser, task, between

class User(HttpUser):
    wait_time = between(0.3, 0.5)  
    
    @task
    def chat(self):
        self.client.post("/chat", json={
            "character": "Tony Stark",
            "user_message": "what is arc reactor"
        })