from llm_client.provider import *
from llm_client.prompt import *
"""
generated by GPT4o:
build a llm_setter() class which provide common interface from all of the llm url (remote or local)
"""
class LLMSetter:
    """
    Factory class to select the appropriate LLM provider.
    """

    def __init__(self, base_url, provider="generic", api_key=None):
        self.provider = provider.lower()

        if self.provider == "openai":
            self.client = OpenAIProvider(base_url, api_key)
        elif self.provider == "ollama":
            self.client = OllamaProvider(base_url)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def get_model_list(self):
        return self.client.get_model_list()

    def generate_text(self, model, prompt, stream=True, temperature = 0.7):
        if stream:
            return self.client.generate_text(model, prompt, stream, temperature)
        else:
            return "".join(self.client.generate_text(model, prompt, stream, temperature))
    
    def test_generate_text_by_template(self,model,prompt_dict,stream = True):
        prompt = test_prompt
        for k,v in prompt_dict.items():
            prompt = prompt.replace("{" + f"{k}" + "}",v)

        return self.generate_text(model, prompt, stream = stream)
    def generate_text_by_template(self,model,template_dict,stream = True,temperature = 0.7):
        prompt = agent_prompt
        for k,v in template_dict.items():
            prompt = prompt.replace("{" + f"{k}" + "}",v)
        print(prompt)

        return self.generate_text(model, prompt, stream = stream, temperature = temperature)
    
    def RAG_filter_result(self,model,template_dict_list,stream = False):
        prompt = rag_prompt
        mask  = [None for i in range(len(template_dict_list))]
        for idx,template_dict in enumerate(template_dict_list):
            for k,v in template_dict.items():
                prompt = prompt.replace("{" + f"{k}" + "}",v)
            print(prompt)
            result = self.generate_text(model, prompt, stream = stream, temperature = 0)
            print(result)
            if "yes" in result:
                mask[idx] = True
            else:
                mask[idx] = False
        return mask


    