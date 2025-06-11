import sys
from .common import perform_computer_action, handle_non_computer_action
import cua.tools
from cua.bridges import BaseCuaBridge
from cua.contracts.action import (
    CuaComputerAction,
    CuaHumanConfirmAction,
    CuaHumanInputAction,
    CuaReasoningAction,
)


class LocalCuaOperator:
    def __init__(self, bridge: BaseCuaBridge) -> None:
        self.bridge: BaseCuaBridge = bridge

    def apply_computer_action(self, action: CuaComputerAction) -> None:
        screenshot = perform_computer_action(action)
        self.bridge.complete_active(screenshot)

    def run(self) -> None:
        dimensions = cua.tools.dimensions()
        if sys.platform == "win32":
            environment = "windows"
        elif sys.platform == "darwin":
            environment = "mac"
        else:
            raise ValueError(f"Unsupported platform: {sys.platform}")
        self.bridge.init(dimensions, environment)

        while True:
            action = self.bridge.active_action()

            if action is None:
                # usually only happen when user confirmed its done
                break
            if isinstance(action, CuaComputerAction):
                self.apply_computer_action(action)
            elif isinstance(
                action, (CuaHumanConfirmAction, CuaHumanInputAction, CuaReasoningAction)
            ):
                handle_non_computer_action(self.bridge, action)
