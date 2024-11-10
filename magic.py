import os
import time
import pyautogui
import subprocess
from PIL import Image, ImageDraw, ImageFont
import io
from dotenv import load_dotenv
import base64
import numpy as np
import random
import re

def add_coordinate_labels(image_array, num_points=25):
    """
    Adds coordinate labels with arrows to an image for random pixel positions on a 50x50 grid.
    Always includes (0,0) coordinate.
    
    Args:
        image_array: numpy array of the image
        num_points: number of random points to label (default 25)
    
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
    
    # Calculate grid size
    grid_step = 50
    grid_width = width // grid_step
    grid_height = height // grid_step
    
    # Generate random grid points
    points = set()
    # Always add (0,0)
    points.add((0, 0))
    
    # Add random points
    while len(points) < num_points + 1:  # +1 because we already added (0,0)
        x = random.randint(0, grid_width) * grid_step
        y = random.randint(0, grid_height) * grid_step
        points.add((x, y))
    
    # Draw points and labels
    arrow_color = (255, 0, 0)  # Red color for visibility
    arrow_size = 5
    
    for x, y in points:
        # Calculate arrow endpoint (offset from point for visibility)
        end_x = x - 10
        end_y = y - 10
        
        # Draw arrow line
        draw.line([(end_x, end_y), (x, y)], fill=arrow_color, width=1)
        
        # Draw arrowhead
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
    
    # Draw light gray grid lines
    grid_color = (200, 200, 200)  # Light gray
    
    # Vertical lines
    for x in range(0, width, grid_step):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    
    # Horizontal lines
    for y in range(0, height, grid_step):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
    
    return image

def capture_region_around_point(x: int, y: int) -> tuple:
    """
    Captures a 150x150 pixel region centered around the given coordinates.
    
    Args:
        x: x-coordinate of center point
        y: y-coordinate of center point
    
    Returns:
        Tuple of (PIL Image, numpy array) of the captured region
    """
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    
    # Calculate region bounds (75 pixels in each direction)
    left = max(0, x - 75)
    top = max(0, y - 75)
    right = min(screen_width, x + 75)
    bottom = min(screen_height, y + 75)
    
    # Take screenshot of region
    screenshot = pyautogui.screenshot(region=(left, top, right-left, bottom-top))
    
    # Convert to numpy array
    screenshot_array = np.array(screenshot)
    
    return screenshot, screenshot_array

class ScreenshotProcessor:
    def __init__(self, client):
        print("Initializing...")
        self.client = client

        # Configure PyAutoGUI settings
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True
        
    def take_screenshot(self, region=None) -> str:
        """Take a screenshot and save it temporarily."""
        # Create screenshots directory if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        
        if region is not None:
            screenshot = pyautogui.screenshot(region=region)
        else:
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

    def generate_automation_code(self, screenshot_path: str, instruction: str) -> tuple:
        """
        Generate automation code using OpenAI's API and extract coordinates.
        Returns both the generated code and the coordinates chosen.
        """
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
                    
                    IMPORTANT COORDINATE SELECTION RULES:
                    1. ONLY use coordinates that are explicitly labeled in the screenshot
                    2. Choose the labeled coordinate point that is CLOSEST to the UI element
                    3. Do NOT interpolate or calculate new coordinates
                    4. Do NOT modify or adjust the coordinates in any way
                    
                    Your response must:
                    1. Start with the exact coordinates chosen in format: COORDINATES: (x,y)
                    2. Follow with executable Python code
                    3. Include necessary imports and time.sleep() for timing
                    4. Use the exact coordinates from step 1
                    5. End with an explanation labeled with 'Explanation' that describes why these coordinates were chosen
                    """
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

            content = response.choices[0].message.content
            
            # Extract coordinates from response
            coord_match = re.search(r'COORDINATES: \((\d+),(\d+)\)', content)
            if coord_match:
                x, y = map(int, coord_match.groups())
                # Remove the coordinates line from the content
                content = re.sub(r'COORDINATES: \(\d+,\d+\)\n*', '', content)
                return content, (x, y)
            else:
                return content, None

        except Exception as e:
            print(f"Error generating automation code: {str(e)}")
            return None, None

    def process_screenshot_and_generate_code(self, instruction: str) -> tuple:
        """Process screenshot and generate automation code with a two-step approach."""
        try:
            # Take initial full screenshot
            screenshot_path = self.take_screenshot()
            
            # Generate initial code and get coordinates
            generated_code, coords = self.generate_automation_code(screenshot_path, instruction)
            
            if coords is None:
                return screenshot_path, generated_code
            
            # Take a closer screenshot around the chosen coordinates
            x, y = coords
            closer_screenshot, closer_array = capture_region_around_point(x, y)
            
            # Save and label the closer screenshot
            closer_path = self.take_screenshot(region=(x-75, y-75, 150, 150))
            
            # Generate new code with closer view
            final_code, final_coords = self.generate_automation_code(closer_path, instruction)
            
            if final_coords is not None:
                # Adjust coordinates relative to original position
                final_x = x - 75 + final_coords[0]
                final_y = y - 75 + final_coords[1]
                return closer_path, final_code
            
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
