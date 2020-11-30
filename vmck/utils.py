import logging
import os
import secrets
import string
from socket import gethostname
from time import sleep

log = logging.getLogger(__name__)
vocabulary_64 = string.ascii_letters + string.digits + '.+'
hostname = os.environ.get('HOST', gethostname())


def random_code(length, vocabulary=vocabulary_64):
    return ''.join(secrets.choice(vocabulary) for _ in range(length))


def is_true(value):
    text = (value or '').lower().strip()
    return text in ['1', 'yes', 'true', 'on', 'enabled']


def retry(count=4, wait_sec=1, exp=2):
    def _retry(f):
        def wrapper(*args, **kwargs):
            current_wait = wait_sec
            for i in range(count):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    if i == count - 1:
                        log.exception(e)
                        raise

                    log.warning(
                        "%s() - #%s/%s retrying in %s sec",
                        f.__qualname__,
                        i + 1,
                        count,
                        current_wait,
                    )
                    sleep(current_wait)
                    current_wait = int(current_wait * exp)
                    continue
        return wrapper

    return _retry
