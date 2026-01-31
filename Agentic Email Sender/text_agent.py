from smolagents import CodeAgent, InferenceClientModel
from email_generator import generate_email
from email_sender import send_email

def init_agent():
    system_prompt = """
    You must ALWAYS:
    1. Call generate_email with input ou received first and store result as generated_email.
    2. Then call send_email and give generated_email as input.
    3. Call final_answer(True) or final_answer(False) immediately after send_email
    NO explanation. NO summaries. ONLY the boolean.
    """

    model = InferenceClientModel(provider="together")
    agent = CodeAgent(tools=[generate_email, send_email], model=model, instructions=system_prompt)

    return agent

def initiate_agent(agent, input):
    return agent.run(input)