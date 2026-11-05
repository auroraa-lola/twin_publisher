from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import TOOLS, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr

load_dotenv(override=True)

client = OpenAI()
MODEL = "gpt-5.4-mini"

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}]

    while True:
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
        choice = response.choices[0]
        if choice.finish_reason == "tool_calls":
            messages.append(choice.message)
            messages.extend(handle_tool_calls(choice.message.tool_calls))
        else:
            return choice.message.content


if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="AI Assistant",
        description="Ask me about Autobiography Publishing",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())
