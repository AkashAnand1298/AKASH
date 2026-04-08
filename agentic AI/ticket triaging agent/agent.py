import requests
import json

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": "Bearer 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",
    "Accept": "text/event-stream",
}

print("Ticket Triaging Agent (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "exit":
        print("Goodbye!")
        break
    if not user_input.strip():
        continue

    print("\nAgent: ", end="", flush=True)

    payload = {
        "model": "google/gemma-4-31b-it",
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 16384,
        "temperature": 1.00,
        "top_p": 0.95,
        "stream": True,
        "chat_template_kwargs": {"enable_thinking": True},
    }

    try:
        response = requests.post(invoke_url, headers=headers, json=payload, stream=True)
        for line in response.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue
            data_str = decoded[6:]
            if data_str.strip() == "[DONE]":
                break
            try:
                data = json.loads(data_str)
                choices = data.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        print(content, end="", flush=True)
            except json.JSONDecodeError:
                continue
        print("\n")
    except Exception as e:
        print(f"\nError: {e}\n")