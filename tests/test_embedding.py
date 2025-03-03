import torch
from transformers import AutoModel
from numpy.linalg import norm
cos_sim = lambda a,b: (a @ b.T) / (norm(a)*norm(b))
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-zh', trust_remote_code=True, torch_dtype=torch.bfloat16)
embeddings = model.encode(['the weather looks not very well', '今天天气怎么样?'])
embeddings2 = model.encode(['爱彼迎预订通知', '今天天气怎么样?'])
print(cos_sim(embeddings[0], embeddings[1]))
print(cos_sim(embeddings2[0], embeddings2[1]))
print(embeddings[0].tolist())