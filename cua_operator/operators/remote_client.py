import asyncio
import pickle
from cua_operator.contracts.action import (
    CuaComputerAction,
    CuaHumanConfirmAction,
    CuaHumanInputAction,
    CuaReasoningAction,
)
from .common import handle_non_computer_action
from cua_operator.bridges import BaseCuaBridge


class RemoteCuaOperatorClient:
    def __init__(
        self, bridge: BaseCuaBridge, host: str = "127.0.0.1", port: int = 54321
    ) -> None:
        self.bridge: BaseCuaBridge = bridge
        self.host: str = host
        self.port: int = port

    async def _send_command(self, command: str, payload: object = None) -> object:
        reader, writer = await asyncio.open_connection(self.host, self.port)
        writer.write(pickle.dumps({"command": command, "payload": payload}) + b"END")
        await writer.drain()
        data: bytes = b""
        while True:
            part: bytes = await reader.read(4096)
            if not part:
                break
            data += part
            if data.endswith(b"END"):
                data = data[:-3]
                break
        writer.close()
        await writer.wait_closed()
        result: object = pickle.loads(data)
        if isinstance(result, dict) and "error" in result:
            raise RuntimeError(result["error"])
        return result

    async def _apply_computer_action(self, action: CuaComputerAction) -> None:
        print(f"Sending action: {action}")
        screenshot: str = await self._send_command("action", action)
        await self.bridge.complete_active(screenshot)

    async def run_async(self) -> None:
        info: dict = await self._send_command("init")
        await self.bridge.init(info["dimensions"], info["environment"])
        while True:
            action = await self.bridge.active_action()
            if action is None:
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
