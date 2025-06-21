import asyncio
import os
import sys
from llm_client import LLMClient
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def main():
    try:
        server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp_server/main.py"))
        print(f"Starting MCP server from: {server_path}")
        server_python = sys.executable

        env = {**os.environ, "PYTHONUNBUFFERED": "1"}
        
        params = StdioServerParameters(
            command=server_python,
            args=[server_path],
            env=env
        )
        
        async with stdio_client(params) as transport:
            async with ClientSession(*transport) as session:
                await session.initialize()

                llm = LLMClient(session)

                while True:
                    question = str(input("Ask about some content on a specific subreddit: "))

                    await llm.answer_query(question)


    except Exception as e:
        print(f"some error occured: {e}")



if __name__ == "__main__":
    asyncio.run(main())
