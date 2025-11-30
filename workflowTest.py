from agno.agent import Agent
import os
import asyncio
from typing import AsyncIterator, Union

from agno.agent.agent import Agent

# Import the workflows
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from agno.team import Team

from agno.workflow.step import Step
from agno.workflow.workflow import Workflow
from agno.models.google import Gemini
from agno.workflow import Workflow,Step, StepOutput, StepInput
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
POSTGRES_DB_URL = os.getenv("POSTGRES_AGNO_DB_URL")

model_id = DEFAULT_MODEL
model = Gemini(id=model_id)
# Defining my agents in here
roast_agent = Agent(
        model=model,
      
        name="HabitElevate AI Assistant",
      
        instructions="whatever input you get you try to roast the user for their questions !",

        markdown=True,
        stream_intermediate_steps=False,
        num_history_runs=10,
    )
Bold_agent = Agent(
        model=model,
      
        name="HabitElevate AI Assistant",
      
        instructions="YOU DONT DO ANYTHING JUST RETURN THE INPUT YOU GET IN THE BOLD LETTERS ",

        markdown=True,
        stream_intermediate_steps=False,
        num_history_runs=10,
    )

step1 = Step(
    name="step1",
    description="This step is used to roast the user for their questions",
    agent=roast_agent,
)
step2 = Step(
    name="step2",
    description="This step is used to return the input you get in the bold letters",
    agent=Bold_agent,
)   
# step3 = Step(
#     name="step3",
#     description="This step is used to return the input you get in the bold letters",
#     agent=Bold_agent,
# )   
def customFx(
    step_input:StepInput):
    # return  StepOutput(content="i cant do anything except -->"+step_input.input)
    return StepOutput(content="i cant do anything except -->"+step_input.previous_step_content)

    
  
#TO MAKE THE ABOVE STEP INTO CUSTOM PYTHON FUNCTION ALONG WITH THE AGENT STEPS 
step3 = Step(
    name="step3",
    executor=customFx,
)

# this is the simple step that will get execute,Main input we give ,gets passed to each step !!

workflow = Workflow(
    name="Mixed Execution Pipeline",
    description="This workflow is a mixed execution pipeline that processes the input through a series of steps.EACH Steps output is the input for the next step",
  
    steps=[
            #i can pass the fx with agent or raw python fx in here !
            #so basically pass small function that do tool calling seperately and 
            #each step can now emit a event right !
        step1,
        step2,
        step3 #this is the step3 doesnt run any agent ,just a custom function 
      
    ]
)

if __name__ == "__main__":
    # Try with stream=False to avoid async issues
    try:
        workflow.print_response("Analyze the competitive landscape for fintech startups", markdown=True, stream=False)
    except Exception as e:
        print(f"Error with stream=False: {e}")
        # If that doesn't work, try using asyncio
        async def run_workflow():
            workflow.print_response("Analyze the competitive landscape for fintech startups", markdown=True)
        
        asyncio.run(run_workflow())