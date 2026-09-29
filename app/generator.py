import ollama


MODEL_NAME = "qwen3:8b"


def generate_copy(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9
) -> str:

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": temperature,
            "top_p": top_p
        }
    )

    return response["message"]["content"]