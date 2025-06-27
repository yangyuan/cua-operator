# pip install cua-operator openai
import asyncio
from cua_operator.bridges import OpenAICuaBridge
from cua_operator.operators import RemoteCuaOperatorClient
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
