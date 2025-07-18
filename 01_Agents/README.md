# 🤖 Weather Assistant — Agentic AI with OpenAI Agents SDK

This project demonstrates a basic **agentic AI system** using the [OpenAI Agents SDK](https://github.com/openai/openai-agents). It features:

- Context-aware dynamic agent instructions
- Tool usage via `function_tool`
- Agent handoffs
- Gemini model integration via `AsyncOpenAI`

> 💡 Ideal for beginners learning how to build contextual, multi-agent workflows.

---

## 🛠️ Features Used

| Feature                              | Description                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------|
| ✅ `function_tool`                  | Enables wrapping Python functions for tool use inside agents.              |
| ✅ `RunContextWrapper`              | Injects user-defined context (`is_premium`) into the agent.                |
| ✅ Dynamic Instructions             | The `instructions` are generated at runtime based on user context.         |
| ✅ Agent Handoff                    | Non-premium users can be handed off to a Refund Agent.                     |
| ✅ Custom LLM Client                | Uses `AsyncOpenAI` with Gemini model and custom base URL.                  |
| ✅ Tool Behavior Control            | Configured with `tool_choice=\"required\"` and `stop_on_first_tool`.       |
| ✅ OpenAI Tracing                   | Integrated tracing via `set_tracing_export_api_key()`.                     |
| ✅ Async Execution                  | Built entirely using async/await for scalability and speed.                |
| ✅ Environment Configuration        | API keys and URLs are loaded from `.env` using `python-dotenv`.            |
| ✅ Pydantic for Context Schema      | Strongly typed context using Pydantic model (`user_details`).              |

---

## 🧪 Requirements

- Python 3.10+
- Packages:
  - `openai-agents-sdk`
  - `pydantic`
  - `python-dotenv`

Install via:

```bash
pip install openai-agents-sdk pydantic python-dotenv
