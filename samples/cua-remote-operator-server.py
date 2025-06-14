import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from cua_operator.operators import RemoteCuaOperatorServer


async def main():
    server = RemoteCuaOperatorServer(host="0.0.0.0", port=54321)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
