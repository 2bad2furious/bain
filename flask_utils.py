import os
import signal


def stop_server():
    os.kill(os.getpid(), signal.SIGTERM)
