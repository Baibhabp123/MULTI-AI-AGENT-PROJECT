import subprocess
import threading
import time

from dotenv import load_dotenv

from app.common.logger import get_logger


load_dotenv()

logger = get_logger(__name__)


def run_backend():

    try:

        logger.info("Starting backend server...")

        subprocess.run(
            [
                "uvicorn",
                "app.backend.api:app",
                "--host",
                "127.0.0.1",
                "--port",
                "9999"
            ],
            check=True
        )

    except Exception as e:

        logger.exception(
            f"Backend service failed: {e}"
        )


def run_frontend():

    try:

        logger.info("Starting frontend server...")

        subprocess.run(
            [
                "streamlit",
                "run",
                "app/frontend/ui.py"
            ],
            check=True
        )

    except Exception as e:

        logger.exception(
            f"Frontend service failed: {e}"
        )


if __name__ == "__main__":

    backend_thread = threading.Thread(
        target=run_backend,
        daemon=True
    )

    backend_thread.start()

    time.sleep(3)

    run_frontend()