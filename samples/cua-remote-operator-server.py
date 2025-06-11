import sys, os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cua.operators import RemoteCuaOperatorServer

if __name__ == "__main__":
    server = RemoteCuaOperatorServer(host="0.0.0.0", port=54321)
    asyncio.run(server.serve_forever())
