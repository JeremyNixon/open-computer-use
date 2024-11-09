import os
import time
import pyautogui
import subprocess
from PIL import Image
import io
from dotenv import load_dotenv
import base64

class ScreenshotProcessor:
    def __init__(self, client):
        print("Initializing...")
        self.client = client

        # Configure PyAutoGUI settings
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True
        
    def take_screenshot(self) -> str:
        """Take a screenshot and save it temporarily."""
        screenshot = pyautogui.screenshot()
        
        # Save screenshot to bytes
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Save to file temporarily
        temp_path = "temp_screenshot.png"
        screenshot.save(temp_path)
        
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
                    Use pyautogui functions and include necessary imports. Focus on accurate coordinates and reliable automation sequences. 
                    Return only executable Python code without any explanation."""
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
            # try:
            response = self.client.chat.completions.create(
                model=os.getenv("VISION_MODEL"),
                messages=messages,
                max_tokens=4000,
                temperature=0.0,
            )
            # except openai.APIError as e:
            #     print(f"OpenAI API returned an API Error: {e}")
            # except openai.APIConnectionError as e:
            #     print(f"Failed to connect to OpenAI API: {e}")
            # except openai.APITimeoutError as e:
            #     print(f"OpenAI API request timed out: {e}")

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating automation code: {str(e)}")
            return None

    def process_screenshot(self, instruction: str) -> tuple:
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

def clean_code(code: str) -> str:
    """Remove markdown formatting and clean the code for execution."""
    # Remove markdown code blocks
    code = code.replace("```python", "").replace("```", "")
    # Remove leading/trailing whitespace
    code = code.strip()
    return code

def main():
    """Main execution function."""
    load_dotenv()  # Load environment variables from .env file
    try:
        if not os.getenv('OPENAI_API_KEY'):
            print("Error: OPENAI_API_KEY not found in environment variables")
            return
        
        from openai import OpenAI
        #print("OpenAI api key = ", os.getenv('OPENAI_API_KEY'))
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
        processor = ScreenshotProcessor(client)
        
        instruction = input("What action would you like to automate? ")
        
        screenshot_path, generated_code = processor.process_screenshot(instruction)
        
        if not generated_code:
            print("Failed to generate automation code")
            return
            
        # Clean the code before displaying and executing
        cleaned_code = clean_code(generated_code)
        
        print("\nGenerated Python code:")
        print(cleaned_code)
        
        confirmation = input("\nWould you like to execute this code? (yes/no): ")
        
        if confirmation.lower() == 'yes':
            print("Executing automation...")
            try:
                # Execute the cleaned code
                exec(cleaned_code)
            except Exception as e:
                print(f"Error executing automation: {str(e)}")
        else:
            print("Execution cancelled.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()