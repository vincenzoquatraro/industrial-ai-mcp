from google import genai
from app.config import settings


class GeminiClient:
    """
    Wrapper attorno a Gemini, con la STESSA interfaccia di OllamaClient
    (metodo chat(system_prompt, user_prompt) -> str). Il PlanningAgent
    non deve sapere quale dei due sta usando.
    """

    def __init__(self, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = model

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=user_prompt,
            config={"system_instruction": system_prompt}
        )
        return response.text or ""