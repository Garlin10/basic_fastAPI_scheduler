from fastapi import FastAPI
import schedule
import threading
import time

app = FastAPI()

# Job Scheduler Code
class JobScheduler:
    def __init__(self):
        self.job = None
        self.is_job_scheduled = False

    def do_job(self):
        print("Job is running...")

    def start_job(self):
        if not self.is_job_scheduled:
            self.job = schedule.every(1).seconds.do(self.do_job)
            self.is_job_scheduled = True
            return "Job started."
        else:
            return "Job is already scheduled."

    def stop_job(self):
        if self.is_job_scheduled:
            schedule.cancel_job(self.job)
            self.is_job_scheduled = False
            return "Job stopped."
        else:
            return "No job is scheduled."

    def get_job_status(self):
        return "Scheduled" if self.is_job_scheduled else "Not scheduled"

scheduler = JobScheduler()

# Endpoint to start the job
@app.get("/start-job")
def start_job():
    return {"message": scheduler.start_job()}

# Endpoint to stop the job
@app.get("/stop-job")
def stop_job():
    return {"message": scheduler.stop_job()}

# Endpoint to get job status
@app.get("/job-status")
def job_status():
    return {"status": scheduler.get_job_status()}

# Background task to run scheduled jobs
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the background task
threading.Thread(target=run_schedule, daemon=True).start()

# Run the server
# uvicorn.run(app, host="0.0.0.0", port=8000)