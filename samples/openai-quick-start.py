# pip install cua-operator openai
from cua_operator.bridges import OpenAICuaBridge
from cua_operator.operators import LocalCuaOperator
from openai import OpenAI

client = OpenAI(
    api_key="{OPENAI_API_KEY}"
)

operator = LocalCuaOperator(bridge=OpenAICuaBridge(client))
operator.run()
