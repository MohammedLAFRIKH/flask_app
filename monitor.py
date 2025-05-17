import subprocess
import time
import requests

FLASK_URL = "http://127.0.0.1:5000/"
CHECK_INTERVAL = 10  # secondes

def is_flask_running():
    try:
        response = requests.get(FLASK_URL, timeout=3)
        return response.status_code == 200
    except Exception:
        return False

def start_flask():
    # Démarre l'application Flask en arrière-plan
    return subprocess.Popen(["python", "app.py"])

if __name__ == "__main__":
    flask_process = None
    while True:
        if not is_flask_running():
            print("Flask n'est pas en cours d'exécution. Redémarrage...")
            if flask_process:
                flask_process.terminate()
            flask_process = start_flask()
        else:
            print("Flask fonctionne correctement.")
        time.sleep(CHECK_INTERVAL)
