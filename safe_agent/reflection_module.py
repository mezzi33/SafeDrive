import os
import textwrap
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class reflection:
    def __init__(self, temperature: float = 0.0) -> None:
        # Initialize language model based on environment configuration
        api_type = os.getenv("OPENAI_API_TYPE")
        self.llm = ChatOpenAI(
            temperature=temperature,
            model_name=os.getenv("OPENAI_CHAT_MODEL", "gpt-4"),
            max_tokens=1000,
            request_timeout=60)


    def reflection(self, human_message: str, llm_response: str) -> str:
        delimiter = "####"
        
        # Define system instructions for reflection
        system_message = textwrap.dedent(f"""
        You are ChatGPT, a large language model trained by OpenAI. Act as an experienced driving assistant. 
        You will receive a detailed description of a driving scenario along with ChatGPT's previous response to that scenario.

        Your response should identify errors in the reasoning that led to an incorrect decision and suggest a correction.
        
        Response format:
        {delimiter} Analysis of the mistake:
        <Explanation of the error in ChatGPT's original reasoning>
        {delimiter} Suggested improvements:
        <Suggestions for improving reasoning and avoiding such errors>
        {delimiter} Corrected response:
        <Revised response with accurate reasoning and correct action>
        """)

        # Prepare human message with scenario details and ChatGPT's original response
        formatted_human_message = textwrap.dedent(f"""
            ``` Human Message ```
            {human_message}
            ``` ChatGPT Response ```
            {llm_response}

            You know that the action ChatGPT output is not safe, indicating a mistake in the reasoning. 
            Please analyze the error, suggest ways to avoid it, and provide a corrected response.
        """)

        # Prepare messages for LLM
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=formatted_human_message),
        ]

        # Get reflection response from LLM
        response = self.llm(messages).content

        # Split response content by delimiter and extract sections
        sections = response.split(delimiter)
        if len(sections) < 4:
            return "[Error: Reflection response does not match expected format.]"

        # Compile corrected memory entry
        corrected_memory = f"{delimiter} Reflection analysis:\n{sections[1].strip()}\n\n" \
                           f"{delimiter} Suggested improvements:\n{sections[2].strip()}\n\n" \
                           f"{delimiter} Corrected response:\n{sections[3].strip()}"

        return corrected_memory
