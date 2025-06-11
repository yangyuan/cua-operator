from abc import ABC, abstractmethod

from cua.contracts.action import CuaAction


class BaseCuaBridge(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def init(self, dimensions: tuple[int, int], environment: str) -> None:
        pass

    @abstractmethod
    def bypass(self) -> None:
        pass

    @abstractmethod
    def input(self, user_input: str) -> None:
        pass

    @abstractmethod
    def confirm(self, confirmed: bool) -> None:
        pass

    @abstractmethod
    def active_action(self) -> CuaAction:
        pass

    @abstractmethod
    def complete_active(self, screenshot_base64: str) -> None:
        pass
