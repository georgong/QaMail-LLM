from pathlib import Path
import sys
import logging
import json
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
print(f"Project Root: {project_root}")
with open("user.json", "r", encoding="utf-8") as file:
    user_dict = json.load(file)

from email_client import reader
logging.basicConfig(filename='email.log', level=logging.DEBUG)
r = reader.email_reader(logging)
print(type(r.logger))
r.delete_user("gzh")