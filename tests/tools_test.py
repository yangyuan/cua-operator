import cua_operator.tools
import pytest


@pytest.mark.asyncio
async def test_import():
    assert hasattr(cua_operator.tools, "move")
    assert hasattr(cua_operator.tools, "click")
    assert hasattr(cua_operator.tools, "screenshot")


@pytest.mark.asyncio
async def test_dimensions_screenshot():
    dimensions = await cua_operator.tools.dimensions()
    assert isinstance(dimensions, tuple)
    assert len(dimensions) == 2
    assert isinstance(dimensions[0], int)
    assert isinstance(dimensions[1], int)
    assert dimensions[0] > 0
    assert dimensions[1] > 0

    screenshot = await cua_operator.tools.screenshot()
    assert isinstance(screenshot, str)

    # decode base64 and check PNG size matches dimensions
    import base64
    from io import BytesIO
    from PIL import Image

    img = Image.open(BytesIO(base64.b64decode(screenshot)))
    assert img.size == dimensions
