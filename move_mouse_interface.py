

import pyautogui
import time

# Add a small pause between actions for safety
pyautogui.PAUSE = 0.5

# Enable fail-safe - moving mouse to upper-left corner will abort script
pyautogui.FAILSAFE = True

def basic_mouse_movement():
    # Get the current screen resolution
    screen_width, screen_height = pyautogui.size()
    
    # Move mouse to center of screen
    pyautogui.moveTo(screen_width/2, screen_height/2, duration=1)
    
    # Click at current position
    pyautogui.click()
    
    # Type some text
    pyautogui.typewrite('Hello, PyAutoGUI!', interval=0.1)
    
    # Press Enter
    pyautogui.press('enter')

if __name__ == '__main__':
    # Wait 3 seconds before starting to give time to switch to target window
    print("Starting in 3 seconds...")
    time.sleep(3)
    basic_mouse_movement()

