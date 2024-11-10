import pyautogui
from typing import Tuple, Optional, List, Callable
from PIL import Image, ImageDraw, ImageStat
import time
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import webbrowser

class MousePosition(BaseModel):
    x: int
    y: int

class PyAutoGuiHelper:
    """
    PyAutoGuiHelper:
    ----------------

    A helper class for automating GUI interactions using PyAutoGUI.

    Methods:
    - __init__()
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
    - screenshot(region=None) -> Image
    - locate_on_screen(image_path, confidence=0.8) -> Optional[Tuple[int, int, int, int]]
    - locate_center_on_screen(image_path, confidence=0.8) -> Optional[Tuple[int, int]]
    - alert(text, title='Alert', button='OK')
    - confirm(text, title='Confirm', buttons=['OK', 'Cancel']) -> str
    - prompt(text, title='Input', default='') -> str
    - password(text, title='Password', default='', mask='*') -> str
    - get_screen_size() -> Tuple[int, int]
    - get_mouse_position() -> MousePosition
    - is_point_on_screen(x, y) -> bool
    - pixel(x, y) -> Tuple[int, int, int]
    - pixel_matches_color(x, y, expected_rgb, tolerance=0) -> bool
    - locate_all_on_screen(image_path, confidence=0.8) -> List[Tuple[int, int, int, int]]
    - locate_on_screen_near(image_path, x, y, confidence=0.8) -> Optional[Tuple[int, int, int, int]]
    - locate_center_on_screen_near(image_path, x, y, confidence=0.8) -> Optional[Tuple[int, int]]
    - outline_region_on_screen(region, outline_color=None, filename='_showRegionOnScreen.png')
    - wait_for_image(image_path, timeout=30, confidence=0.8) -> bool
    - wait_for_image_and_click(image_path, timeout=30, confidence=0.8, clicks=1, interval=0.0, button='left')
    - draw_cursor_on_screenshot(x, y, screenshot, cursor)
    - get_cursor_image() -> Image
    - launch_url_in_default_browser(url) -> bool
    """

    def __init__(self):
        load_dotenv()
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = float(os.getenv("PYAUTOGUI_PAUSE_SECONDS_AFTER_COMMAND", 0.5))

    def move_mouse(self, x: int, y: int, duration: float = 0.25):
        pyautogui.moveTo(x, y, duration=duration)

    def move_mouse_relative(self, dx: int, dy: int, duration: float = 0.25):
        pyautogui.moveRel(dx, dy, duration=duration)

    def click(self, x: int = None, y: int = None, clicks: int = 1, interval: float = 0.0, button: str = 'left'):
        pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)

    def double_click(self, x: int = None, y: int = None, interval: float = 0.0, button: str = 'left'):
        pyautogui.doubleClick(x, y, interval=interval, button=button)

    def right_click(self, x: int = None, y: int = None):
        pyautogui.rightClick(x, y)

    def middle_click(self, x: int = None, y: int = None):
        pyautogui.middleClick(x, y)

    def scroll(self, clicks: int, x: int = None, y: int = None):
        pyautogui.scroll(clicks, x=x, y=y)

    def drag_to(self, x: int, y: int, duration: float = 0.25, button: str = 'left'):
        pyautogui.dragTo(x, y, duration=duration, button=button)

    def drag_rel(self, dx: int, dy: int, duration: float = 0.25, button: str = 'left'):
        pyautogui.dragRel(dx, dy, duration=duration, button=button)

    def type_text(self, text: str, interval: float = 0.0):
        pyautogui.write(text, interval=interval)

    def press_key(self, key: str):
        pyautogui.press(key)

    def hotkey(self, *keys: str):
        pyautogui.hotkey(*keys)

    def screenshot(self, region: Tuple[int, int, int, int] = None) -> Image:
        return pyautogui.screenshot(region=region)

    def locate_on_screen(self, image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int, int, int]]:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            return (location.left, location.top, location.width, location.height)
        return None

    def locate_center_on_screen(self, image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            return (location[0], location[1])
        return None

    def alert(self, text: str, title: str = 'Alert', button: str = 'OK'):
        pyautogui.alert(text=text, title=title, button=button)

    def confirm(self, text: str, title: str = 'Confirm', buttons: List[str] = ['OK', 'Cancel']) -> str:
        return pyautogui.confirm(text=text, title=title, buttons=buttons)

    def prompt(self, text: str, title: str = 'Input', default: str = '') -> str:
        return pyautogui.prompt(text=text, title=title, default=default)

    def password(self, text: str, title: str = 'Password', default: str = '', mask: str = '*') -> str:
        return pyautogui.password(text=text, title=title, default=default, mask=mask)

    def get_screen_size(self) -> Tuple[int, int]:
        return pyautogui.size()

    def get_mouse_position(self) -> MousePosition:
        position = pyautogui.position()
        return MousePosition(x=position[0], y=position[1])

    def is_point_on_screen(self, x: int, y: int) -> bool:
        return pyautogui.onScreen(x, y)

    def pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        return pyautogui.pixel(x, y)

    def pixel_matches_color(self, x: int, y: int, expected_rgb: Tuple[int, int, int], tolerance: int = 0) -> bool:
        return pyautogui.pixelMatchesColor(x, y, expected_rgb, tolerance=tolerance)

    def locate_all_on_screen(self, image_path: str, confidence: float = 0.8) -> List[Tuple[int, int, int, int]]:
        return list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))

    def locate_on_screen_near(self, image_path: str, x: int, y: int, confidence: float = 0.8) -> Optional[Tuple[int, int, int, int]]:
        matches = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
        if not matches:
            return None
        closest_match = min(matches, key=lambda match: (match.left - x)**2 + (match.top - y)**2)
        return (closest_match.left, closest_match.top, closest_match.width, closest_match.height)

    def locate_center_on_screen_near(self, image_path: str, x: int, y: int, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        location = self.locate_on_screen_near(image_path, x, y, confidence)
        if location:
            return (location[0] + location[2] // 2, location[1] + location[3] // 2)
        return None

    def get_cursor_image(self) -> Image:
        """
        Draw realistic mac cursor on screen
        """
        cursor = Image.new('RGBA', (16, 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(cursor)
        draw.polygon([(0,0), (0,24), (12,18), (16,24), (16,22), (13,16), (16,16)], fill=(0,0,0,255))
        return cursor

    def outline_region_on_screen(self, region: Tuple[int, int, int, int], outline_color: str = None, filename: str = '_showRegionOnScreen.png'):
        im = self.screenshot()
        mouse_position = self.get_mouse_position()
        self.draw_cursor_on_screenshot(mouse_position.x, mouse_position.y, im, self.get_cursor_image())

        draw = ImageDraw.Draw(im)
        left, top, width, height = region
        right = left + width
        bottom = top + height

        # Compute average brightness of the region
        region_im = im.crop((left, top, right, bottom))
        stat = ImageStat.Stat(region_im)
        mean_brightness = sum(stat.mean) / len(stat.mean)

        # Choose a contrasting color if outline_color is not specified
        if outline_color is None:
            outline_color = 'red' if mean_brightness > 128 else 'yellow'

        # Set line parameters
        line_width = 5
        dash_length = 15
        gap_length = 10

        # Draw dashed rectangle
        # Top edge
        for x in range(left, right, dash_length + gap_length):
            x_end = min(x + dash_length, right)
            draw.line([(x, top), (x_end, top)], fill=outline_color, width=line_width)
        # Bottom edge
        for x in range(left, right, dash_length + gap_length):
            x_end = min(x + dash_length, right)
            draw.line([(x, bottom), (x_end, bottom)], fill=outline_color, width=line_width)
        # Left edge
        for y in range(top, bottom, dash_length + gap_length):
            y_end = min(y + dash_length, bottom)
            draw.line([(left, y), (left, y_end)], fill=outline_color, width=line_width)
        # Right edge
        for y in range(top, bottom, dash_length + gap_length):
            y_end = min(y + dash_length, bottom)
            draw.line([(right, y), (right, y_end)], fill=outline_color, width=line_width)

        im.save(filename)

    def wait_for_image(self, image_path: str, timeout: int = 30, confidence: float = 0.8) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            if pyautogui.locateOnScreen(image_path, confidence=confidence):
                return True
            time.sleep(0.5)
        return False

    def draw_cursor_on_screenshot(self, x: int, y: int, screenshot: Image, cursor: Image):
        screenshot.paste(cursor, (x, y), cursor)

    def wait_for_image_and_click(self, image_path: str, timeout: int = 30, confidence: float = 0.8, clicks: int = 1, interval: float = 0.0, button: str = 'left'):
        if self.wait_for_image(image_path, timeout, confidence):
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                pyautogui.click(x=location[0], y=location[1], clicks=clicks, interval=interval, button=button)
            else:
                print(f"Image {image_path} not found on screen.")
        else:
            print(f"Image {image_path} not found within {timeout} seconds.")

    def launch_url_in_default_browser(self, url: str) -> bool:
        try:
            webbrowser.open_new_tab(url)
            return True
        except Exception as e:
            print(f"Error launching URL: {e}")
            return False
