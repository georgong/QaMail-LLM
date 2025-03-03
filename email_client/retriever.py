
from email_client.email_util import str2datetime
from email_client.splitter import recursive_email_splitter
import logging
import chromadb
import uuid
import json
import re
import os

class email_retriever:
    def __init__(self,user_id,embedding_model,user_config,logger):
        self.user_id = user_id
        self.presist_directory = f'local_db/{user_id}/vectordb'
        self.file_path = f"local_db/{self.user_id}"
        self.embedding_model = embedding_model
        self.chroma_client = chromadb.PersistentClient(path=self.presist_directory)
        self.collection = self.chroma_client.get_or_create_collection(name="email_collection")
        if user_config["enable_summary"]:
            #TODO add another summary collection (summary each email and store as summary_collection(need llm))
            self.summary_collection = self.chroma_client.get_or_create_collection(name="summary_collection")
            pass
        self.logger = logger

    def store_data(self,content_dicts):
        documents_list = []
        metadatas_list = []
        embedding_list = []
        ids_list = []
        id2text = {}
        id2content = {}
        if len(content_dicts) == 0:
            self.logger.info("No new email")
            return True;
        for content_tuple in content_dicts.items():
            text,from_account,subject,date,message_id = self.parse_content_dict(content_tuple)
            id2text[message_id] = text
            content_list = recursive_email_splitter(text)
            id2content[message_id] = content_list
            basic_path = f"local_db/{self.user_id}/htmldb" 

            temperate_documents_list = []
            temperate_embedding_list = []
            temperate_metadatas_list = []
            temperate_ids_list = []
            for content in content_list:
                temperate_documents_list.append(content)
                temperate_embedding_list.append(self.embedding_model.encode(content).tolist())
                temperate_metadatas_list.append({"date":date,"from":from_account,"subject":subject,"message_id":message_id,"file_path":basic_path + f"/{re.sub(r'[^a-zA-Z0-9]', '', message_id)}.html"})
                temperate_ids_list.append(f"{uuid.uuid4()}")
            documents_list.extend(temperate_documents_list)
            metadatas_list.extend(temperate_metadatas_list)
            embedding_list.extend(temperate_embedding_list)
            ids_list.extend(temperate_ids_list)
        self.collection.add(
        documents= documents_list,
        metadatas= metadatas_list,
        embeddings=embedding_list,
        ids = ids_list
        )
        self.logger.info("store collections into local database")
        self.store_id2text(id2text)
        self.store_id2content(id2content)
        return True
        
    def key_word_search():
        #TODO

        raise NotImplementedError()


    def similarities_search(self,query,filters,document_filters,n_results = 10):
        self.logger.debug(f"similarities search with {query}")
        if filters and document_filters:
            results = self.collection.query(
            query_embeddings=self.embedding_model.encode(query).tolist(),
            n_results=n_results,
            where=filters,
            where_document=document_filters)
        elif filters:
            results = self.collection.query(
            query_embeddings=self.embedding_model.encode(query).tolist(),
            n_results=n_results,
            where=filters,)
        elif document_filters:
            results = self.collection.query(
            query_embeddings=self.embedding_model.encode(query).tolist(),
            n_results=n_results,
            where_document=document_filters)
        else:
            results = self.collection.query(
            query_embeddings=self.embedding_model.encode(query),
            n_results=n_results)
        return results

    def bm25_search():
         #TODO
        
        raise NotImplementedError()

    def parse_content_dict(self,content_tuple):
        #{"Date":msg["Date"],"From":msg["From"],"Subject":decoded_subject,"Message-ID":msg["Message-ID"],"Text":extract_plain_text(msg)}
        message_id = content_tuple[0]
        content_dict = content_tuple[1]
        text = content_dict["text"]
        from_account = content_dict["from"]
        subject = content_dict["subject"]
        date = str2datetime(content_dict["date"])
        if date:
            date = date.timestamp()
        return text,from_account,subject,date,message_id

    def store_id2text(self, id2text):
        basic_path = f"local_db/{self.user_id}/otherdb"
        file_path = f"{basic_path}/id2text.json"

        # Ensure directory exists
        os.makedirs(basic_path, exist_ok=True)

        # If file does not exist, create it with an empty JSON object
        if not os.path.exists(file_path):
            print("⚠️ File not found. Creating a new JSON file.")
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump({}, file, ensure_ascii=False, indent=4)

        # Open the file in read mode first to load existing data
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)  # Read existing JSON content
            except json.JSONDecodeError:
                print("⚠️ JSON file is corrupted or empty. Resetting...")
                data = {}

        # Update with new data
        data.update(id2text)

        # Write back the updated data
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        self.logger.info("Successful load id2text")
        return True
        
    def store_id2content(self, id2content):
        basic_path = f"local_db/{self.user_id}/otherdb"
        file_path = f"{basic_path}/id2content.json"

        # Ensure directory exists
        os.makedirs(basic_path, exist_ok=True)

        # If file does not exist, create it with an empty JSON object
        if not os.path.exists(file_path):
            print("⚠️ File not found. Creating a new JSON file.")
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump({}, file, ensure_ascii=False, indent=4)

        # Open the file in read mode first to load existing data
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)  # Read existing JSON content
            except json.JSONDecodeError:
                print("⚠️ JSON file is corrupted or empty. Resetting...")
                data = {}

        # Update with new data
        data.update(id2content)

        # Write back the updated data
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        self.logger.info("Successful load id2content")
        return True

    def hybrid_search(self):
        #TODO
        raise NotImplementedError()
    
    def hook(self):
        #TODO
        """
        This function for catching the email based on user's command.
        eg: the user said notice the email with ... content,
        llm with check each emails when reading and catch the target email.
        """
        raise NotImplementedError()
    
    def add_llm(self,llm):
        self.llm_client = llm #this llm helps to do summary, hook etc.s

    

        


        




