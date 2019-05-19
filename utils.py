
import pyautogui


def move_mouse_relative(command):
    """Move mouse relative to the current position.

    command should be a string of format: "x, y"
    returns empty string or error message.
    """
    try:
        x, y = [float(val) for val in command.split(',')]
    except ValueError:
        return f'Invalid command: {command}. Command should be "x, y"'.encode()
    pyautogui.moveRel(x, y)
    return 'OK'.encode()


def get_mouse_position(command):
    """Return current mouse position.

    command is ignored.
    returns the current cursor position in pixels. Format: "x, y"
    """
    return ','.join([str(value) for value in pyautogui.position()]).encode()


def get_screen_size(command):
    """Return screen size.

    command is ignored.
    returns the screen size in pixels. Format: "x, y"
    """
    return ','.join([str(value) for value in pyautogui.size()]).encode()
