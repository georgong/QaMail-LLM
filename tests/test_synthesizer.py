from pathlib import Path
import sys
import logging
import pprint
import json
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
print(f"Project Root: {project_root}")
from synthesizer import ResponseSunthesizer
with open("user.json", "r", encoding="utf-8") as file:
    user_dict = json.load(file)
rs = ResponseSunthesizer(user_config=user_dict)
setting = {"temperature":0.7,"startdate":"","enddate":"","keywordFilter":"","selfRAG":False}
generator,id =rs.forward("Information about Enrollment",setting=setting)
for i in generator:
    print(i,end = "")
print("\n\n")
print(rs.get_metadata(id))