import os
import textwrap
import time
from rich import print
from typing import List
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks import OpenAICallbackHandler

# Define delimiter for separating sections in messages
delimiter = "####"

class reasoning:
    def __init__(self, temperature: float = 0.0, verbose: bool = False) -> None:
        oai_api_type = os.getenv("OPENAI_API_TYPE")
        
        # Initialize LLM based on environment configuration
        if oai_api_type == "azure":
            print("Using Azure Chat API")
            self.llm = AzureChatOpenAI(
                deployment_name=os.getenv("AZURE_CHAT_DEPLOY_NAME"),
                temperature=temperature,
                max_tokens=2000,
                request_timeout=60,
                streaming=True,
            )
        elif oai_api_type == "openai":
            print("Using OpenAI API")
            self.llm = ChatOpenAI(
                temperature=temperature,
                model_name=os.getenv("OPENAI_CHAT_MODEL", "gpt-4"),
                max_tokens=2000,
                request_timeout=60,
                streaming=True,
            )
        else:
            raise ValueError("Unsupported API type. Set OPENAI_API_TYPE to either 'azure' or 'openai'.")

    # Modify the few_shot_decision method in the DriverAgent class to add extra instructions in human_message
# Modify the few_shot_decision method in the DriverAgent class
    def few_shot_decision(
        self,
        scenario_description: str,
        previous_decisions: str,
        available_actions: str,
        driving_intensions: str,
        fewshot_messages: List[str],
        fewshot_answers: List[str]
    ):
        # Define the system message to guide the assistant
        system_message = textwrap.dedent(f"""
        You are ChatGPT, a mature driving assistant. You will be given a detailed driving scenario description,
        previous decisions, available actions, and driving intentions. Analyze these inputs to choose the best action.

        Your response format should follow:
        <reasoning>
        <reasoning>
        <repeat reasoning steps until a decision is reached>
        Response to user:{delimiter} <output only the Action_id as an integer for the chosen action, e.g., if decelerate, output `4`>
        """)

        # Combine few-shot examples
        messages = [SystemMessage(content=system_message)]
        for i in range(len(fewshot_messages)):
            messages.append(HumanMessage(content=fewshot_messages[i]))
            messages.append(AIMessage(content=fewshot_answers[i]))

        # Additional guidance message, appended right after the few-shot examples
        additional_guidance = textwrap.dedent(f"""
        In the scenario description, there will be a navigation instruction to follow. You should first check if you can change lane according to the navigation, and then consider other safe actions.
        When making a decision, you should consider all vehicles that will be involved by the decision in the surroundings, from different aspects, including time headway, time to collision, responsibility-sensitive safety. You can use all your knowledge to make decisions. 
        The few-shot answers template passed by AI message is just an example of reasoning steps. Feel free to come up with better structures and more comprehensive thoughts that help choose a reasonable action.
        """)

        # Prepare the human message for current scenario and actions
        human_message = textwrap.dedent(f"""
        Current Scenario:
        {delimiter} Driving scenario description:
        {scenario_description}
        {delimiter} Driving Intentions:
        {driving_intensions}
        {delimiter} Available actions:
        {available_actions}

        Stop reasoning once you have a valid action.
        """)

        # Add additional guidance and scenario details to the message list
        messages.append(HumanMessage(content=additional_guidance + "\n" + human_message))

        # Initialize the response without printing the chunks
        response_content = ""
        for chunk in self.llm.stream(messages):
            response_content += chunk.content

        # Extract the decision action
        decision_action = response_content.split(delimiter)[-1].strip()
        try:
            result = int(decision_action)
            if result < 0 or result > 4:
                raise ValueError
        except ValueError:
            # Handle invalid output
            check_message = textwrap.dedent(f"""
            Please verify and provide only a single integer Action_id (0-4) based on the following output:
            {delimiter} Received output:
            {decision_action}
            """)
            messages = [HumanMessage(content=check_message)]
            check_response = self.llm(messages)
            result = int(check_response.content.split(delimiter)[-1].strip())

        few_shot_answers_store = "\n---------------\n".join(fewshot_answers)
        return result, response_content, human_message, few_shot_answers_store
