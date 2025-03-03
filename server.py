from flask import Flask,request,Response
from flask import render_template
import webbrowser
import os
from synthesizer import ResponseSunthesizer
import json

def make_unique(a):
    unique_dict = {}  # Stores unique dicts based on non-first key-values

    for d in a:
        first_key, first_value = next(iter(d.items()))  # Get the first key-value pair
        remaining_items = frozenset(list(d.items())[1:])  # Remaining key-value pairs (as set for uniqueness)

        if remaining_items in unique_dict:
            # Update max value for the first key
            unique_dict[remaining_items][first_key] = max(unique_dict[remaining_items][first_key], first_value)
        else:
            # Store the dictionary with its first key-value pair
            unique_dict[remaining_items] = {first_key: first_value, **dict(remaining_items)}

    # Convert back to list
    unique_a = list(unique_dict.values())
    return unique_a



with open("user.json", "r", encoding="utf-8") as file:
    user_config = json.load(file)
email_id = None
user_id = user_config["user_id"]
rs = None  # Global variable, but not initialized yet



app = Flask(__name__,template_folder="templates")


rs = None  # Global variable to store synthesizer instance

initialized = False  # Flag to prevent multiple initializations

@app.before_request
def initialize_synthesizer():
    """Ensure ResponseSunthesizer is initialized only once"""
    global rs, initialized
    if not initialized:
        print("✅ Initializing ResponseSunthesizer for the first request...")
        rs = ResponseSunthesizer(user_config=user_config)
        initialized = True  # Mark as initialized


@app.route("/")
def index():
    return render_template('chat_example.html')

@app.route("/chat",methods = ["POST"])
def chat_response():
    global email_id
    print(request.json)
    user_info = request.json["user_info"]
    settings = request.json["setting"]
    print(user_info,type(user_info))
    stream,email_id = rs.forward(user_info,settings)
    return Response(stream, mimetype="text/event-stream")

@app.route("/retrieve",methods = ["POST"])
def retrieve_document():
    global email_id
    if email_id is None:
        return {"error": "User ID is missing. Start a chat first."}, 400
    metadata_result = rs.get_metadata(email_id)
    metadata_list = []
    for distance,metadata in zip(metadata_result["distances"][0],metadata_result["metadatas"][0]):
        metadata_list.append([round(distance,2),metadata["file_path"],metadata["date"],metadata["subject"]])
    metadata_list = [{"score":i[0],"file_path":i[1],"date":i[2],"subject":i[3]} for i in metadata_list]
    metadata_list = make_unique(metadata_list)
    for i in metadata_list:
        file_path = i["file_path"]
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                i["html_content"] = html_content
        else:
            i["html_content"] = ""
    return {"result":metadata_list}
            
        

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5001")
    app.run(host = "0.0.0.0",port = 5001)