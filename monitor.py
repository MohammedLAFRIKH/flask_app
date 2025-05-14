import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def monitor_app():
    url = "http://127.0.0.1:5000/health"
    retries = 3
    while True:
        for attempt in range(retries):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    logging.info("Application is running: %s", response.json())
                    break
                else:
                    logging.warning("Application is not healthy! Status code: %d", response.status_code)
            except Exception as e:
                logging.error("Error connecting to the application: %s", e)
            time.sleep(5)
        time.sleep(10)

if __name__ == "__main__":
    monitor_app()
