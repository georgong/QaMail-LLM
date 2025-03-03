from pathlib import Path
import sys
import logging
import json
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
print(f"Project Root: {project_root}")
with open("user.json", "r", encoding="utf-8") as file:
    user_dict = json.load(file)
from llm_client import client
llm = client.LLMSetter(base_url="http://localhost:11434",provider = "ollama")
for i in llm.generate_text(model = "qwen2.5:3b",prompt = "Hello!",temperature=0):
    print(i, end = "")

print("\n","="*20)

llm = client.LLMSetter(base_url="http://localhost:11434",provider = "ollama")
print(llm.generate_text(model = "qwen2.5:3b",prompt = "Hello!",temperature=0,stream = False))

