import os
import yaml
import numpy as np
from safe_agent.reasoning_module import reasoning
from safe_agent.reflection_module import reflection
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document


# Function to retrieve similar cases
def retrieve_similar_cases(test_case_description, vector_store, top_k=5):
    similarity_results = vector_store.similarity_search_with_score(test_case_description, k=top_k)
    fewshot_messages = [result.metadata.get("human_question", "") for result, _ in similarity_results]
    fewshot_answers = [result.metadata.get("LLM_response", "") for result, _ in similarity_results]
    return fewshot_messages, fewshot_answers


# Function to parse test case files
def parse_test_case(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        scenario_description = ""
        expected_response = None
        parsing_scenario = False

        for line in lines:
            line = line.strip()
            if line.startswith("Scenario:"):
                parsing_scenario = True
                continue
            elif line.startswith("response: ####"):
                try:
                    expected_response = int(line.split("####")[1].strip())
                except (IndexError, ValueError):
                    print(f"Error parsing expected response in {file_path}")
                parsing_scenario = False

            if parsing_scenario:
                scenario_description += line + " "

        return scenario_description.strip(), expected_response


# Configuration setup
with open("config.yaml", 'r') as file:
    config = yaml.safe_load(file)

os.environ["OPENAI_API_TYPE"] = config.get("OPENAI_API_TYPE", "openai")
os.environ["OPENAI_API_KEY"] = config.get("OPENAI_KEY", "")
os.environ["OPENAI_CHAT_MODEL"] = config.get("OPENAI_CHAT_MODEL", "")

reflection_module_enabled = config.get("reflection_module", False)
few_shot_num = config.get("few_shot_num", 3)

# Paths
test_case_folder = "./test_cases"
memory_path = "./memories"

# Initialize embeddings, vector store, and agents
embedding_function = OpenAIEmbeddings()
vector_store = Chroma(embedding_function=embedding_function, persist_directory=memory_path)
driver_agent = reasoning(temperature=0.5, verbose=True)
reflection_agent = reflection() if reflection_module_enabled else None

# Process test cases
print("Processing test cases...")
for idx, filename in enumerate(os.listdir(test_case_folder)):
    if filename.endswith(".txt"):
        file_path = os.path.join(test_case_folder, filename)
        scenario_description, expected_response = parse_test_case(file_path)

        # Retrieve few-shot examples
        fewshot_messages, fewshot_answers = retrieve_similar_cases(scenario_description, vector_store, top_k=few_shot_num)

        # Define available actions
        available_actions = """
        IDLE - remain in the current lane with current speed, Action_id: 0
        Turn-left - change lane to the left of the current lane, Action_id: 1
        Turn-right - change lane to the right of the current lane, Action_id: 2
        Acceleration - accelerate the vehicle Action_id: 3
        Decelerate -decelerate the vehicle Action_id: 4
        """

        # Use DriverAgent to decide
        action, response_content, human_message, few_shot_answers_store = driver_agent.few_shot_decision(
            scenario_description=scenario_description,
            previous_decisions="No previous decisions",
            available_actions=available_actions,
            driving_intensions="Drive safely and avoid collisions",
            fewshot_messages=fewshot_messages,
            fewshot_answers=fewshot_answers
        )

        # Log results
        is_correct = action == expected_response
        with open("simulation_results.txt", "a") as log_file:
            log_file.write(f"Test Case {idx + 1}: {filename}\n")
            log_file.write(f"Scenario Description:\n{scenario_description}\n")
            log_file.write(f"Model Response: {action}\n")
            log_file.write(f"Expected Response: {expected_response}\n")
            log_file.write(f"Correct: {is_correct}\n")
            log_file.write(f"Reasoning Process:\n{response_content}\n\n")

        # Reflection for incorrect responses
        if not is_correct and reflection_module_enabled:
            corrected_response = reflection_agent.reflection(human_message, response_content)

            with open("reflections.txt", "a") as reflection_log_file:
                reflection_log_file.write(f"Test Case {idx + 1}: {filename}\n")
                reflection_log_file.write(f"Scenario Description:\n{scenario_description}\n")
                reflection_log_file.write(f"Original Reasoning:\n{response_content}\n")
                reflection_log_file.write("Reflection Analysis:\n")
                reflection_log_file.write(f"{corrected_response}\n\n")

            doc = Document(
                page_content=scenario_description,
                metadata={"human_question": human_message, "LLM_response": corrected_response, "action": action, "comments": "Reflection correction"}
            )
            vector_store.add_documents([doc])
            vector_store.persist()

        print(f"Test Case {idx + 1}: {filename} processed.")

print("All test cases processed.")
