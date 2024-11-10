import os
import time
import pyautogui
import subprocess
from PIL import Image, ImageDraw, ImageFont
import io
from dotenv import load_dotenv
import base64
import numpy as np

def add_coordinate_labels(image_array, step=50):
    """
    Adds coordinate labels with arrows to an image for pixel positions.
    
    Args:
        image_array: numpy array of the image
        step: spacing between labeled points (default 50 pixels)
    
    Returns:
        PIL Image with coordinate labels and arrows
    """
    # Convert numpy array to PIL Image for drawing
    image = Image.fromarray(image_array)
    draw = ImageDraw.Draw(image)
    
    # Try to load a system font, fall back to default if not found
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    height, width = image_array.shape[:2]
    
    # Create coordinate points grid
    for y in range(0, height, step):
        for x in range(0, width, step):
            # Draw arrow
            arrow_length = 20
            arrow_color = (255, 0, 0)  # Red color for visibility
            
            # Calculate arrow endpoint (offset from point for visibility)
            end_x = x + 15
            end_y = y - 15
            
            # Draw arrow line
            draw.line([(end_x, end_y), (x, y)], fill=arrow_color, width=1)
            
            # Draw arrowhead
            arrow_size = 5
            draw.polygon([
                (x, y),
                (x + arrow_size, y - arrow_size),
                (x - arrow_size, y - arrow_size)
            ], fill=arrow_color)
            
            # Add coordinate text
            text = f"({x}, {y})"
            text_bbox = draw.textbbox((end_x, end_y), text, font=font)
            
            # Draw white background for text for better visibility
            draw.rectangle([
                (text_bbox[0]-2, text_bbox[1]-2),
                (text_bbox[2]+2, text_bbox[3]+2)
            ], fill=(255, 255, 255))
            
            # Draw coordinate text
            draw.text((end_x, end_y), text, fill=(0, 0, 0), font=font)
    
    return image

def convert_coordinates_to_mac_os_4k_for_pyautogui(x, y):
    """
    Convert coordinates from Mac OS 4K resolution to PyAutoGUI coordinates.
    
    Args:
        x: x-coordinate in Mac OS 4K resolution
        y: y-coordinate in Mac OS 4K resolution
    
    Returns:
        Tuple of converted PyAutoGUI coordinates
    """
    # Mac OS 4K resolution
    mac_os_4k_width = 3840
    mac_os_4k_height = 2160
    
    # PyAutoGUI default resolution
    pyautogui_width, pyautogui_height = pyautogui.size()
    
    # Convert coordinates to PyAutoGUI resolution
    x_new = x * pyautogui_width / mac_os_4k_width
    y_new = y * pyautogui_height / mac_os_4k_height
    
    return x_new, y_new

class ScreenshotProcessor:
    def __init__(self, client):
        print("Initializing...")
        self.client = client

        # Configure PyAutoGUI settings
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True
        
    def take_screenshot(self) -> str:
        """Take a screenshot and save it temporarily."""
        # Create screenshots directory if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        
        screenshot = pyautogui.screenshot()
        
        # Convert PIL Image to numpy array
        screenshot_array = np.array(screenshot)
        
        # Add coordinate labels
        labeled_screenshot = add_coordinate_labels(screenshot_array)
        
        # Save screenshot to bytes
        img_byte_arr = io.BytesIO()
        labeled_screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Save to file temporarily
        datetime_yyyy_mm_dd_hh_mm_ss = time.strftime("%Y%m%d_%H%M%S")
        temp_path = f"./screenshots/temp_screenshot-{datetime_yyyy_mm_dd_hh_mm_ss}.png"
        labeled_screenshot.save(temp_path)
        
        return temp_path

    def generate_automation_code(self, screenshot_path: str, instruction: str) -> str:
        """Generate automation code using OpenAI's API."""
        try:
            # Read the image file
            with open(screenshot_path, "rb") as image_file:
                image_data = image_file.read()
            
            # Create messages for the API
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert Python automation engineer specializing in PyAutoGUI. 
                    Generate precise Python code to automate user interface interactions based on screenshots and instructions. 
                    The code should be properly formatted without indentation at the root level.
                    Include necessary imports and use time.sleep() for proper timing.
                    Use pyautogui functions and focus on accurate coordinates from the labeled screenshot.
                    Return only executable Python code at the beginning and a quick explanation of why the coordinate was chosen 
                    at the end.
                    Label the quick explanation with the keyword Explanation. 
                    Make sure your co-ordinates are accurate for mac retina 4k resolution, 
                    for example (960,600) should be (170,450)"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Generate PyAutoGUI code to: {instruction}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"
                            }
                        }
                    ]
                }
            ]

            # Make the API call
            response = self.client.chat.completions.create(
                model=os.getenv("VISION_MODEL"),
                messages=messages,
                max_tokens=4000,
                temperature=0.0,
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating automation code: {str(e)}")
            return None

    def process_screenshot_and_generate_code(self, instruction: str) -> tuple:
        """Process screenshot and generate automation code."""
        try:
            # Take screenshot
            screenshot_path = self.take_screenshot()
            
            # Generate automation code
            generated_code = self.generate_automation_code(screenshot_path, instruction)
            
            return screenshot_path, generated_code
            
        except Exception as e:
            print(f"Error processing screenshot: {str(e)}")
            return None, None


def grab_explanation(code: str) -> str:
        """
        Extracts text from the keyword 'Explanation' to the end of the string.
        
        Args:
            code: Input string that may contain an explanation
            
        Returns:
            The extracted explanation text, or empty string if no explanation found
        """
        if "Explanation" not in code:
            return ""
        
        # Find the index where 'Explanation' starts
        explanation_index = code.find("Explanation")
        
        # Return everything from 'Explanation' to the end
        return code[:explanation_index], code[explanation_index:]


def clean_code(code: str) -> str:
    """Remove markdown formatting and clean the code for execution."""
    # Remove markdown code blocks
    code = code.replace("```python", "").replace("```", "")
    # Remove leading/trailing whitespace
    code = code.strip()
    # Ensure no indentation at root level
    lines = code.split('\n')
    cleaned_lines = [line.strip() for line in lines]
    return '\n'.join(cleaned_lines)

def create_execution_environment():
    """Create a safe execution environment with necessary imports."""
    namespace = {
        'pyautogui': pyautogui,
        'time': time,
        'subprocess': subprocess,
    }
    
    # Configure PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 1
    
    return namespace

def main():
    """Main execution function."""
    load_dotenv()  # Load environment variables from .env file
    
    # Create screenshots directory if it doesn't exist
    os.makedirs("screenshots", exist_ok=True)
    
    try:
        if not os.getenv('OPENAI_API_KEY'):
            print("Error: OPENAI_API_KEY not found in environment variables")
            return
        
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
        processor = ScreenshotProcessor(client)
        
        instruction = input("What action would you like to automate? ")
        
        # Fixed: Changed process_screenshot to process_screenshot_and_generate_code
        screenshot_path, generated_code = processor.process_screenshot_and_generate_code(instruction)
        
        if not generated_code:
            print("Failed to generate automation code")
            return
            
        code, explanation = grab_explanation(generated_code)

        print(explanation)

        # Clean the code before displaying and executing
        cleaned_code = clean_code(code)
        
        print("\nGenerated Python code:")
        print(cleaned_code)
        
        confirmation = input("\nWould you like to execute this code? (yes/no): ")
        PREPARE_TIME = 0  # Time to prepare before execution
        
        if confirmation.lower() == 'yes':
            print(f"Executing automation in {PREPARE_TIME} seconds...")
            try:
                # Create execution environment
                exec_env = create_execution_environment()
                
                # Wait for preparation time
                time.sleep(PREPARE_TIME)
                
                # Execute the cleaned code in the prepared environment
                exec(cleaned_code, exec_env)
                
            except Exception as e:
                print(f"Error executing automation: {str(e)}")
                print("Detailed error info:", e.__class__.__name__)
        else:
            print("Execution cancelled.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()