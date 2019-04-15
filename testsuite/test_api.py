from time import time, sleep
import pytest

pytestmark = [pytest.mark.django_db]


class JobApi:

    def __init__(self, client):
        self.client = client
        self.id = client.post('/v0/jobs').json()['id']
        self.url = f'/v0/jobs/{self.id}'

    def wait(self, timeout=900):
        t0 = time()

        while time() < t0 + timeout:
            data = self.client.get(self.url).json()

            if data['state'] == 'done':
                break

            assert time() < t0 + timeout, f"Job {self.id} timeout"
            sleep(1)

    def destroy(self):
        return self.client.delete(self.url)


def test_api_home(client):
    resp = client.get('/v0/').json()
    assert resp['version'] == '0.0.1'


def test_api_job_lifecycle(client, after_test):
    job = JobApi(client)
    after_test(job.destroy)
    job.wait()
