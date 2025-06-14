from abc import ABC, abstractmethod

from cua_operator.contracts.action import CuaAction


class BaseCuaBridge(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def init(self, dimensions: tuple[int, int], environment: str) -> None:
        pass

    @abstractmethod
    async def bypass(self) -> None:
        pass

    @abstractmethod
    async def input(self, user_input: str) -> None:
        pass

    @abstractmethod
    async def confirm(self, confirmed: bool) -> None:
        pass

    @abstractmethod
    async def active_action(self) -> CuaAction:
        pass

    @abstractmethod
    async def complete_active(self, screenshot_base64: str) -> None:
        pass
