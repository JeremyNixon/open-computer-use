import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai_client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
task_planner_model = os.getenv("TASK_PLANNER_MODEL", "gpt-4o")

def generate_task_plan(goal):
    prompt = f"Generate a detailed task plan to achieve the following goal but only within the scope of actions that can be performed on a computer:\\n\\n{goal}"

    # Make the API call
    response = openai_client.chat.completions.create(
        model=task_planner_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    initial_task_plan = response.choices[0].message.content.strip()
    return initial_task_plan

def update_task_plan(initial_task_plan, user_feedback):
    prompt = f"The initial task plan is:\\n{initial_task_plan}\\n\\nUser feedback:\\n{user_feedback}\\n\\nProvide an updated task plan incorporating the user's feedback."
    response = openai_client.chat.completions.create(
        model=task_planner_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    updated_task_plan = response.choices[0].message.content.strip()
    return updated_task_plan

def get_next_action_with_image(state_description, image_path):
    # Assuming we can send image to GPT-4 Vision
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    response = openai_client.chat.completions.create(
        model="gpt-4-vision",
        messages=[{"role": "system", "content": state_description}],
        files=[{"name": "current_state.png", "bytes": image_data}],
        max_tokens=200,
        temperature=0.7,
    )
    action = response.choices[0].message.content.strip()
    return action
