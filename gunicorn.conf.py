import os


bind = "0.0.0.0:" + os.getenv(
    "PORT",
    "5000"
)

workers = int(
    os.getenv(
        "WEB_WORKERS",
        "2"
    )
)

threads = int(
    os.getenv(
        "WEB_THREADS",
        "4"
    )
)

timeout = int(
    os.getenv(
        "WEB_TIMEOUT",
        "120"
    )
)

keepalive = 5

accesslog = "-"
errorlog = "-"

capture_output = True

preload_app = False
