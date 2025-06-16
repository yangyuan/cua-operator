import asyncio
import ctypes
import base64
from io import BytesIO
from ctypes import wintypes
from typing import Optional, Union
from PIL import ImageGrab, Image


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

SLEEP_INTERVAL = 0.01

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_HWHEEL = 0x01000

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
VK_RETURN = 0x0D
VK_SHIFT = 0x10

# Virtual-Key Codes: https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VK_MAP = {  # everything except 0-1, A-Z
    "LBUTTON": 0x01,
    "RBUTTON": 0x02,
    "CANCEL": 0x03,
    "MBUTTON": 0x04,
    "XBUTTON1": 0x05,
    "XBUTTON2": 0x06,
    "BACK": 0x08,
    "TAB": 0x09,
    "CLEAR": 0x0C,
    "RETURN": 0x0D,
    "SHIFT": 0x10,
    "CONTROL": 0x11,
    "MENU": 0x12,
    "PAUSE": 0x13,
    "CAPITAL": 0x14,
    "KANA": 0x15,
    "HANGUL": 0x15,
    "IME_ON": 0x16,
    "JUNJA": 0x17,
    "FINAL": 0x18,
    "HANJA": 0x19,
    "KANJI": 0x19,
    "IME_OFF": 0x1A,
    "ESCAPE": 0x1B,
    "CONVERT": 0x1C,
    "NONCONVERT": 0x1D,
    "ACCEPT": 0x1E,
    "MODECHANGE": 0x1F,
    "SPACE": 0x20,
    "PRIOR": 0x21,
    "NEXT": 0x22,
    "END": 0x23,
    "HOME": 0x24,
    "LEFT": 0x25,
    "UP": 0x26,
    "RIGHT": 0x27,
    "DOWN": 0x28,
    "SELECT": 0x29,
    "PRINT": 0x2A,
    "EXECUTE": 0x2B,
    "SNAPSHOT": 0x2C,
    "INSERT": 0x2D,
    "DELETE": 0x2E,
    "HELP": 0x2F,
    "LWIN": 0x5B,
    "RWIN": 0x5C,
    "APPS": 0x5D,
    "SLEEP": 0x5F,
    "NUMPAD0": 0x60,
    "NUMPAD1": 0x61,
    "NUMPAD2": 0x62,
    "NUMPAD3": 0x63,
    "NUMPAD4": 0x64,
    "NUMPAD5": 0x65,
    "NUMPAD6": 0x66,
    "NUMPAD7": 0x67,
    "NUMPAD8": 0x68,
    "NUMPAD9": 0x69,
    "MULTIPLY": 0x6A,
    "ADD": 0x6B,
    "SEPARATOR": 0x6C,
    "SUBTRACT": 0x6D,
    "DECIMAL": 0x6E,
    "DIVIDE": 0x6F,
    "F1": 0x70,
    "F2": 0x71,
    "F3": 0x72,
    "F4": 0x73,
    "F5": 0x74,
    "F6": 0x75,
    "F7": 0x76,
    "F8": 0x77,
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7A,
    "F12": 0x7B,
    "F13": 0x7C,
    "F14": 0x7D,
    "F15": 0x7E,
    "F16": 0x7F,
    "F17": 0x80,
    "F18": 0x81,
    "F19": 0x82,
    "F20": 0x83,
    "F21": 0x84,
    "F22": 0x85,
    "F23": 0x86,
    "F24": 0x87,
    "NUMLOCK": 0x90,
    "SCROLL": 0x91,
    "LSHIFT": 0xA0,
    "RSHIFT": 0xA1,
    "LCONTROL": 0xA2,
    "RCONTROL": 0xA3,
    "LMENU": 0xA4,
    "RMENU": 0xA5,
    "BROWSER_BACK": 0xA6,
    "BROWSER_FORWARD": 0xA7,
    "BROWSER_REFRESH": 0xA8,
    "BROWSER_STOP": 0xA9,
    "BROWSER_SEARCH": 0xAA,
    "BROWSER_FAVORITES": 0xAB,
    "BROWSER_HOME": 0xAC,
    "VOLUME_MUTE": 0xAD,
    "VOLUME_DOWN": 0xAE,
    "VOLUME_UP": 0xAF,
    "MEDIA_NEXT_TRACK": 0xB0,
    "MEDIA_PREV_TRACK": 0xB1,
    "MEDIA_STOP": 0xB2,
    "MEDIA_PLAY_PAUSE": 0xB3,
    "LAUNCH_MAIL": 0xB4,
    "LAUNCH_MEDIA_SELECT": 0xB5,
    "LAUNCH_APP1": 0xB6,
    "LAUNCH_APP2": 0xB7,
    "OEM_1": 0xBA,
    "OEM_PLUS": 0xBB,
    "OEM_COMMA": 0xBC,
    "OEM_MINUS": 0xBD,
    "OEM_PERIOD": 0xBE,
    "OEM_2": 0xBF,
    "OEM_3": 0xC0,
    "OEM_4": 0xDB,
    "OEM_5": 0xDC,
    "OEM_6": 0xDD,
    "OEM_7": 0xDE,
    "OEM_8": 0xDF,
    "OEM_102": 0xE2,
    "PROCESSKEY": 0xE5,
    "PACKET": 0xE7,
    "ATTN": 0xF6,
    "CRSEL": 0xF7,
    "EXSEL": 0xF8,
    "EREOF": 0xF9,
    "PLAY": 0xFA,
    "ZOOM": 0xFB,
    "NONAME": 0xFC,
    "PA1": 0xFD,
    "OEM_CLEAR": 0xFE,
}

# Define ULONG_PTR for compatibility if not present in ctypes.wintypes
if not hasattr(wintypes, "ULONG_PTR"):
    import sys

    if sys.maxsize > 2**32:
        wintypes.ULONG_PTR = ctypes.c_uint64
    else:
        wintypes.ULONG_PTR = ctypes.c_uint32


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT)]

    _anonymous_ = ("_input",)
    _fields_ = [("type", wintypes.DWORD), ("_input", _INPUT)]


def send_input(input_obj: Union[INPUT, list[INPUT]]) -> None:
    """Send a single INPUT or a sequence of INPUTs."""
    if isinstance(input_obj, list):
        n_inputs = len(input_obj)
        arr_type = INPUT * n_inputs
        arr = arr_type(*input_obj)
        user32.SendInput(n_inputs, ctypes.byref(arr), ctypes.sizeof(INPUT))
    else:
        user32.SendInput(1, ctypes.byref(input_obj), ctypes.sizeof(input_obj))


async def move(x: int, y: int) -> None:
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    abs_x = int(x * 65535 / screen_width)
    abs_y = int(y * 65535 / screen_height)
    inp = INPUT(
        type=INPUT_MOUSE,
        mi=MOUSEINPUT(
            dx=abs_x,
            dy=abs_y,
            mouseData=0,
            dwFlags=MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
            time=0,
            dwExtraInfo=0,
        ),
    )
    send_input(inp)


async def click(
    button: str = "left", x: Optional[int] = None, y: Optional[int] = None
) -> None:
    # button: left, right, wheel, back, forward
    if x is not None and y is not None:
        await move(x, y)
        await asyncio.sleep(SLEEP_INTERVAL)
    if button == "left":
        down_flag = MOUSEEVENTF_LEFTDOWN
        up_flag = MOUSEEVENTF_LEFTUP
        mouseData = 0
    elif button == "right":
        down_flag = MOUSEEVENTF_RIGHTDOWN
        up_flag = MOUSEEVENTF_RIGHTUP
        mouseData = 0
    elif button == "middle" or button == "wheel":
        down_flag = 0x0020  # MOUSEEVENTF_MIDDLEDOWN
        up_flag = 0x0040  # MOUSEEVENTF_MIDDLEUP
        mouseData = 0
    elif button == "back":
        down_flag = 0x0020  # MOUSEEVENTF_XDOWN
        up_flag = 0x0040  # MOUSEEVENTF_XUP
        mouseData = 0x0001  # XBUTTON1
    elif button == "forward":
        down_flag = 0x0020  # MOUSEEVENTF_XDOWN
        up_flag = 0x0040  # MOUSEEVENTF_XUP
        mouseData = 0x0002  # XBUTTON2
    else:
        raise ValueError(
            "button must be 'left', 'right', 'middle', 'wheel', 'back', or 'forward'"
        )
    down = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, mouseData, down_flag, 0, 0))
    up = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, mouseData, up_flag, 0, 0))
    send_input([down, up])


async def double_click(x: Optional[int] = None, y: Optional[int] = None) -> None:
    await click(button="left", x=x, y=y)
    await asyncio.sleep(SLEEP_INTERVAL)
    await click(button="left", x=x, y=y)


async def drag(path: list[tuple[int, int]]) -> None:
    if not path or len(path) < 2:
        raise ValueError("Path must contain at least two points")
    await move(*path[0])
    await asyncio.sleep(SLEEP_INTERVAL)
    down = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, 0))
    send_input(down)
    await asyncio.sleep(SLEEP_INTERVAL)
    for point in path[1:-1]:
        await move(*point)
        await asyncio.sleep(SLEEP_INTERVAL)
    await move(*path[-1])
    await asyncio.sleep(SLEEP_INTERVAL)
    up = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, 0))
    send_input(up)


async def key_press(keys: list[str]) -> None:
    vk_codes = []
    for key in keys:
        key_upper = key.upper()
        if key_upper in VK_MAP:
            vk_codes.append(VK_MAP[key_upper])
        elif len(key) == 1:
            vk = user32.VkKeyScanW(ord(key)) & 0xFF
            if vk != 0xFF:
                vk_codes.append(vk)
        else:
            raise ValueError(f"Unknown key: {key}")

    downs = [
        INPUT(
            type=INPUT_KEYBOARD,
            ki=KEYBDINPUT(wVk=vk, wScan=0, dwFlags=0, time=0, dwExtraInfo=0),
        )
        for vk in vk_codes
    ]
    ups = [
        INPUT(
            type=INPUT_KEYBOARD,
            ki=KEYBDINPUT(
                wVk=vk, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0
            ),
        )
        for vk in reversed(vk_codes)
    ]
    send_input(downs)
    await asyncio.sleep(SLEEP_INTERVAL)
    send_input(ups)


async def type_text(text: str) -> None:
    for char in text:
        await asyncio.sleep(SLEEP_INTERVAL)
        vk_scan = user32.VkKeyScanW(ord(char))
        vk = vk_scan & 0xFF
        shift = (vk_scan >> 8) & 0xFF
        if vk == 0xFF or ord(char) > 0x7F:
            # Send as Unicode event
            down = INPUT(
                type=INPUT_KEYBOARD,
                ki=KEYBDINPUT(
                    wVk=0,
                    wScan=ord(char),
                    dwFlags=KEYEVENTF_UNICODE,
                    time=0,
                    dwExtraInfo=0,
                ),
            )
            up = INPUT(
                type=INPUT_KEYBOARD,
                ki=KEYBDINPUT(
                    wVk=0,
                    wScan=ord(char),
                    dwFlags=KEYEVENTF_UNICODE | KEYEVENTF_KEYUP,
                    time=0,
                    dwExtraInfo=0,
                ),
            )
            send_input(down)
            await asyncio.sleep(SLEEP_INTERVAL)
            send_input(up)
        else:
            downs = []
            ups = []
            if shift & 1:
                downs.append(
                    INPUT(
                        type=INPUT_KEYBOARD,
                        ki=KEYBDINPUT(
                            wVk=VK_SHIFT, wScan=0, dwFlags=0, time=0, dwExtraInfo=0
                        ),
                    )
                )
            downs.append(
                INPUT(
                    type=INPUT_KEYBOARD,
                    ki=KEYBDINPUT(wVk=vk, wScan=0, dwFlags=0, time=0, dwExtraInfo=0),
                )
            )
            ups.append(
                INPUT(
                    type=INPUT_KEYBOARD,
                    ki=KEYBDINPUT(
                        wVk=vk, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0
                    ),
                )
            )
            if shift & 1:
                ups.append(
                    INPUT(
                        type=INPUT_KEYBOARD,
                        ki=KEYBDINPUT(
                            wVk=VK_SHIFT,
                            wScan=0,
                            dwFlags=KEYEVENTF_KEYUP,
                            time=0,
                            dwExtraInfo=0,
                        ),
                    )
                )

            send_input(downs)
            await asyncio.sleep(SLEEP_INTERVAL)
            send_input(ups)


async def scroll(
    scroll_x: int, scroll_y: int, x: Optional[int] = None, y: Optional[int] = None
) -> None:
    if x is not None and y is not None:
        await move(x, y)
        await asyncio.sleep(SLEEP_INTERVAL)
    if scroll_y != 0:
        inp = INPUT(
            type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, scroll_y, MOUSEEVENTF_WHEEL, 0, 0)
        )
        send_input(inp)
    if scroll_x != 0:
        inp = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(0, 0, scroll_x, MOUSEEVENTF_HWHEEL, 0, 0),
        )
        send_input(inp)


async def screenshot() -> str:
    img = ImageGrab.grab()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    img = img.resize((screen_width, screen_height), Image.LANCZOS)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


async def dimensions() -> tuple[int, int]:
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height


async def wait() -> None:
    await asyncio.sleep(1)
