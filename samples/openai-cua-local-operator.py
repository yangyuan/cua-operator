import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from cua.bridges import OpenAICuaBridge
from cua.operators import LocalCuaOperator
from openai import OpenAI


async def main():
    client = OpenAI()
    operator = LocalCuaOperator(bridge=OpenAICuaBridge(client))
    await operator.run_async()


if __name__ == "__main__":
    asyncio.run(main())
