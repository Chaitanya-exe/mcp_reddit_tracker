from mcp import ClientSession
from ollama import AsyncClient

class LLMClient:
    tools = []

    def __init__(self, mcp_session: ClientSession):
        self.model = "llama3.2"
        self.mcp_session = mcp_session
        self.system_prompt = "You are a analyzer who analyzes content from social media and tells various things about the data such as trends, anomalies, how the data can be helpful to user's purpose and help to answer specific questions about the data asked by the user. You are also given set of tools which you can use to assist the user."
        self.ollamaClient = AsyncClient()

    async def answer_query(self, question: str) -> None | str:
        try:
            if self.mcp_session is None:
                raise ValueError("MCP session is not initialized. The server may not be running correctly.")
                
            tools_response = await self.mcp_session.list_tools()

            print("Tools fetched successfully")

            available_tools =[
                {
                    "type":"function",
                    "function":{
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                }
                for tool in tools_response.tools
            ]

            response = await self.ollamaClient.chat(
                model= self.model,
                messages=[
                    {"role":"system", "content": self.system_prompt},
                    {"role":"user", "content": question}
                ],
                tools=available_tools,
                stream=False
            )

            tool_calls = response["message"].get("tool_calls", [])

            print(tool_calls)

            if not tool_calls:
                return response["message"]["content"]
            
            tool_results = []
            for call in tool_calls:
                tool_name = call["function"]["name"]
                tool_args = call["function"]["arguments"]
                tool_response = await self.mcp_session.call_tool(tool_name, tool_args)

                print(f"\nCalled tool: {tool_name}")
                tool_results.append({
                    "tool_use_id":f"tool_{tool_name}_{len(tool_results)}",
                    "content" : tool_response.content,
                    "type" : "tool_result"
                })

            tool_result_str = "Tool results:\n"
            for result in tool_results:
                tool_result_str += f"Result from {result["tool_use_id"]}:\n{result["content"]}\n\n"

            print("\n[LLM response]:")
            async for chunk in await self.ollamaClient.chat(
                model=self.model,
                messages=[
                    {"role":"system", "content": self.system_prompt},
                    {"role":"user", "content": question},
                    {"role": "assistant", "content": response["message"]["content"]},
                    {"role":"user", "content": tool_result_str}
                ],
                stream=True
            ):
                print(f"{chunk["message"]["content"]}", end="") 

            print("\n\n")               


        except Exception as e:
            import traceback
            print(f"Error while querying: {e}")
            traceback.print_exc()
            return str(e)
