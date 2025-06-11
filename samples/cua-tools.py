import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cua.tools import *

x, y = dimensions()
move(500, 300)
for button in ["left", "right", "wheel", "back", "forward"]:
    click(button=button)
double_click()
key_press(["A"])
key_press(["SHIFT", "A"])
type_text("Hello World!")
type_text("中文")
drag([(300, 300), (600, 600)])
scroll(scroll_x=0, scroll_y=410)
scroll(scroll_x=410, scroll_y=0)
screenshot_base64 = screenshot()
wait()
