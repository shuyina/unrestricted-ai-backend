import logging
import os
from typing import Optional
import anthropic
import openai

logger = logging.getLogger(__name__)


class LLMProvider:
    def __init__(self, provider: str = "local", model: str = "llama3"):
        self.provider = provider
        self.model = model
        self._setup_provider()

    def _setup_provider(self):
        if self.provider == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")
            logger.info("OpenAI provider initialized")
        elif self.provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            logger.info("Anthropic provider initialized")
        elif self.provider == "local":
            logger.info(f"Local LLM provider initialized: {self.model}")

    async def chat(
        self,
        messages: list[dict],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
    ) -> str:
        try:
            if self.provider == "openai":
                return await self._openai_chat(messages, max_tokens, temperature, system_prompt)
            elif self.provider == "anthropic":
                return await self._anthropic_chat(messages, max_tokens, temperature, system_prompt)
            else:
                return await self._local_chat(messages, max_tokens, temperature, system_prompt)
        except Exception as e:
            logger.error(f"LLM chat failed: {e}")
            raise

    async def _openai_chat(
        self,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str],
    ) -> str:
        try:
            all_messages = []
            if system_prompt:
                all_messages.append({"role": "system", "content": system_prompt})
            all_messages.extend(messages)

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=all_messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI chat failed: {e}")
            raise

    async def _anthropic_chat(
        self,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str],
    ) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt or "",
                messages=messages,
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic chat failed: {e}")
            raise

    async def _local_chat(
        self,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str],
    ) -> str:
        try:
            # Placeholder for local LLM
            logger.info(f"Local LLM chat with {self.model}")
            return "This is a placeholder response from local LLM. Connect to actual Llama/Mistral endpoint."
        except Exception as e:
            logger.error(f"Local LLM chat failed: {e}")
            raise

    async def complete(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        try:
            messages = [{"role": "user", "content": prompt}]
            return await self.chat(messages, max_tokens, temperature)
        except Exception as e:
            logger.error(f"LLM completion failed: {e}")
            raise
