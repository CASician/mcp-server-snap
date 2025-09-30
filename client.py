import os
import json
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def call_mcp_tool(name: str, arguments: dict) -> str:
	server_path = Path(__file__).with_name("server.py")
	params = StdioServerParameters(
		command=sys.executable,
		args=[str(server_path)],
	)
	async with stdio_client(params) as (read_stream, write_stream):
		session = ClientSession(read_stream, write_stream)
		await session.initialize()
		result = await session.call_tool(name, arguments)
		if result.content and hasattr(result.content[0], "text"):
			return result.content[0].text
		return result.model_dump_json(indent=2)


async def main():
	load_dotenv()
	api_key = os.getenv("GROQ_KEY")
	if not api_key:
		raise ValueError("Missing GROQ_KEY in .env")

	client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
	model = "llama-3.1-8b-instant"

	messages = [
		{"role": "system", "content": "Usa i tools MCP se serve"},
		{"role": "user", "content": "Dammi le linee bus per agenzia TPL di Firenze"},
	]

	resp = client.chat.completions.create(
		model=model,
		messages=messages,
		tools=[
			{
				"type": "function",
				"function": {
					"name": "get_tpl_data",
					"description": "Retrieve list of public transport lines",
					"parameters": {
						"type": "object",
						"properties": {"agency": {"type": "string"}},
						"required": ["agency"],
					},
				},
			}
		],
	)

	choice = resp.choices[0].message
	if choice.tool_calls:
		for call in choice.tool_calls:
			args = json.loads(call.function.arguments)
			tool_output = await call_mcp_tool(call.function.name, args)
			messages.append(choice)
			messages.append({
				"role": "tool",
				"tool_call_id": call.id,
				"content": tool_output,
			})
			final = client.chat.completions.create(model=model, messages=messages)
			print(final.choices[0].message.content)
			return

	# No tool call: just print the model's reply
	print(choice["content"])


if __name__ == "__main__":
    asyncio.run(main())
