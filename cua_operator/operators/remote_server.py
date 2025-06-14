import sys
import asyncio
import pickle
import cua_operator.tools
from .common import perform_computer_action


class RemoteCuaOperatorServer:
    host: str
    port: int

    def __init__(self, host: str = "127.0.0.1", port: int = 54321) -> None:
        self.host: str = host
        self.port: int = port

    async def serve_forever(self) -> None:
        server = await asyncio.start_server(self._handle_client, self.host, self.port)
        async with server:
            await server.serve_forever()

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            while True:
                data: bytes = b""
                while True:
                    part: bytes = await reader.read(4096)
                    if not part:
                        writer.close()
                        await writer.wait_closed()
                        return
                    data += part
                    if data.endswith(b"END"):
                        data = data[:-3]
                        break
                try:
                    request: dict = pickle.loads(data)
                    if isinstance(request, dict) and "command" in request:
                        if request["command"] == "init":
                            info: dict[str, object] = await self._get_init_info()
                            writer.write(pickle.dumps(info) + b"END")
                            await writer.drain()
                        elif request["command"] == "action":
                            result: object = await perform_computer_action(
                                request["payload"]
                            )
                            writer.write(pickle.dumps(result) + b"END")
                            await writer.drain()
                        else:
                            writer.write(
                                pickle.dumps({"error": "Unknown command"}) + b"END"
                            )
                            await writer.drain()
                    else:
                        writer.write(
                            pickle.dumps({"error": "Invalid request"}) + b"END"
                        )
                        await writer.drain()
                except Exception as e:
                    writer.write(pickle.dumps({"error": str(e)}) + b"END")
                    await writer.drain()
        except Exception:
            pass

    async def _get_init_info(self) -> dict[str, object]:
        dimensions: tuple[int, int] = await cua_operator.tools.dimensions()
        if sys.platform == "win32":
            environment: str = "windows"
        elif sys.platform == "darwin":
            environment = "mac"
        else:
            environment = sys.platform
        return {"dimensions": dimensions, "environment": environment}
