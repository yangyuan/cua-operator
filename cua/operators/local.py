import asyncio
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

    async def _apply_computer_action(self, action: CuaComputerAction) -> None:
        screenshot = await perform_computer_action(action)
        await self.bridge.complete_active(screenshot)

    async def run_async(self) -> None:
        dimensions = await cua.tools.dimensions()
        if sys.platform == "win32":
            environment = "windows"
        elif sys.platform == "darwin":
            environment = "mac"
        else:
            raise ValueError(f"Unsupported platform: {sys.platform}")
        await self.bridge.init(dimensions, environment)

        while True:
            action = await self.bridge.active_action()

            if action is None:
                # usually only happen when user confirmed its done
                break
            if isinstance(action, CuaComputerAction):
                await self._apply_computer_action(action)
            elif isinstance(
                action, (CuaHumanConfirmAction, CuaHumanInputAction, CuaReasoningAction)
            ):
                await handle_non_computer_action(self.bridge, action)

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_async())
        loop.close()
