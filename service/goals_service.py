from agent import get_user_agent
async def generate_plan(user_id:str,profile:dict)->dict:
    try:
        # logger.info(f"Generating goals for user {user_id} with profile {profile}")
        agent = get_user_agent(user_id)
        response = await agent.arun(f"Generate a goal plan for the user {user_id} with profile {profile}")
        print(response.content)
        return response.content
    except Exception as e:
        # logger.error(f"Error generating goals: {e}")
        raise e