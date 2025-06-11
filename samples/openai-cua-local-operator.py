import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cua.bridges import OpenAICuaBridge
from cua.operators import LocalCuaOperator
from openai import OpenAI

if __name__ == "__main__":
    client = OpenAI()

    operator = LocalCuaOperator(bridge=OpenAICuaBridge(client))
    operator.run()
