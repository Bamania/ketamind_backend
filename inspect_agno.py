from agno.workflow import  Workflow
from agno.agent import Agent
from agno.team import Team
import inspect

# print("Step init parameters:", inspect.signature(Step.__init__))
print("Workflow init parameters:", inspect.signature(Workflow.__init__))
print("Is Team an instance of Agent?", issubclass(Team, Agent))
