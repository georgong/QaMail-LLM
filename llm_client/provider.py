from abc import ABC, abstractmethod
import requests
import json

# ======================== Abstract Base Class =========================
class Provider(ABC):
    """
    Abstract class to represent an LLM provider.
    All child classes must implement `get_model_list()` and `generate_text()`.
    """

    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip("/")  # Normalize URL
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    @abstractmethod
    def get_model_list(self):
        """Fetch available models from the provider."""
        pass

    @abstractmethod
    def generate_text(self, model, prompt, stream=True):
        """Generate text using the given model and prompt."""
        pass


# ======================== OpenAI Provider =========================
class OpenAIProvider(Provider):
    """Implementation for OpenAI API."""
    def get_model_list(self):
        try:
            response = requests.get(f"{self.base_url}/v1/models", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return [model["id"] for model in data["data"]]
            else:
                return f"Error fetching models: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_text(self, model, prompt, stream=True, temperature = 0.7):
        try:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": stream
            }
            response = requests.post(f"{self.base_url}/v1/chat/completions", json=payload, headers=self.headers, stream=stream)

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode("utf-8"))
                        yield data["choices"][0]["message"]["content"]
            else:
                yield f"Error generating text: {response.status_code}"
        except Exception as e:
            yield f"Error: {str(e)}"


# ======================== Ollama Provider =========================
class OllamaProvider(Provider):
    """Implementation for Ollama local API."""

    def __init__(self,base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def get_model_list(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data["models"]]
            else:
                return f"Error fetching models: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_text(self, model, prompt, stream=True, temperature = 0.7):
        try:
            payload = {"model": model, "prompt": prompt, "stream": stream, "options":{"temperature":temperature}}
            response = requests.post(f"{self.base_url}/api/generate", json=payload, headers=self.headers, stream=stream)

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode("utf-8"))
                        yield data["response"]
                        
            else:
                yield f"Error generating text: {response.status_code}"
        except Exception as e:
            yield f"Error: {str(e)}"




