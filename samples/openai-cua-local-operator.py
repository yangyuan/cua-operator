# pip install cua-operator openai
import asyncio
from cua_operator.bridges import OpenAICuaBridge
from cua_operator.operators import LocalCuaOperator
from openai import OpenAI


async def main():
    client = OpenAI()
    operator = LocalCuaOperator(bridge=OpenAICuaBridge(client))
    await operator.run_async()


if __name__ == "__main__":
    asyncio.run(main())
