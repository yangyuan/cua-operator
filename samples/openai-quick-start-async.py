# pip install cua-operator openai
import asyncio
from cua_operator.bridges import OpenAICuaBridge
from cua_operator.operators import LocalCuaOperator
from openai import AsyncOpenAI


async def main():
    client = AsyncOpenAI(
        api_key="{OPENAI_API_KEY}"
    )

    operator = LocalCuaOperator(bridge=OpenAICuaBridge(client))
    await operator.run_async()


if __name__ == "__main__":
    asyncio.run(main())
