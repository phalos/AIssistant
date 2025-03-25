import requests

def chat_with_agent():
    url = "http://localhost:8000/respond"  # Ensure this matches your backend URL
    headers = {"Content-Type": "application/json"}

    print("Start chatting with the agent (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        data = {
            "messages": [{"role": "user", "content": user_input}],
            "screen_context": None,
            "audio_context": None
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            result = response.json()
            if result["success"]:
                print("Agent:", result["response"])
            else:
                print("Error:", result.get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

if __name__ == "__main__":
    chat_with_agent() 