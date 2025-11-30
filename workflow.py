from agno.agent import Agent
import os
from agno.models.google import Gemini
from agno.workflow import Workflow, StepOutput
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
POSTGRES_DB_URL = os.getenv("POSTGRES_AGNO_DB_URL")
model_id = DEFAULT_MODEL
model = Gemini(id=model_id)
def data_preprocessor(step_input):
    data_preprocessor_agent = Agent(
        model=model,
      
        name="HabitElevate AI Assistant",
      
        instructions="whatever input you get you try to roast the user for their questions !",

        markdown=True,
        stream_intermediate_steps=False,
        num_history_runs=10,
    )
    print("inside the dataPreprocessor")
    response = data_preprocessor_agent.run(step_input.input)
  
    return StepOutput(content=f"Processed: {response}") 
def howitworksAgent(step_input):
    agent = Agent(
        model=model,
      
        name="HabitElevate AI Assistant",
      
        instructions="YOU DONT DO ANYTHING JUST RETURN THE INPUT YOU GET IN THE BOLD LETTERS ",

        markdown=True,
        stream_intermediate_steps=False,
        num_history_runs=10,
    )
  
    query = step_input.input if hasattr(step_input, 'input') else "ARE HUMANS IMMORTAL?"
    
    # Run the agent synchronously (non-streaming for simplicity)
    try:
        response = agent.run(query)
        
        # Extract content from response
        if hasattr(response, 'content'):
            final_content = response.content
        elif hasattr(response, 'output') and hasattr(response.output, 'content'):
            final_content = response.output.content
        else:
            final_content = str(response)
            
        return StepOutput(content=f"Processed: {final_content}")
    except Exception as e:
        print(f"Error in howitworksAgent: {e}")
        return StepOutput(content=f"Error: {str(e)}")
def step2(step_input):
    # Custom preprocessing logic
    # print(step_input)
    print("inside the step 2")
    # Or you can also run any agent/team over here itself
    finalResponse="i cant do anything except -->"
    # response = some_agent.run(...)
    return StepOutput(content=f"Processed: {finalResponse+step_input.input}") # <-- Now pass the agent/team response in content here

workflow = Workflow(
    name="Mixed Execution Pipeline",
    description="This workflow is a mixed execution pipeline that processes the input through a series of steps.EACH Steps output is the input for the next step",
  
    steps=[
            #i can pass the fx with agent or raw python fx in here !
            #so basically pass small function that do tool calling seperately and 
            #each step can now emit a event right !
        data_preprocessor,  # Function
        howitworksAgent,
        step2
      
    ]
)

workflow.print_response("Analyze the competitive landscape for fintech startups", markdown=True)