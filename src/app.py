import os
import sys
from dotenv import load_dotenv
from LLMHelper import generate_task_plan, update_task_plan, get_next_action_with_image
from AutoHelper import execute_command
from pyautoguihelper import PyAutoGuiHelper

def main():
    # Load environment variables
    load_dotenv()

    # Initialize PyAutoGuiHelper
    gui_helper = PyAutoGuiHelper()

    # Ask the user for their goal
    goal = input("Please enter your goal: ")
    print(f"Your goal is: {goal}")

    # Generate initial task plan
    task_plan = generate_task_plan(goal)
    print("Generated Task Plan:")
    print(task_plan)

    # Ask user to verify or provide feedback
    feedback = input("Do you agree with this task plan? If not, please provide your feedback: ")
    if feedback.lower() in ['yes', 'y', '']:
        final_task_plan = task_plan
    else:
        final_task_plan = update_task_plan(task_plan, feedback)
        print("Updated Task Plan:")
        print(final_task_plan)

    # Main application loop
    goal_completed = False
    retry_count = 0
    max_retries = 3

    while not goal_completed:
        # Observe: Take a screenshot and draw a box around the cursor position
        cursor_position = gui_helper.get_mouse_position()
        gui_helper.outline_region_on_screen(
            region=(cursor_position.x - 10, cursor_position.y - 10, 20, 20),
            outline_color='red',
            filename='current_state.png'
        )

        # Orient: Analyze the captured state
        print("Current state captured. Sending to LLM for analysis.")

        # Prepare state description
        state_description = f"""
The current task plan is:
{final_task_plan}

You have access to PyAutoGUI functions via the PyAutoGuiHelper class.

The cursor position is highlighted in the image as a red box.

Available functions:
- move_mouse(x, y, duration=0.25)
- move_mouse_relative(dx, dy, duration=0.25)
- click(x=None, y=None, clicks=1, interval=0.0, button='left')
- double_click(x=None, y=None, interval=0.0, button='left')
- right_click(x=None, y=None)
- middle_click(x=None, y=None)
- scroll(clicks, x=None, y=None)
- drag_to(x, y, duration=0.25, button='left')
- drag_rel(dx, dy, duration=0.25, button='left')
- type_text(text, interval=0.0)
- press_key(key)
- hotkey(*keys)
- launch_url_in_default_browser(url)
"""

        # Send state to LLM to get next action
        next_action = get_next_action_with_image(state_description, "current_state.png")
        print("LLM recommended action:")
        print(next_action)

        # Decide: Ask user for approval
        user_input = input("Enter 'LGTM' to proceed, 'Stop' to exit, 'Intervene' to perform the action manually: ")
        if user_input.lower() == 'lgtm':
            # Act: Execute the command
            success = execute_command(next_action, gui_helper)
            if success:
                print("Action executed successfully.")
                retry_count = 0
            else:
                print("Failed to execute action.")
                retry_count += 1
        elif user_input.lower() == 'stop':
            print("Stopping the agent.")
            sys.exit(0)
        elif user_input.lower() == 'intervene':
            print("Please perform the action manually. Press Enter when done.")
            input()
            retry_count = 0
        else:
            print("Invalid input.")

        # Verify if goal is completed
        goal_status = input("Is the goal completed? (yes/no): ")
        if goal_status.lower() in ['yes', 'y']:
            goal_completed = True
            print("Goal completed.")
        else:
            retry_count += 1
            if retry_count >= max_retries:
                print("Maximum retries reached. Exiting.")
                sys.exit(0)

if __name__ == "__main__":
    main()
