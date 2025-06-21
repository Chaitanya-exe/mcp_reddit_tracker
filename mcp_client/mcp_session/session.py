import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def create_session() -> ClientSession:
    try:
        server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../mcp_server/main.py"))
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
                print("✅ MCP Session initialized successfully")
                return session
    except Exception as e:
        import traceback
        print(f"❌ Error occurred initializing session: {str(e)}")
        traceback.print_exc()
        return None
