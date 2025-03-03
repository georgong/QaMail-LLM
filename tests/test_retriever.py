
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
from email_client import reader,retriever
from pathlib import Path
import logging
import pprint
import torch
import json
from transformers import AutoModel
from numpy.linalg import norm
cos_sim = lambda a,b: (a @ b.T) / (norm(a)*norm(b))

with open("user.json", "r", encoding="utf-8") as file:
    user_dict = json.load(file)

user_dict["initial_load_num"] = 10
logging.basicConfig(filename='email.log', level=logging.INFO)
reader = reader.email_reader(logger=logging)
reader.login(user_config=user_dict)
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-zh', trust_remote_code=True, torch_dtype=torch.bfloat16)
retrive = retriever.email_retriever(user_id="gzh",logger=logging,embedding_model=model,user_config=user_dict)
content = reader.get_content_dict()
print(content)
retrive.store_data(content)
retrieve_result = retrive.similarities_search("Standford University information",False)

