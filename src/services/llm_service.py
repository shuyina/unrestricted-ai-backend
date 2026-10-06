class LLMService:
    async def chat(self, payload):
        return {
            "model": payload.model,
            "response": "This is a starter LLM response. Connect to a real provider or local model to enable actual generation.",
            "usage": {"input_tokens": 0, "output_tokens": 0},
        }

    async def complete(self, prompt: str, max_tokens: int = 256):
        return {
            "prompt": prompt,
            "completion": "This is a starter completion. Connect to a real LLM provider.",
            "max_tokens": max_tokens,
        }
