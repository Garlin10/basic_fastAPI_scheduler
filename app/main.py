from fastapi import FastAPI
import schedule
import threading
import time
import uvicorn
import logging
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.access")
def job():
    logging.info("Job started.")
    try:
        #Insert your scheduled job here!
        print("Job is running at the momment")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        logging.info("Job finished.")

class SchedulerThread(threading.Thread):
    @classmethod
    def run(cls):
        while True:
            schedule.run_pending()
            time.sleep(1)

scheduler_thread = SchedulerThread()

@app.get("/start")
def start_scheduling():
    if not schedule.jobs:
        schedule.every(2).seconds.do(job)
        if not scheduler_thread.is_alive():
            scheduler_thread.start()
        return {"message": "Scheduling started."}
    return {"message": "Scheduling is already running."}

@app.get("/stop")
def stop_scheduling():
    schedule.clear()
    return {"message": "Scheduling stopped."}

@app.get("/status")
def is_scheduling_running():
    return {"running": bool(schedule.jobs)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")