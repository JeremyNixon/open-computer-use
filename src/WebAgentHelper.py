import webbrowser

def launch_url_in_default_browser(url: str) -> bool:
    """
    Launch the specified URL in the default web browser.

    Args:
        url (str): The URL to open in the browser.

    Returns:
        bool: True if successful, False if an error occurs.
    """
    try:
        webbrowser.open_new_tab(url)
        return True
    except Exception as e:
        print(f"Error launching URL: {e}")
        return False
