import socket
import pickle
from cua.contracts.action import (
    CuaComputerAction,
    CuaHumanConfirmAction,
    CuaHumanInputAction,
    CuaReasoningAction,
)
from .common import handle_non_computer_action
from cua.bridges import BaseCuaBridge


class RemoteCuaOperatorClient:
    def __init__(
        self, bridge: BaseCuaBridge, host: str = "127.0.0.1", port: int = 54321
    ) -> None:
        self.bridge: BaseCuaBridge = bridge
        self.host: str = host
        self.port: int = port

    def send_command(self, command: str, payload: object = None) -> object:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(pickle.dumps({"command": command, "payload": payload}) + b"END")
            data: bytes = b""
            while True:
                part: bytes = s.recv(4096)
                if not part:
                    break
                data += part
                if data.endswith(b"END"):
                    data = data[:-3]
                    break
            result: object = pickle.loads(data)
            if isinstance(result, dict) and "error" in result:
                raise RuntimeError(result["error"])
            return result

    def apply_computer_action(self, action: CuaComputerAction) -> None:
        print(f"Sending action: {action}")
        screenshot: str = self.send_command("action", action)
        self.bridge.complete_active(screenshot)

    def run(self) -> None:
        info: dict = self.send_command("init")
        self.bridge.init(info["dimensions"], info["environment"])
        while True:
            action = self.bridge.active_action()
            if action is None:
                break
            if isinstance(action, CuaComputerAction):
                self.apply_computer_action(action)
            elif isinstance(
                action, (CuaHumanConfirmAction, CuaHumanInputAction, CuaReasoningAction)
            ):
                handle_non_computer_action(self.bridge, action)
