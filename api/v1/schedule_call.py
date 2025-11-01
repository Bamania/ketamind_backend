from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from tools.calling_tool import CallingTool  # Assuming this can be instantiated

router = APIRouter()

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Instantiate the calling tool
calling_tool = CallingTool()

class ScheduleRequest(BaseModel):
    phone_number: str
    schedule_time: datetime
    user_id: str

def make_call(phone_number: str, user_id: str):
    """Function to be executed by the scheduler to make a call."""
    try:
        print(f"Executing call to {phone_number} for user {user_id} at {datetime.now()}")
        # You might need to adjust how you call this method based on your CallingTool implementation
        result = calling_tool.call_phone_number(phone_number=phone_number, user_id=user_id)
        print(f"Call result: {result}")
    except Exception as e:
        print(f"Failed to make call to {phone_number}: {e}")

@router.post("/schedule-call")
async def schedule_call(request: ScheduleRequest):
    """
    Schedules a call to a specified phone number at a given time.
    """
    if request.schedule_time < datetime.now():
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future.")

    try:
        scheduler.add_job(
            make_call,
            'date',
            run_date=request.schedule_time,
            args=[request.phone_number, request.user_id]
        )
        return {"message": f"Call scheduled for {request.phone_number} at {request.schedule_time}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule call: {e}")
