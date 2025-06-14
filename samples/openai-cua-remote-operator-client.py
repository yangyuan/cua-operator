import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from cua.bridges import OpenAICuaBridge
from cua.operators import RemoteCuaOperatorClient
from openai import OpenAI


async def main():
    client = OpenAI()

    operator = RemoteCuaOperatorClient(
        bridge=OpenAICuaBridge(client),
        host="127.0.0.1",
        port=54321,
    )
    await operator.run_async()


if __name__ == "__main__":
    asyncio.run(main())
