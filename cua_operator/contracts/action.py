from enum import StrEnum
from typing import Optional
from dataclasses import dataclass


class CuaActionType(StrEnum):
    USER_CONFIRM = "user_confirm"
    USER_INPUT = "user_input"
    REASONING = "reasoning"
    COMPUTER_CALL = "computer_call"


class CuaComputerActionType(StrEnum):
    SCREENSHOT = "screenshot"
    WAIT = "wait"
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    KEY_PRESS = "key_press"
    TYPE_TEXT = "type_text"
    MOVE = "move"
    SCROLL = "scroll"
    DRAG = "drag"


@dataclass
class CuaAction:
    action_type: CuaActionType

    def __init__(self, action_type: CuaActionType) -> None:
        self.action_type = action_type


@dataclass
class CuaReasoningAction(CuaAction):
    def __init__(self) -> None:
        super().__init__(action_type=CuaActionType.REASONING)


@dataclass
class CuaHumanAction(CuaAction):
    message: Optional[str]

    def __init__(self, action_type: CuaActionType, message: Optional[str]) -> None:
        super().__init__(action_type)
        self.message = message


@dataclass
class CuaHumanConfirmAction(CuaHumanAction):
    def __init__(self, message: Optional[str]) -> None:
        super().__init__(action_type=CuaActionType.USER_CONFIRM, message=message)


@dataclass
class CuaHumanInputAction(CuaHumanAction):
    def __init__(self, message: Optional[str]) -> None:
        super().__init__(action_type=CuaActionType.USER_INPUT, message=message)


@dataclass
class CuaComputerAction(CuaAction):
    computer_action_type: str

    def __init__(self, computer_action_type: CuaComputerActionType) -> None:
        super().__init__(action_type=CuaActionType.COMPUTER_CALL)
        self.computer_action_type = computer_action_type

    def __str__(self) -> str:
        return f"{self.computer_action_type}"


@dataclass
class CuaComputerScreenshotAction(CuaComputerAction):
    def __init__(self) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.SCREENSHOT)


@dataclass
class CuaComputerWaitAction(CuaComputerAction):
    def __init__(self) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.WAIT)


@dataclass
class CuaComputerClickAction(CuaComputerAction):
    button: str
    x: Optional[int]
    y: Optional[int]

    def __init__(self, button: str, x: Optional[int], y: Optional[int]) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.CLICK)
        self.button = button
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.computer_action_type} ({self.button} at {self.x}, {self.y})"


@dataclass
class CuaComputerDoubleClickAction(CuaComputerAction):
    x: Optional[int]
    y: Optional[int]

    def __init__(self, x: Optional[int], y: Optional[int]) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.DOUBLE_CLICK)
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.computer_action_type} at ({self.x}, {self.y})"


@dataclass
class CuaComputerKeyPressAction(CuaComputerAction):
    keys: list[str]

    def __init__(self, keys: list[str]) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.KEY_PRESS)
        self.keys = keys

    def __str__(self) -> str:
        return f"{self.computer_action_type} ({', '.join(self.keys)})"


@dataclass
class CuaComputerTypeTextAction(CuaComputerAction):
    text: str

    def __init__(self, text: str) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.TYPE_TEXT)
        self.text = text

    def __str__(self) -> str:
        return f"{self.computer_action_type} ({self.text})"


@dataclass
class CuaComputerMoveAction(CuaComputerAction):
    x: Optional[int]
    y: Optional[int]

    def __init__(self, x: Optional[int], y: Optional[int]) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.MOVE)
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.computer_action_type} ({self.x}, {self.y})"


@dataclass
class CuaComputerScrollAction(CuaComputerAction):
    scroll_x: int
    scroll_y: int
    x: Optional[int]
    y: Optional[int]

    def __init__(
        self, scroll_x: int, scroll_y: int, x: Optional[int], y: Optional[int]
    ) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.SCROLL)
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return (
            f"{self.computer_action_type} ({self.scroll_x}, {self.scroll_y}) at ({self.x}, {self.y})"
            if self.x is not None and self.y is not None
            else f"{self.computer_action_type} ({self.scroll_x}, {self.scroll_y})"
        )


@dataclass
class CuaComputerDragAction(CuaComputerAction):
    path: list[tuple[int, int]]

    def __init__(self, path: list[tuple[int, int]]) -> None:
        super().__init__(computer_action_type=CuaComputerActionType.DRAG)
        self.path = path

    def __str__(self) -> str:
        return f"{self.computer_action_type} ({self.path})"
