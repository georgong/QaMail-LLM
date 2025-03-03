from email_client import retriever,reader,email_util
from llm_client import client
from uuid import uuid4
from transformers import AutoModel
from torch import bfloat16
import logging

class ResponseSunthesizer:
    def __init__(self,user_config):
        """
        store the metadata list getting by each query
        when the corresponding retrieve info is used, delete the key from the dict
        """
        self.queryid2metadata = {}
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.email_reader = reader.email_reader(logger=self.logger)
        self.email_reader.login(user_config)
        self.embedding_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-zh', trust_remote_code=True, torch_dtype= bfloat16)
        if user_config["llm_provider"] == "ollama":
            self.llm_client = client.LLMSetter(base_url=user_config["llm_url"],provider=user_config["llm_provider"])
        else:
            self.llm_client = client.LLMSetter(base_url=user_config["llm_url"],provider=user_config["llm_provider"], api_key=user_config["api_key"])

        self.email_retriever = retriever.email_retriever(user_config=user_config,logger = self.logger,user_id = self.email_reader.user_id,embedding_model= self.embedding_model)
        if user_config["enable_summary"]:
            self.email_retriever.add_llm(self.llm_client)
        content_dict = self.email_reader.get_content_dict()
        self.email_retriever.store_data(content_dict)
        self.model = user_config["model"]
        self.user_config = user_config
    
    def forward(self,user_input,setting):
        filters,document_filters = self.get_filter(setting)
        temperature = setting["temperature"]
        selfrag = setting["selfRAG"]
        self.logger.info("temperature:",temperature)
        if not selfrag:
            search_result = self.email_retriever.similarities_search(user_input,filters=filters,
                                                                 document_filters = document_filters,
                                                                 n_results= self.user_config["n_results"])
        else: 
            search_result = self.email_retriever.similarities_search(user_input,filters=filters,
                                                                 document_filters = document_filters,
                                                                 n_results= self.user_config["n_results"])
            rag_template = self.constructing_rag_template(search_result,user_input)
            if len(rag_template) != 0:
                mask_list = self.llm_client.RAG_filter_result(self.model,rag_template)
                for k in ["ids","documents","metadatas","distances"]:
                    search_result[k][0]= [content for content,mask in zip(search_result[k][0], mask_list) if mask == True]
                    pass

        queryid = f"{uuid4()}"
        self.queryid2metadata[queryid] = self.parse_search_result(search_result)
        prompt_dict = self.constructing_template_dict(search_result,user_input)
        return self.query(prompt_dict, temperature=temperature),queryid
    
    def get_filter(self, setting):
        startdate = setting["startdate"]
        enddate = setting["enddate"]
        keyword = setting["keywordFilter"]
        print(startdate,enddate,keyword)
        filter_dict = {}
        document_filter_dict = {}
        if startdate == "" and enddate == "":
            pass
        elif startdate == "":
            filter_dict["date"] = {"$lte": email_util.date2dt(enddate).timestamp()}
        elif enddate == "":
            filter_dict["date"] = {"$gte": email_util.date2dt(startdate).timestamp()}
        else:
            filter_dict["$and"] = [
    {"date": {"$gte": email_util.date2dt(startdate).timestamp()}},
    {"date": {"$lte": email_util.date2dt(enddate).timestamp()}}
]
        if keyword:
            if len(keyword.split(";"))>1:
                document_filter_dict["$or"] = [{"$contains":i} for i in keyword.split(";")]
            else:
                document_filter_dict["$contains"] = keyword.split(";")[0]
        print(filter_dict)
        print(document_filter_dict)
        return filter_dict,document_filter_dict
    
    
    def get_filter_test(self,setting):
        startdate = setting["startdate"]
        enddate = setting["enddate"]
        keyword = setting["keywordFilter"]
        filter_dict = {}
        # Process date filters
        date_filters = []
        if startdate:
            date_filters.append({"date": {"$gte": email_util.date2dt(startdate).timestamp()}})
        if enddate:
            date_filters.append({"date": {"$lte": email_util.date2dt(enddate).timestamp()}})

        # Process keyword filters
        keyword_filters = [{"$contains": i} for i in keyword.split(";")] if keyword else []

        # Construct the final filter dictionary
        if date_filters and keyword_filters:
            filter_dict["$and"] = date_filters + [{"$or": keyword_filters}]
        elif date_filters:
            filter_dict["$and"] = date_filters if len(date_filters) > 1 else date_filters[0]
        elif keyword_filters:
            if len(keyword_filters) > 1:
                filter_dict["$or"] = keyword_filters
            else:
                filter_dict.update(keyword_filters[0]) 
        print(filter_dict)
        return filter_dict

    def parse_search_result(self,search_result):
        result_dict = search_result
        return result_dict
    
    def query(self,template_dict,temperature):
        return self.llm_client.generate_text_by_template(model = self.model,template_dict = template_dict,temperature = temperature)
    
    def get_metadata(self,query_id):
        return self.queryid2metadata.pop(query_id, None)
    
    def constructing_template_dict(self,search_result,question):
        documents = search_result["documents"][0]
        metadatas = search_result["metadatas"][0]
        print(metadatas)
        document_str = ""
        for doc,metadata in zip(documents,metadatas):
            document_str += "Date:" + email_util.timestamp2str(metadata["date"]) +"\n"+ " Subject:" + metadata["subject"] +"\n"+  " Content:" + doc + "\n"
        if len(documents) == 0:
            document_str += "<<told user that there is no satisfied email retrieve>>"
        return {"documents":document_str,"question":question}
    
    def constructing_rag_template(self,search_result,question):
        documents = search_result["documents"][0]
        metadatas = search_result["metadatas"][0]
        print(metadatas)
        document_list = []
        for doc,metadata in zip(documents,metadatas):
            document_list.append({"email_contents":"Date:" + email_util.timestamp2str(metadata["date"]) +"\n"+ " Subject:" + metadata["subject"] +"\n"+  " Content:" + doc + "\n",
                                  "question":question
                                  })
        return document_list

    
    