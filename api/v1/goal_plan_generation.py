"""
Goal Plan Generation API
Generates personalized habit plans based on user goals and profile using Agno Agent
"""

from fastapi import APIRouter, HTTPException, Body  
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from service.goals_service import generate_plan
router = APIRouter()


class UserProfile(BaseModel):
    age: Optional[int] = None
    schedule: Optional[str] = None
    goals: Optional[List[str]] = []
    challenges: Optional[List[str]] = []
    currenthabits: Optional[List[str]] = []
    description: Optional[str] = None


class GoalData(BaseModel):
    primary_goal: str
    goal_duration: int
    duration_type: str  # 'days', 'weeks', or 'months'


class GeneratePlanRequest(BaseModel):
    user_id: str
    profile: UserProfile
    goal: GoalData


class GeneratePlanResponse(BaseModel):
    success: bool
    plan:Any = Field(default=None,description="The generated plan")

@router.post("/generate-goal-plan", response_model=GeneratePlanResponse)
async def generate_goal_plan_endpoint(request: GeneratePlanRequest = Body(...)):
    """
    Generate a personalized goal achievement plan using Agno Agent
    
    Args:
        request: Contains user_id, profile data, and goal information
        
    Returns:
        Success status and the generated plan as structured JSON
    """
    try:
        # Validate required fields
        if not request.user_id or not request.goal.primary_goal:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Convert profile to dict
        print('request body ! ', request);
        profile_dict = {
            "age": request.profile.age,
            "schedule": request.profile.schedule,
            "goals": request.profile.goals,
            "challenges": request.profile.challenges,
            "currenthabits": request.profile.currenthabits,
            "description": request.profile.description
        }
        
        # Convert goal to dict
        # goal_dict = {
        #     "primary_goal": request.goal.primary_goal,
        #     "goal_duration": request.goal.goal_duration,
        #     "duration_type": request.goal.duration_type
        # }
        
        # # Include goal information in profile for generation
        # profile_dict["goal"] = goal_dict
        
        # Generate the plan using chat service
        plan = await generate_plan(
            user_id=request.user_id,
            profile=profile_dict
        )
        print("planrecived from the generate goal fx ",plan)
        
        return GeneratePlanResponse(
            success=True,
            plan=plan
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

