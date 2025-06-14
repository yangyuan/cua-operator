import cua_operator.tools
from cua_operator.bridges.base import BaseCuaBridge
from cua_operator.contracts.action import (
    CuaAction,
    CuaComputerAction,
    CuaComputerClickAction,
    CuaComputerDoubleClickAction,
    CuaComputerScreenshotAction,
    CuaComputerWaitAction,
    CuaComputerMoveAction,
    CuaComputerKeyPressAction,
    CuaComputerTypeTextAction,
    CuaComputerScrollAction,
    CuaComputerDragAction,
    CuaHumanConfirmAction,
    CuaHumanInputAction,
    CuaReasoningAction,
)


async def perform_computer_action(action: CuaComputerAction) -> str:
    if isinstance(action, CuaComputerScreenshotAction):
        print(action)
    elif isinstance(action, CuaComputerWaitAction):
        print(action)
        await cua_operator.tools.wait()
    elif isinstance(action, CuaComputerClickAction):
        print(action)
        await cua_operator.tools.click(action.button, action.x, action.y)
    elif isinstance(action, CuaComputerDoubleClickAction):
        print(action)
        await cua_operator.tools.double_click(action.x, action.y)
    elif isinstance(action, CuaComputerMoveAction):
        print(action)
        await cua_operator.tools.move(action.x, action.y)
    elif isinstance(action, CuaComputerKeyPressAction):
        print(action)
        await cua_operator.tools.key_press(action.keys)
    elif isinstance(action, CuaComputerScrollAction):
        print(action)
        await cua_operator.tools.scroll(
            action.scroll_x, action.scroll_y, action.x, action.y
        )
    elif isinstance(action, CuaComputerTypeTextAction):
        print(action)
        await cua_operator.tools.type_text(action.text)
    elif isinstance(action, CuaComputerDragAction):
        print(action)
        if len(action.path) < 2:
            raise ValueError("Drag action requires at least two points in the path.")
        await cua_operator.tools.drag(action.path)
    else:
        raise ValueError(f"Unknown computer action type: {type(action)}")
    screenshot = await cua_operator.tools.screenshot()
    return screenshot


async def handle_non_computer_action(bridge: BaseCuaBridge, action: CuaAction) -> None:
    if isinstance(action, CuaHumanConfirmAction):
        user_input = input(f"{action.message}\nPlease confirm (y): ")
        if user_input.lower() in ["y", "yes"]:
            await bridge.confirm(True)
        else:
            await bridge.confirm(False)
    elif isinstance(action, CuaHumanInputAction):
        user_input = input(f"{action.message}\n")
        await bridge.input(user_input)
    elif isinstance(action, CuaReasoningAction):
        await bridge.bypass()
