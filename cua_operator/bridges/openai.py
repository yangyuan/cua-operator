import sys
from typing import Optional

from openai import OpenAI, AsyncOpenAI
from cua_operator.bridges.base import BaseCuaBridge
from cua_operator.contracts.action import (
    CuaAction,
    CuaComputerAction,
    CuaComputerClickAction,
    CuaComputerDoubleClickAction,
    CuaComputerDragAction,
    CuaComputerKeyPressAction,
    CuaComputerMoveAction,
    CuaComputerScreenshotAction,
    CuaComputerScrollAction,
    CuaComputerTypeTextAction,
    CuaComputerWaitAction,
    CuaHumanConfirmAction,
    CuaHumanInputAction,
    CuaReasoningAction,
)
from openai.types.responses import (
    Response,
    ResponseOutputText,
    EasyInputMessageParam,
    ResponseComputerToolCallOutputScreenshotParam,
)
from openai.types.responses.response_input_param import ComputerCallOutput


class OpenAICuaBridge(BaseCuaBridge):
    def __init__(
        self,
        client: OpenAI | AsyncOpenAI,
        welcome_message: str = "Welcome to CUA Operator! Please enter your first task to get started.",
    ) -> None:
        self.client: OpenAI | AsyncOpenAI = client
        self.welcome_message: str = welcome_message
        self._dimensions: Optional[tuple[int, int]] = None
        self._environment: Optional[str] = None
        self._last_response_id: Optional[str] | None = None
        self._active_item = None
        self._acknowledged_safety_checks = None
        self._pending_items = []
        self._completed_items = []

    async def init(self, dimensions: tuple[int, int], environment: str) -> None:
        self._dimensions = dimensions
        self._environment = environment

    async def input(self, user_input: str) -> None:
        # input is also allowed if there are no active action
        if self._active_item is not None:
            # then it must be a message
            self._completed_items.append(self._active_item)
            self._active_item = None

        item = EasyInputMessageParam(content=user_input, role="user", type="message")
        self._completed_items.append(item)
        await self._advance()

    async def bypass(self) -> None:
        if self._active_item is None:
            raise ValueError("No active item to bypass.")
        if self._active_item.type != "reasoning":
            raise ValueError("Bypass can only be called on a reasoning item.")
        # self._completed_items.append(self._active_item)
        self._active_item = None
        if self._pending_items is not None and len(self._pending_items) > 0:
            self._active_item = self._pending_items.pop(0)

    async def confirm(self, confirmed: bool) -> None:
        if self._active_item is None:
            raise ValueError("No active item to confirm.")

        if confirmed:
            self._acknowledged_safety_checks = self._active_item.pending_safety_checks

    async def complete_active(self, screenshot_base64: str) -> None:
        if self._active_item is None:
            raise ValueError("No active item to complete.")

        call_output = ComputerCallOutput(
            type="computer_call_output",
            call_id=self._active_item.call_id,
            acknowledged_safety_checks=self._acknowledged_safety_checks,
            output=ResponseComputerToolCallOutputScreenshotParam(
                type="input_image",
                image_url=f"data:image/png;base64,{screenshot_base64}",
            ),
        )
        # confirm buffer consumed
        self._acknowledged_safety_checks = None

        # Mark the active item as completed
        self._completed_items.append(self._active_item)
        self._active_item = None

        self._completed_items.append(call_output)

        if self._pending_items is not None and len(self._pending_items) > 0:
            self._active_item = self._pending_items.pop(0)
        else:
            await self._advance()

    def computer_call_to_action(self, item) -> CuaComputerAction:
        action = item.action
        action_type = action.type

        """
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
        if action_type == "screenshot":
            return CuaComputerScreenshotAction()
        elif action_type == "wait":
            return CuaComputerWaitAction()
        elif action_type == "click":
            return CuaComputerClickAction(button=action.button, x=action.x, y=action.y)
        elif action_type == "double_click":
            return CuaComputerDoubleClickAction(x=action.x, y=action.y)
        elif action_type == "keypress":
            if sys.platform == "darwin":
                key_remap = {
                    "/": "/",
                    "\\": "\\",
                    "ALT": "ALT",
                    "ARROWDOWN": "DOWN",
                    "ARROWLEFT": "LEFT",
                    "ARROWRIGHT": "RIGHT",
                    "ARROWUP": "UP",
                    "BACKSPACE": "DELETE",
                    "CAPSLOCK": "CAPSLOCK",
                    "CMD": "CMD",
                    "CTRL": "CTRL",
                    "DEL": "DELETE",
                    "DELETE": "DELETE",
                    "END": "END",
                    "ENTER": "RETURN",
                    "ESC": "ESC",
                    "HOME": "HOME",
                    "INSERT": "INSERT",
                    "OPTION": "ALT",
                    "PAGEDOWN": "PAGEDOWN",
                    "PAGEUP": "PAGEUP",
                    "SHIFT": "SHIFT",
                    "SPACE": "SPACE",
                    "SUPER": "CMD",
                    "TAB": "TAB",
                    "WIN": "CMD",
                }
            else:
                # Windows key mapping (original)
                key_remap = {
                    "/": "/",
                    "\\": "\\",
                    "ALT": "MENU",
                    "ARROWDOWN": "DOWN",
                    "ARROWLEFT": "LEFT",
                    "ARROWRIGHT": "RIGHT",
                    "ARROWUP": "UP",
                    "BACKSPACE": "BACK",
                    "CAPSLOCK": "CAPITAL",
                    "CMD": "LWIN",  # Windows key (left)
                    "CTRL": "CONTROL",
                    "DEL": "DELETE",
                    "DELETE": "DELETE",
                    "END": "END",
                    "ENTER": "RETURN",
                    "ESC": "ESCAPE",
                    "HOME": "HOME",
                    "INSERT": "INSERT",
                    "OPTION": "MENU",  # Alt/Option
                    "PAGEDOWN": "NEXT",
                    "PAGEUP": "PRIOR",
                    "SHIFT": "SHIFT",
                    "SPACE": "SPACE",
                    "SUPER": "LWIN",  # Windows key (left)
                    "TAB": "TAB",
                    "WIN": "LWIN",  # Windows key (left)
                }
            remapped_keys = [key_remap.get(k, k) for k in action.keys]
            return CuaComputerKeyPressAction(keys=remapped_keys)
        elif action_type == "type":
            return CuaComputerTypeTextAction(text=action.text)
        elif action_type == "move":
            return CuaComputerMoveAction(x=action.x, y=action.y)
        elif action_type == "scroll":
            return CuaComputerScrollAction(
                scroll_x=action.scroll_x,
                scroll_y=action.scroll_y,
                x=action.x,
                y=action.y,
            )
        elif action_type == "drag":
            return CuaComputerDragAction(
                path=[(point.x, point.y) for point in action.path],
            )

    async def active_action(self) -> CuaAction:
        # if active item is a computer call action with acknowledge, yield a human_confirm action, clear other pending actions if there is any.
        # if active item is a computer call action with acknowledge, but confirm is called, yield a computer_call action
        # if active item is a computer call action without acknowledge, yield a computer_call action
        # once the computer call action is completed, call self.bridge.complete(), so bridge knows the action is done.
        # depends on if there are more pending actions, the bridge might or might not call advance() to get the next action.
        # if active internal item is a assistant message, yield a human_input action, clear other pending actions if there is any.
        if self._active_item is not None:
            if self._active_item.type == "computer_call":
                if (
                    not self._acknowledged_safety_checks
                    and self._active_item.pending_safety_checks
                    and len(self._active_item.pending_safety_checks) > 0
                ):
                    message = ";".join(
                        [
                            check.message
                            for check in self._active_item.pending_safety_checks
                        ]
                    )
                    return CuaHumanConfirmAction(message=message)
                return self.computer_call_to_action(self._active_item)
            elif self._active_item.type == "message":  # print messages
                if self._active_item.role == "assistant":
                    message = ";".join(
                        [content.text for content in self._active_item.content]
                    )
                    return CuaHumanInputAction(message=message)
                else:
                    raise ValueError(
                        "Unexpected role for active item: {}".format(
                            self._active_item.role
                        )
                    )
            elif self._active_item.type == "reasoning":
                return CuaReasoningAction()

        elif self._active_item is None:
            return CuaHumanInputAction(message=self.welcome_message)

    def _assert_check(self, response: Response) -> None:
        assert (
            response.id is not None
        ), "Response ID must not be None. Response: {}".format(response)

        _count_message = 0
        _count_computer_call = 0
        _count_reasoning_call = 0
        for item in response.output:
            if item.type == "message":
                assert item.role in [
                    "assistant"
                ], f"Only assistant messages are expected, got {item.role}"

                assert isinstance(item.content, list) and all(
                    isinstance(c, ResponseOutputText) for c in item.content
                ), "Message content must not be empty and must be a list of ResponseOutputText. Got: {}".format(
                    item.content
                )

                # separate assertion for less confidence
                assert (
                    len(item.content) == 1
                ), "Message content must contain exactly one ResponseOutputText item."
                _count_message += 1
            elif item.type == "computer_call":
                assert item.action is not None, "Computer call action must not be None."

                assert item.action.type in [
                    "screenshot",
                    "wait",
                    "click",
                    "double_click",
                    "keypress",
                    "type",
                    "move",
                    "scroll",
                    "drag",
                ], "Computer call action must be one of screenshot, wait, click, keypress, type, move, scroll, drag"
                _count_computer_call += 1
            elif item.type == "reasoning":
                _count_reasoning_call += 1

        assert (
            _count_message + _count_computer_call + _count_reasoning_call
        ) > 0, "Response must contain at least one message or computer call item."
        assert (
            _count_message < 2 and _count_computer_call < 2
        ), "Response must contain at most one message and one computer call item."
        assert (_count_reasoning_call + _count_computer_call + _count_message) == len(
            response.output
        ), "Response must contain only message, computer call, or reasoning items. "

    async def _advance(self) -> None:
        assert (
            self._environment is not None
        ), "Environment must be set before advancing."
        assert self._dimensions is not None, "Dimensions must be set before advancing."

        assert (
            self._active_item is None
        ), "There is an active item that needs to be completed before advancing."
        assert (
            self._pending_items is not None and len(self._pending_items) == 0
        ), "There are no pending items to process."

        response = self.client.responses.create(
            model="computer-use-preview",
            previous_response_id=self._last_response_id,
            input=[self._completed_items[-1]],
            truncation="auto",
            tools=[
                {
                    "type": "computer-preview",
                    "display_width": self._dimensions[0],
                    "display_height": self._dimensions[1],
                    "environment": self._environment,
                }
            ],
        )

        if isinstance(self.client, AsyncOpenAI):
            response = await response

        self._last_response_id = response.id

        self._assert_check(response)

        self._pending_items = response.output
        # move first from pending items to active item
        self._active_item = self._pending_items.pop(0)
