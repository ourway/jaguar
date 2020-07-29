import time

# You don't need to import jaguar utils, it is loaded
# from jaguar.http_status_codes import HTTP_200

## Write your endpoints, prefix with HTTP method:


def get_ping() -> dict:
    "a simple endpoint without authentication for monitoring"
    status = HTTP_200
    auth = False
    return dict(message="pong")
