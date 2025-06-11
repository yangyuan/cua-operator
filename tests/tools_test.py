import cua.tools


def test_import():
    assert hasattr(cua.tools, "move")
    assert hasattr(cua.tools, "click")
    assert hasattr(cua.tools, "screenshot")


def test_dimensions_screenshot():
    dimensions = cua.tools.dimensions()
    assert isinstance(dimensions, tuple)
    assert len(dimensions) == 2
    assert isinstance(dimensions[0], int)
    assert isinstance(dimensions[1], int)
    assert dimensions[0] > 0
    assert dimensions[1] > 0

    screenshot = cua.tools.screenshot()
    assert isinstance(screenshot, str)

    # decode base64 and check PNG size matches dimensions
    import base64
    from io import BytesIO
    from PIL import Image

    img = Image.open(BytesIO(base64.b64decode(screenshot)))
    assert img.size == dimensions
