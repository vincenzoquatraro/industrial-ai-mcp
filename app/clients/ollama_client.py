import ollama

class OllamaClient:
    """
    Wrapper attorno al modello locale di ollama
    """

    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt,
                 "role": "user", "content": user_prompt}
            ]
        )
        return response["message"]["content"]