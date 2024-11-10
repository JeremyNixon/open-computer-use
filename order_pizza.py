import pyautogui
import time

def get_ui_elements():
    ui_elements_dict = {
        "PizzaType": {
            "dropdown": {"x": 260, "y": 215},
        },
        "PizzaSize": {
            "dropdown": {"x": 236, "y": 274},
        },
        "Toppings": {
            "Extra Cheese": {"x": 110, "y": 357},
            "Peppers": {"x": 110, "y": 381},
            "Olives": {"x": 110, "y": 405},
        },
        "BuyNow": {
            "button": {"x": 170, "y": 445},
        },
    }
    return ui_elements_dict
ui_elements_dict = get_ui_elements()

print("Starting in 3 seconds...please make sure the browser is active window!")
time.sleep(0)
print("Started")

# Pizza Type dropdown
print("Selecting pizza type: Pepperoni")
pizza_type_coords = ui_elements_dict["PizzaType"]["dropdown"]
print(f"Moving to pizza type dropdown at coordinates: ({pizza_type_coords['x']}, {pizza_type_coords['y']})")
pyautogui.moveTo(pizza_type_coords["x"], pizza_type_coords["y"])
pyautogui.click()
time.sleep(1)
print("Typing 'Pepperoni'...")
pyautogui.typewrite("Pepperoni")
pyautogui.press("enter")

# Pizza Size dropdown
print("\nSelecting pizza size: Large")
pizza_size_coords = ui_elements_dict["PizzaSize"]["dropdown"]
print(f"Moving to pizza size dropdown at coordinates: ({pizza_size_coords['x']}, {pizza_size_coords['y']})")
pyautogui.moveTo(pizza_size_coords["x"], pizza_size_coords["y"])
pyautogui.click()
time.sleep(1)
print("Typing 'Large'...")
pyautogui.typewrite("Large")
pyautogui.press("enter")

# Select desired toppings
print("\nSelecting toppings...")
desired_toppings = ["Extra Cheese", "Peppers"]
toppings_dict = ui_elements_dict["Toppings"]
for topping in desired_toppings:
    if topping in toppings_dict:
        coords = toppings_dict[topping]
        print(f"Adding {topping} at coordinates: ({coords['x']}, {coords['y']})")
        pyautogui.moveTo(coords["x"], coords["y"])
        pyautogui.click()
        time.sleep(0.5)

# Buy Now button
print("\nMoving to Buy Now button...")
buy_coords = ui_elements_dict["BuyNow"]["button"]
print(f"Buy button coordinates: ({buy_coords['x']}, {buy_coords['y']})")
pyautogui.moveTo(buy_coords["x"], buy_coords["y"])
pyautogui.click()
print("Changed my mind! Moving away from Buy button...")
pyautogui.moveTo(500, 500)  # Move mouse away from Buy button

print("\nPizza order cancelled!")
print("Final mouse position:", pyautogui.position())
