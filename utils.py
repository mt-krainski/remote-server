
import pyautogui
from sys import platform

if platform == 'linux':
    try:
        import alsaaudio
        _audio_mixer = alsaaudio.Mixer()
    except:
        print('Audio controls will not work. Please install libasound2-dev and pyalsaaudio')


def move_mouse_relative(command):
    """Move mouse relative to the current position.

    command should be a string of format: "x, y"
    returns OK or error message.
    """
    try:
        x, y = [float(val) for val in command.split(',')]
    except ValueError:
        return f'Invalid command: {command}. Command should be "x, y"'.encode()
    pyautogui.moveRel(x, y)
    return 'OK'.encode()


def scroll_mouse(command):
    """Scroll the mouse wheel.

    command should be a string of format: "x".
    returns OK or error message.
    """
    try:
        x = int(float(command))
    except ValueError:
        return f'Invalid command: {command}. Should be "x"'.encode()
    pyautogui.scroll(x)
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


def left_click(command):
    """Left mouse click.

    command is ignored.
    returns OK or error message.
    """
    pyautogui.click(button='left')
    return 'OK'.encode()


def right_click(command):
    """Left mouse click.

    command is ignored.
    returns OK or error message.
    """
    pyautogui.click(button='right')
    return 'OK'.encode()


def middle_click(command):
    """Middle mouse click.

    command is ignored.
    returns OK or error message
    """
    pyautogui.click(button='middle')
    return 'OK'.encode()


def text_input(command):
    """Input a text from keyboard.

    command: text to input.
    returns OK or error message.
    """
    pyautogui.typewrite(command)
    return 'OK'.encode()


def press_key(command):
    """Press a special key on the keyboard.

    See https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
    for the list of keys. 
    """
    pyautogui.press(command)
    return 'OK'.encode()


def hotkey(command):
    """Press a combination of keys on the keyboard.

    See https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
    for the list of keys. 
    """
    sequence = [s.strip() for s in command.split(',')]
    pyautogui.hotkey(*sequence)
    return 'OK'.encode()

def update_volume_relative(command):
    """Change the volume relative by command percent.
    
    Returns updated volume or error message.
    """
    if platform == 'linux':
        try:
            vol = _audio_mixer.getvolume()
            vol = int(vol[0])
            new_vol = vol + int(command)
            _audio_mixer.setvolume(new_vol)
            return f'volume: {new_vol}'.encode()
        except Exception:
            return 'Error updating volume.'.encode()
    if int(command)>0:
        pyautogui.press('volumeup')
    elif int(command)<0:
        pyautogui.press('volumedown')

    return 'Volume: None'.encode()
