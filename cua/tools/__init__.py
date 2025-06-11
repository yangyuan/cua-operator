import sys

"""
# System Tools
Dimensions

# CUA Tools
Click
DoubleClick
Drag
KeyPress
Move
Screenshot
Scroll
Type
Wait
"""

if sys.platform == "win32":
    from .win32 import (
        dimensions,
        click,
        double_click,
        drag,
        key_press,
        move,
        screenshot,
        scroll,
        wait,
        type_text,
    )
elif sys.platform == "darwin":
    from .darwin import (
        dimensions,
        click,
        double_click,
        drag,
        key_press,
        move,
        screenshot,
        scroll,
        wait,
        type_text,
    )
