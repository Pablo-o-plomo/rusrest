import time
from app.services.email_collector import check_email_now

INTERVAL_SECONDS = 600

def run_forever():
    while True:
        try:
            result = check_email_now()
            print(f"[email-worker] processed={result['processed']} failed={result['failed']}")
        except Exception as e:
            print(f"[email-worker] error: {e}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == '__main__':
    run_forever()
