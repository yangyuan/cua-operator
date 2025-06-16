import asyncio
import ctypes
import ctypes.util
import base64
from io import BytesIO
from typing import Optional
from PIL import Image
import asyncio

# Load CoreGraphics
core = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreGraphics"))
cf = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreFoundation"))


# Types
class CGPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]


CGEventRef = ctypes.c_void_p
CGEventSourceRef = ctypes.c_void_p
CGWindowID = ctypes.c_uint32
CGImageRef = ctypes.c_void_p

# Set function signatures for CoreGraphics
core.CGEventCreateMouseEvent.restype = ctypes.c_void_p
core.CGEventCreateMouseEvent.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint32,
    CGPoint,
    ctypes.c_uint32,
]
core.CGEventPost.restype = None
core.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
core.CFRelease.restype = None
core.CFRelease.argtypes = [ctypes.c_void_p]
core.CGEventCreate.restype = ctypes.c_void_p
core.CGEventCreate.argtypes = [ctypes.c_void_p]
core.CGEventGetLocation.restype = CGPoint
core.CGEventGetLocation.argtypes = [ctypes.c_void_p]
core.CGEventCreateKeyboardEvent.restype = ctypes.c_void_p
core.CGEventCreateKeyboardEvent.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint16,
    ctypes.c_bool,
]
core.CGEventCreateScrollWheelEvent.restype = ctypes.c_void_p
core.CGEventCreateScrollWheelEvent.argtypes = [
    ctypes.c_void_p,
    ctypes.c_int32,
    ctypes.c_uint32,
    ctypes.c_int32,
]
# Add correct signature for CGEventSourceCreate
core.CGEventSourceCreate.restype = ctypes.c_void_p
core.CGEventSourceCreate.argtypes = [ctypes.c_uint32]

# Add CGEventSetFlags signature (missing, causes crash if not set)
core.CGEventSetFlags = core.CGEventSetFlags
core.CGEventSetFlags.restype = None
core.CGEventSetFlags.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

CGEventSetType = core.CGEventSetType
CGEventSetType.argtypes = [ctypes.c_void_p, ctypes.c_uint32]  # eventRef, eventType
CGEventSetType.restype = None

# Add CGEventSetIntegerValueField and kCGMouseEventClickState for double-click support
core.CGEventSetIntegerValueField.argtypes = [
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_long,
]
core.CGEventSetIntegerValueField.restype = None

core.CGEventKeyboardSetUnicodeString.restype = None
core.CGEventKeyboardSetUnicodeString.argtypes = [
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_uint16),
]

kCGMouseEventClickState = 1

# Mouse event types
kCGEventLeftMouseDown = 1
kCGEventLeftMouseUp = 2
kCGEventRightMouseDown = 3
kCGEventRightMouseUp = 4
kCGEventMouseMoved = 5
kCGEventLeftMouseDragged = 6
kCGEventRightMouseDragged = 7
kCGEventScrollWheel = 22
kCGEventOtherMouseDown = 25
kCGEventOtherMouseUp = 26
kCGEventOtherMouseDragged = 27

# Mouse buttons
kCGMouseButtonLeft = 0
kCGMouseButtonRight = 1
kCGMouseButtonCenter = 2

# Scroll units
kCGScrollEventUnitPixel = 0
kCGScrollEventUnitLine = 1

# Keyboard event types
kCGEventKeyDown = 10
kCGEventKeyUp = 11

# Event tap
kCGHIDEventTap = 0

# Keycode map (complete for standard US keyboard)
KEY_MAP = {
    "A": 0,
    "S": 1,
    "D": 2,
    "F": 3,
    "H": 4,
    "G": 5,
    "Z": 6,
    "X": 7,
    "C": 8,
    "V": 9,
    "B": 11,
    "Q": 12,
    "W": 13,
    "E": 14,
    "R": 15,
    "Y": 16,
    "T": 17,
    "1": 18,
    "2": 19,
    "3": 20,
    "4": 21,
    "6": 22,
    "5": 23,
    "EQUAL": 24,
    "9": 25,
    "7": 26,
    "MINUS": 27,
    "8": 28,
    "0": 29,
    "RIGHTBRACKET": 30,
    "O": 31,
    "U": 32,
    "LEFTBRACKET": 33,
    "I": 34,
    "P": 35,
    "RETURN": 36,
    "L": 37,
    "J": 38,
    "APOSTROPHE": 39,
    "K": 40,
    "SEMICOLON": 41,
    "BACKSLASH": 42,
    "COMMA": 43,
    "SLASH": 44,
    "N": 45,
    "M": 46,
    "PERIOD": 47,
    "TAB": 48,
    "SPACE": 49,
    "GRAVE": 50,
    "DELETE": 51,
    "ESC": 53,
    "CMD": 55,
    "SHIFT": 56,
    "CAPSLOCK": 57,
    "ALT": 58,
    "CTRL": 59,
    "RIGHTSHIFT": 60,
    "RIGHTALT": 61,
    "RIGHTCTRL": 62,
    "FN": 63,
    "F17": 64,
    "KEYPADDECIMAL": 65,
    "KEYPADMULTIPLY": 67,
    "KEYPADPLUS": 69,
    "CLEAR": 71,
    "KEYPADDIVIDE": 75,
    "KEYPADENTER": 76,
    "KEYPADMINUS": 78,
    "F18": 79,
    "F19": 80,
    "KEYPADEQUAL": 81,
    "KEYPAD0": 82,
    "KEYPAD1": 83,
    "KEYPAD2": 84,
    "KEYPAD3": 85,
    "KEYPAD4": 86,
    "KEYPAD5": 87,
    "KEYPAD6": 88,
    "KEYPAD7": 89,
    "F20": 90,
    "KEYPAD8": 91,
    "KEYPAD9": 92,
    "F5": 96,
    "F6": 97,
    "F7": 98,
    "F3": 99,
    "F8": 100,
    "F9": 101,
    "F11": 103,
    "F13": 105,
    "F16": 106,
    "F14": 107,
    "F10": 109,
    "F12": 111,
    "F15": 113,
    "HELP": 114,
    "HOME": 115,
    "PAGEUP": 116,
    "FORWARDDELETE": 117,
    "F4": 118,
    "END": 119,
    "F2": 120,
    "PAGEDOWN": 121,
    "F1": 122,
    "LEFT": 123,
    "RIGHT": 124,
    "DOWN": 125,
    "UP": 126,
}

SLEEP_INTERVAL = 0.01


async def move(x: int, y: int) -> None:
    event = core.CGEventCreateMouseEvent(
        None, kCGEventMouseMoved, CGPoint(x, y), kCGMouseButtonLeft
    )
    core.CGEventPost(kCGHIDEventTap, event)
    core.CFRelease(event)


async def click(
    button: str = "left", x: Optional[int] = None, y: Optional[int] = None
) -> None:
    if x is not None and y is not None:
        await move(x, y)
        await asyncio.sleep(SLEEP_INTERVAL)
    btn_map = {
        "left": kCGMouseButtonLeft,
        "right": kCGMouseButtonRight,
        "wheel": kCGMouseButtonCenter,  # middle/wheel button
        "middle": kCGMouseButtonCenter,  # alias for wheel
        "back": 3,  # macOS supports up to 31 mouse buttons
        "forward": 4,
    }
    if button not in btn_map:
        raise ValueError(f"Unknown button: {button}")
    btn = btn_map[button]
    if x is not None and y is not None:
        pt = CGPoint(x, y)
    else:
        loc = get_mouse_pos()
        pt = CGPoint(*loc)
    # Determine event types for the button
    if btn == kCGMouseButtonLeft:
        events = [kCGEventLeftMouseDown, kCGEventLeftMouseUp]
    elif btn == kCGMouseButtonRight:
        events = [kCGEventRightMouseDown, kCGEventRightMouseUp]
    elif btn == kCGMouseButtonCenter:
        events = [kCGEventOtherMouseDown, kCGEventOtherMouseUp]
    else:
        # For back/forward/other buttons, use OtherMouse events
        events = [kCGEventOtherMouseDown, kCGEventOtherMouseUp]
    for t in events:
        await asyncio.sleep(SLEEP_INTERVAL)
        event = core.CGEventCreateMouseEvent(None, t, pt, btn)
        core.CGEventPost(kCGHIDEventTap, event)
        core.CFRelease(event)


async def double_click(x: Optional[int] = None, y: Optional[int] = None) -> None:
    if x is not None and y is not None:
        await move(x, y)
        await asyncio.sleep(SLEEP_INTERVAL)
        pt = CGPoint(x, y)
    else:
        loc = get_mouse_pos()
        pt = CGPoint(*loc)
    event_dclick = core.CGEventCreateMouseEvent(
        None, kCGEventLeftMouseDown, pt, kCGMouseButtonLeft
    )
    core.CGEventSetIntegerValueField(event_dclick, kCGMouseEventClickState, 1)
    core.CGEventPost(kCGHIDEventTap, event_dclick)
    core.CGEventSetType(event_dclick, kCGEventLeftMouseUp)
    core.CGEventPost(kCGHIDEventTap, event_dclick)
    await asyncio.sleep(SLEEP_INTERVAL)
    core.CGEventSetIntegerValueField(event_dclick, kCGMouseEventClickState, 2)
    core.CGEventSetType(event_dclick, kCGEventLeftMouseDown)
    core.CGEventPost(kCGHIDEventTap, event_dclick)
    core.CGEventSetType(event_dclick, kCGEventLeftMouseUp)
    core.CGEventPost(kCGHIDEventTap, event_dclick)
    await asyncio.sleep(SLEEP_INTERVAL)
    core.CFRelease(event_dclick)


async def drag(path: list[tuple[int, int]]) -> None:
    if not path or len(path) < 2:
        raise ValueError("Path must contain at least two points")
    pt_start = CGPoint(*path[0])
    event = core.CGEventCreateMouseEvent(
        None, kCGEventLeftMouseDown, pt_start, kCGMouseButtonLeft
    )
    core.CGEventPost(kCGHIDEventTap, event)
    core.CFRelease(event)
    await asyncio.sleep(SLEEP_INTERVAL)
    for point in path[1:-1]:
        pt = CGPoint(*point)
        event = core.CGEventCreateMouseEvent(
            None, kCGEventLeftMouseDragged, pt, kCGMouseButtonLeft
        )
        core.CGEventPost(kCGHIDEventTap, event)
        core.CFRelease(event)
        await asyncio.sleep(SLEEP_INTERVAL)
    pt_end = CGPoint(*path[-1])
    event = core.CGEventCreateMouseEvent(
        None, kCGEventLeftMouseDragged, pt_end, kCGMouseButtonLeft
    )
    core.CGEventPost(kCGHIDEventTap, event)
    core.CFRelease(event)
    await asyncio.sleep(SLEEP_INTERVAL)
    event = core.CGEventCreateMouseEvent(
        None, kCGEventLeftMouseUp, pt_end, kCGMouseButtonLeft
    )
    core.CGEventPost(kCGHIDEventTap, event)
    core.CFRelease(event)


def get_mouse_pos() -> tuple[float, float]:
    event = core.CGEventCreate(None)
    pt = core.CGEventGetLocation(event)
    core.CFRelease(event)
    return pt.x, pt.y


async def key_press(keys: list[str]) -> None:
    # macOS modifier flags
    MODIFIER_FLAGS = {
        "SHIFT": 0x20000,  # kCGEventFlagMaskShift (correct value)
        "CTRL": 0x40000,  # kCGEventFlagMaskControl (correct value)
        "ALT": 0x80000,  # kCGEventFlagMaskAlternate (correct value)
        "CMD": 0x100000,  # kCGEventFlagMaskCommand (correct value)
        "OPTION": 0x80000,  # alias for ALT
    }

    keys_upper = [k.upper() for k in keys]
    modifiers = [k for k in keys_upper if k in MODIFIER_FLAGS]
    normal_keys = [k for k in keys_upper if k not in MODIFIER_FLAGS]

    if not normal_keys:
        keycodes = [KEY_MAP[k] for k in modifiers if k in KEY_MAP]
        for keycode in keycodes:
            event_down = core.CGEventCreateKeyboardEvent(None, keycode, True)
            core.CGEventPost(kCGHIDEventTap, event_down)
            core.CFRelease(event_down)
        await asyncio.sleep(SLEEP_INTERVAL)
        for keycode in reversed(keycodes):
            event_up = core.CGEventCreateKeyboardEvent(None, keycode, False)
            core.CGEventPost(kCGHIDEventTap, event_up)
            core.CFRelease(event_up)
        return

    flags = 0
    for mod in modifiers:
        flags |= MODIFIER_FLAGS[mod]

    modifier_keycodes = []
    for mod in modifiers:
        if mod in KEY_MAP:
            keycode = KEY_MAP[mod]
            modifier_keycodes.append(keycode)
            event_down = core.CGEventCreateKeyboardEvent(None, keycode, True)
            core.CGEventPost(kCGHIDEventTap, event_down)
            core.CFRelease(event_down)

    for key in normal_keys:
        k = key.upper()
        if k in KEY_MAP:
            keycode = KEY_MAP[k]
        elif len(key) == 1 and k.upper() in KEY_MAP:
            keycode = KEY_MAP[k.upper()]
        else:
            continue

        event_down = core.CGEventCreateKeyboardEvent(None, keycode, True)
        if flags:
            core.CGEventSetFlags(event_down, flags)
        core.CGEventPost(kCGHIDEventTap, event_down)
        core.CFRelease(event_down)

        event_up = core.CGEventCreateKeyboardEvent(None, keycode, False)
        if flags:
            core.CGEventSetFlags(event_up, flags)
        core.CGEventPost(kCGHIDEventTap, event_up)
        core.CFRelease(event_up)

    await asyncio.sleep(SLEEP_INTERVAL)

    for keycode in reversed(modifier_keycodes):
        event_up = core.CGEventCreateKeyboardEvent(None, keycode, False)
        core.CGEventPost(kCGHIDEventTap, event_up)
        core.CFRelease(event_up)


async def type_text(text: str) -> None:
    # Types text using CGEventKeyboardSetUnicodeString for Unicode support
    # Reference: https://developer.apple.com/documentation/coregraphics/1454426-cgeventkeyboardsetunicodestring
    for char in text:
        # Create a key down event with dummy keycode (0)
        event_down = core.CGEventCreateKeyboardEvent(None, 0, True)
        # Set the Unicode string for the event
        utf16 = char.encode("utf-16-le")
        length = len(utf16) // 2
        buf = (ctypes.c_uint16 * length).from_buffer_copy(utf16)
        core.CGEventKeyboardSetUnicodeString(event_down, length, buf)
        core.CGEventPost(kCGHIDEventTap, event_down)
        core.CFRelease(event_down)
        await asyncio.sleep(SLEEP_INTERVAL)
        # Key up event
        event_up = core.CGEventCreateKeyboardEvent(None, 0, False)
        core.CGEventKeyboardSetUnicodeString(event_up, length, buf)
        core.CGEventPost(kCGHIDEventTap, event_up)
        core.CFRelease(event_up)
        await asyncio.sleep(SLEEP_INTERVAL)


async def scroll(
    scroll_x: int, scroll_y: int, x: Optional[int] = None, y: Optional[int] = None
) -> None:
    if x is not None and y is not None:
        await move(x, y)
        await asyncio.sleep(SLEEP_INTERVAL)
    event = None
    if scroll_y != 0 and scroll_x != 0:
        # Both directions: 2 axes
        event = core.CGEventCreateScrollWheelEvent(
            None, kCGScrollEventUnitLine, 2, int(scroll_y), int(scroll_x)
        )
    elif scroll_y != 0:
        event = core.CGEventCreateScrollWheelEvent(
            None, kCGScrollEventUnitLine, 1, int(scroll_y)
        )
    elif scroll_x != 0:
        event = core.CGEventCreateScrollWheelEvent(
            None, kCGScrollEventUnitLine, 2, 0, int(scroll_x)
        )
    if event:
        core.CGEventPost(kCGHIDEventTap, event)
        core.CFRelease(event)


def raw_screenshot() -> str:
    # Use CoreGraphics to capture the main display and convert to PNG base64 using PIL
    # Get display ID and CGImageRef
    core.CGMainDisplayID.restype = ctypes.c_uint32
    display_id = core.CGMainDisplayID()
    core.CGDisplayCreateImage.restype = CGImageRef
    image_ref = core.CGDisplayCreateImage(display_id)

    # Get image width, height, and bytes per row
    core.CGImageGetWidth.restype = ctypes.c_size_t
    core.CGImageGetHeight.restype = ctypes.c_size_t
    core.CGImageGetBytesPerRow.restype = ctypes.c_size_t
    width = core.CGImageGetWidth(image_ref)
    height = core.CGImageGetHeight(image_ref)
    bytes_per_row = core.CGImageGetBytesPerRow(image_ref)

    # Get data provider and data pointer
    core.CGImageGetDataProvider.restype = ctypes.c_void_p
    data_provider = core.CGImageGetDataProvider(image_ref)
    core.CGDataProviderCopyData.restype = ctypes.c_void_p
    cfdata = core.CGDataProviderCopyData(data_provider)
    core.CFDataGetBytePtr.restype = ctypes.POINTER(ctypes.c_ubyte)
    data_ptr = core.CFDataGetBytePtr(cfdata)
    core.CFDataGetLength.restype = ctypes.c_long
    data_len = core.CFDataGetLength(cfdata)

    # Get pixel format (assume RGBA8888)
    # Create PIL Image from buffer
    img = Image.frombuffer("RGBA", (width, height), data_ptr, "raw", "RGBA", 0, 1)
    img = img.convert("RGB")  # Remove alpha for PNG

    # Encode to base64 PNG
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Release CoreFoundation objects
    core.CFRelease(cfdata)
    core.CFRelease(data_provider)
    core.CFRelease(image_ref)
    return img_str


async def screenshot() -> str:
    # Use PIL to capture the screen and return as base64 PNG string
    from PIL import ImageGrab

    img = ImageGrab.grab()
    # Resize to match dimensions() output (physical pixel size)
    width, height = await dimensions()
    if img.size != (width, height):
        img = img.resize((width, height), Image.LANCZOS)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


async def dimensions() -> tuple[int, int]:
    # Get main display ID
    core.CGMainDisplayID.restype = ctypes.c_uint32
    display_id = core.CGMainDisplayID()

    # Get pixel dimensions
    core.CGDisplayPixelsWide.restype = ctypes.c_size_t
    core.CGDisplayPixelsHigh.restype = ctypes.c_size_t
    width = core.CGDisplayPixelsWide(display_id)
    height = core.CGDisplayPixelsHigh(display_id)
    return width, height


async def wait() -> None:
    await asyncio.sleep(1)
