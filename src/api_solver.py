# from google import genai
# from google.genai import types

# client = genai.Client(api_key="AIzaSyCmeWQRKpH0WfDyVJmU3wJcDsQlPx1Y6B0")

# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Explain how AI works"
# )

# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents=["Explain how AI works"],
#     config=types.GenerateContentConfig(
#         max_output_tokens=500,
#         temperature=0.1
#     )
# )
# print(response.text)

# sys_instruct="You are a cat. Your name is Neko."
# client = genai.Client(api_key="GEMINI_API_KEY")

# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     config=types.GenerateContentConfig(
#         system_instruction=sys_instruct),
#     contents=["your prompt here"]
# )

# chat = client.chats.create(model="gemini-2.0-flash")
# response = chat.send_message("I have 2 dogs in my house.")
# print(response.text)
# response = chat.send_message("How many paws are in my house?")
# print(response.text)
# for message in chat._curated_history:
#     print(f'role - ', message.role, end=": ")
#     print(message.parts[0].text)

import json
from pathlib import Path
import logging
from google import genai
from google.genai import types
from schema import Problem, Solution
import re

# Initialize Gemini Client
client = genai.Client(api_key="AIzaSyCmeWQRKpH0WfDyVJmU3wJcDsQlPx1Y6B0")  # Replace with your actual API key

def read_problem(problem_id, folder_path=Path("../sample-data/puzzles")):
    """Reads a specific problem from the problem folder."""
    file_path = folder_path / f"{problem_id}.json"
    
    if not file_path.exists():
        logging.error(f"Problem file {file_path} does not exist.")
        return None

    with open(file_path, 'r') as f:
        problem_data = json.load(f)
    
    return Problem(**problem_data)


def generate_solution(problem: Problem):
    """Uses Gemini API to generate a solution for the given problem."""

    # sys_instruct = """
    #     Return the solution as a list of transition indices (0-based) that transform the initial string to an empty string.
    #     Don't provide the code but only the list of transitions. (the only things in curly braces must be the solution). 
    
    #     Format:
    #     {{
    #         "problem_id": "{problem.problem_id}",
    #         "solution": [0, 1, 2]
    #     }}

    #     1. Keep track of the string under consideration and keep on applying the transitions until the string converts to an empty string...
    #     2. Always check which all transitions have the left side present in the current state of the string, only try to apply the valid transitions.
    #     3. Try to reach the empty state of the string being tracked.
    #     4. There is no limit on the number of iterations required.
    # """

    file = open("prompt_cot.txt", "r", encoding='utf-8')
    sys_instruct = file.read()
    file.close()

    # Craft the prompt based on the problem data
    prompt = f"""
    You are given an initial string: '{problem.initial_string}'. This is problem {problem.problem_id}. 
    Transitions:
    {json.dumps([{"src": t.src, "tgt": t.tgt} for t in problem.transitions], indent=2)}
    """

    # Send the prompt to Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            max_output_tokens=5000,
            # temperature=0.05,  # Slight randomness
            system_instruction=sys_instruct
        ),
    )

    # print(response)

    print(response.text)
    match = re.search(r'\{.*\}', response.text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            solution_data = json.loads(json_str)
            print(solution_data)
            return Solution(**solution_data)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
    else:
        logging.error("No JSON found in response.")

    # # Parse the model's response
    # try:
    #     print(response.text[8:-4])

    #     solution_data = json.loads(response.text[8:-4])
    #     return Solution(**solution_data)
    # except (json.JSONDecodeError, KeyError) as e:
    #     logging.error(f"Error parsing Gemini response: {e}")
    #     return None


# def save_solution(solution: Solution, folder_path=Path("../sample-data/solutions")):
#     """Saves the solution to the solutions folder."""
#     folder_path.mkdir(parents=True, exist_ok=True)
#     file_path = folder_path / f"{solution.problem_id}.json"

#     with open(file_path, 'w') as f:
#         f.write(solution.json(indent=4))

#     logging.info(f"Solution for problem {solution.problem_id} saved at {file_path}")

def save_solution(solution, path=Path("../sample-data/solutions3")):
    path.mkdir(exist_ok=True)
    file_path = path / f"{solution.problem_id}.json"
    
    logging.info(f"Saving solution for problem {solution.problem_id}...")
    with open(file_path, 'w') as f:
        f.write(solution.model_dump_json(indent=4))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example problem ID
    
    for i in range(0, 11) :
        problem_id = str(i).zfill(3)

        # Read the problem
        problem = read_problem(problem_id)
        
        if problem:
            # Generate solution using Gemini
            solution = generate_solution(problem)
            # print(solution.text)
            # print(solution)
            
            if solution:
                # Save the solution to the solutions folder
                save_solution(solution)
            else:
                logging.error("Failed to generate a valid solution.")
        else:
            logging.error("Problem could not be loaded.")
