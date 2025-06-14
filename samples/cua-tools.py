import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from cua.tools import *


async def main():
    x, y = await dimensions()
    await move(500, 300)
    for button in ["left", "right", "wheel", "back", "forward"]:
        await click(button=button)
    await double_click()
    await key_press(["A"])
    await key_press(["SHIFT", "A"])
    await type_text("Hello World!")
    await type_text("中文")
    await drag([(300, 300), (600, 600)])
    await scroll(scroll_x=0, scroll_y=410)
    await scroll(scroll_x=410, scroll_y=0)
    screenshot_base64 = await screenshot()
    await wait()


if __name__ == "__main__":
    asyncio.run(main())
