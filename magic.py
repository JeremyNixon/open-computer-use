from typing import Optional, Tuple
from datetime import datetime
import base64
import os
import subprocess
from pathlib import Path

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import pyautogui
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SCREENSHOT_STEP = int(os.getenv('SCREENSHOT_STEP', '100'))
FONT_SIZE = int(os.getenv('FONT_SIZE', '12'))
ARROW_LENGTH = int(os.getenv('ARROW_LENGTH', '20'))
ARROW_SIZE = int(os.getenv('ARROW_SIZE', '5'))
OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'screenshots')

class ScreenshotProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 string.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 encoded string of image
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def add_coordinate_labels(self, image_array: np.ndarray, step: int = SCREENSHOT_STEP) -> Image:
        """
        Add coordinate labels with arrows to an image.
        
        Args:
            image_array: Numpy array of screenshot
            step: Spacing between labeled points
            
        Returns:
            PIL Image with coordinates labeled
        """
        image = Image.fromarray(image_array)
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", FONT_SIZE)
        except:
            font = ImageFont.load_default()
        
        height, width = image_array.shape[:2]
        
        for y in range(0, height, step):
            for x in range(0, width, step):
                end_x = x + 15
                end_y = y - 15
                
                # Draw arrow
                draw.line([(end_x, end_y), (x, y)], fill=(255, 0, 0), width=1)
                draw.polygon([
                    (x, y),
                    (x + ARROW_SIZE, y - ARROW_SIZE),
                    (x - ARROW_SIZE, y - ARROW_SIZE)
                ], fill=(255, 0, 0))
                
                # Add coordinate text
                text = f"({x}, {y})"
                text_bbox = draw.textbbox((end_x, end_y), text, font=font)
                
                draw.rectangle([
                    (text_bbox[0]-2, text_bbox[1]-2),
                    (text_bbox[2]+2, text_bbox[3]+2)
                ], fill=(255, 255, 255))
                
                draw.text((end_x, end_y), text, fill=(0, 0, 0), font=font)
        
        return image

    def get_python_code_to_execute_pyautogui(self, image_path: str, instruction: str) -> str:
        """
        Get Python code from GPT-4 to execute user's instruction using PyAutoGUI.
        
        Args:
            image_path: Path to labeled screenshot
            instruction: User's instruction
            
        Returns:
            Python code string to execute
        """
        prompt = f"""
        The user's instruction is: {instruction}
        Based on this pixel labeled image of a computer screen, write PyAutoGUI code that executes the user's instruction.
        Return only the executable Python code without any markdown formatting.
        """
        
        base64_image = self.encode_image(image_path)
        
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": prompt,
                }, {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                }],
            }]
        )
        
        return response.choices[0].message.content

    def process_screenshot(self, instruction: str) -> Tuple[str, str]:
        """
        Process screenshot and generate automation code.
        
        Args:
            instruction: User's instruction
            
        Returns:
            Tuple of (screenshot path, generated python code)
        """
        print("Taking screenshot...")
        screenshot = pyautogui.screenshot()
        image_array = np.array(screenshot)
        
        print("Adding coordinate labels...")
        labeled_image = self.add_coordinate_labels(image_array)
        
        # Create output directory if it doesn't exist
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(OUTPUT_DIR) / f"labeled_screenshot_{timestamp}.png"
        labeled_image.save(output_path)
        print(f"Labeled screenshot saved to: {output_path}")
        
        print("Generating automation code...")
        generated_code = self.get_python_code_to_execute_pyautogui(str(output_path), instruction)
        
        return str(output_path), generated_code

def main():
    """Main execution function."""
    processor = ScreenshotProcessor()
    
    instruction = input("What action would you like to automate? ")
    
    screenshot_path, generated_code = processor.process_screenshot(instruction)
    
    print("\nGenerated Python code:")
    print(generated_code)
    
    confirmation = input("\nWould you like to execute this code? (yes/no): ")
    
    if confirmation.lower() == 'yes':
        print("Executing automation...")
        exec(generated_code)
    else:
        print("Execution cancelled.")

if __name__ == "__main__":
    main()