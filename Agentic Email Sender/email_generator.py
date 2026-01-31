from smolagents import tool
from openai import OpenAI
import os 

@tool
def generate_email(input: str) -> None:
    '''
    Generates the body of an email with given instructions.
    Args:
        input: A string containting instructions for generating the email text. 
    Returns: 
        Email message
    '''

    return "Hello"

    API_KEY=os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=API_KEY);

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="Generate only the main body text of the email. Your email must only contain the body. It will be sent to the user without any changes. Do NOT include placeholders, brackets, or templates",
        input=input
    )

    return response.output[0].content[0].text
