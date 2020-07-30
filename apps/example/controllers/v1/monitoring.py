import time
import sys

# You don't need to import jaguar utils, it is loaded
# from jaguar.http_status_codes import HTTP_200

## Write your endpoints, prefix with HTTP method:


def get_ping2() -> dict:
    "a simple endpoint without authentication for monitoring"
    status = J.HTTP_202
    print(locals(), file=sys.stderr)
    sys.stderr.flush()
    auth = False
    return dict(message="pong")


def get_farshid():
    return {"wow": "you are awesome3"}


def options_ping() -> dict:
    "a simple endpoint without authentication for monitoring"
    status = J.HTTP_200
    auth = False
    return dict(message="pong")


def post_time(params) -> dict:
    status = J.HTTP_201
    return dict(message=params.time)
