def execute_command(command, gui_helper):
    """
    Execute the given command using the provided PyAutoGuiHelper instance.

    Args:
        command (str): The command to execute.
        gui_helper (PyAutoGuiHelper): An instance of PyAutoGuiHelper.

    Returns:
        bool: True if the command was executed successfully, False otherwise.
    """
    # Allowed functions mapping
    allowed_functions = {
        'move_mouse': gui_helper.move_mouse,
        'move_mouse_relative': gui_helper.move_mouse_relative,
        'click': gui_helper.click,
        'double_click': gui_helper.double_click,
        'right_click': gui_helper.right_click,
        'middle_click': gui_helper.middle_click,
        'scroll': gui_helper.scroll,
        'drag_to': gui_helper.drag_to,
        'drag_rel': gui_helper.drag_rel,
        'type_text': gui_helper.type_text,
        'press_key': gui_helper.press_key,
        'hotkey': gui_helper.hotkey,
        'launch_url_in_default_browser': gui_helper.launch_url_in_default_browser,
    }

    try:
        # Prepare a safe execution environment
        exec_globals = {'__builtins__': None}
        exec_locals = allowed_functions.copy()

        # Execute the command
        exec(command, exec_globals, exec_locals)
        return True
    except Exception as e:
        print(f"Error executing command: {e}")
        return False
