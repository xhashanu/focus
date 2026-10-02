from app.workers.tasks import process_news_link

class DummySelf:
    class DummyRequest:
        id = "test-123"
        retries = 3
    request = DummyRequest()
    def update_state(self, **kwargs):
        print(f"Update state: {kwargs}")
    def retry(self, exc):
        return exc

try:
    process_news_link(DummySelf(), "https://www.youtube.com/watch?v=ya2kFq8qcBI")
except Exception as e:
    print(f"Exception caught: {e}")
