from email.parser import Parser
import poplib
from email import policy
from email.parser import BytesParser
from email.header import decode_header
import json
import os
import re
from bs4 import BeautifulSoup
import email
from email.parser import Parser
import poplib
from email import policy
from email.parser import BytesParser
from email.header import decode_header
import json
import os
import re
import shutil
import logging
from bs4 import BeautifulSoup
from email_client.email_parser import extract_plain_text
from email_client.html_template import email_template
from tqdm import tqdm

class email_reader():
    def __init__(self,logger):
        self.login_state = False
        self.logger = logger

    def login(self, user_config:dict):
        self.logger.info("start to login...")
        #set the mail,password from config_dict
        from_mail = user_config["email"]
        from_password = user_config["password"]
        pop_server = user_config["server"]
        user_id = user_config["user_id"]
        initial_load_num = user_config["initial_load_num"]
        server = poplib.POP3(pop_server)
        server.set_debuglevel(1)
        server.user(from_mail)
        server.pass_(from_password)
        self.user_id = user_id
        self.server = server
        self.email_dict = None
        self.content_dict = {}
        self.load_email(user_id,initial_load_num)
        self.login_state = True
        self.logger.info("success login!")

    def reset_config(self,user_config:dict):
        self.logger.info("reset the user config...")
        from_mail = user_config["email"]
        from_password = user_config["password"]
        pop_server = user_config["server"]
        user_id = user_config["user_id"]
        server = poplib.POP3(pop_server)
        server.set_debuglevel(1)
        server.user(from_mail)
        server.pass_(from_password)
        self.server = server
        self.email_dict = None
        self.content_dict = {}
        self.load_email(user_id)
        self.login_state = True
        self.logger.info("successful reset!")

    def create_folder(self,user_id):
        self.logger.debug("check folder status")
        if not os.path.exists(f"local_db/{user_id}"):
            os.makedirs(f"local_db/{user_id}")
            self.logger.debug(f"created folder local_db/{user_id}")
        else:
            pass
        if not os.path.exists(f"local_db/{user_id}/vectordb"):
            os.makedirs(f"local_db/{user_id}/vectordb")
            self.logger.debug(f"created folder local_db/{user_id}/vectordb")
        else:
            pass
        if not os.path.exists(f"local_db/{user_id}/htmldb"):
            os.makedirs(f"local_db/{user_id}/htmldb")
            self.logger.debug(f"created folder local_db/{user_id}/htmldb")
        else:
            pass
        if not os.path.exists(f"local_db/{user_id}/otherdb"):
            os.makedirs(f"local_db/{user_id}/otherdb")
            self.logger.debug(f"created folder local_db/{user_id}/otherdb")
        else:
            pass
        self.vectordb_path = f"local_db/{user_id}/vectordb"
        self.htmldb_path = f"local_db/{user_id}/htmldb"
        self.otherdb_path = f"local_db/{user_id}/otherdb"



    def load_email(self,user_id,max_num = -1):
        self.create_folder(user_id)
        if os.path.exists(f"{self.otherdb_path}/email_id.json"):
            #load the exist email_dict
            mail_num = self.get_stat()["mail_num"]
            email_dict = self.load_dict_from_json(user_id)
        else:
            #create the empty email_dict 
            email_dict = {}
            mail_num = self.get_stat()["mail_num"]

        #load the email_id and text
        count = 0;
        for i in tqdm(range(mail_num,0,-1)):
            if count > max_num and max_num != -1:
                self.logger.info("Exceed Maximum Number")
                break
            else:
                count +=1
            mail_dict = self.get_text(i)
            if mail_dict["text"] == "Error information":
                continue;
            message_id,text,date,From,subject = mail_dict["id"],mail_dict["text"],mail_dict["date"],mail_dict["from"],mail_dict["subject"]
            if message_id not in email_dict:
                email_dict[message_id] = re.sub(r'[^a-zA-Z0-9]', '', message_id)
                with open(f"{self.htmldb_path}/{email_dict[message_id]}.html","w",encoding='utf-8') as f:
                    f.write(self.get_html(i)) #save the html content into folder
                self.content_dict[message_id] = {"text":text,"date":date,"from":From,"subject":subject}
            else:
                self.logger.info("READ ALL OF THE EMAIL, EXIT")
                #already load all of the new email
                break;
        self.save_dict_to_json(email_dict, user_id)
    
    def delete_user(self,user_id):
        folder_path = f"local_db/{user_id}"
        # check if the path exist
        if os.path.exists(folder_path):
            # delete the path
            shutil.rmtree(folder_path)
            self.logger.debug(f"folder: {folder_path} has been delete")
        else:
            self.logger.debug(f"folder: {folder_path} do not exist")



# get the statistical information of email
    def get_stat(self):
        num, totalsize = self.server.stat()
        return{"mail_num":num,"total_size":totalsize}

# get the emaillist
    def get_resp(self):
        resp, mailist, r = self.server.list()
        return{"respond":resp,"mail_list":mailist}
    
    def get_text(self,index):
        resp, lines, octets = self.server.retr(index)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        subject = msg["Subject"]
        self.logger.debug(subject)
        decoded_subject, charset = decode_header(subject)[0]
        if isinstance(decoded_subject, bytes):
            decoded_subject = decoded_subject.decode(charset or 'utf-8')
        #self.logger.debug(msg['Date'] + "\n\n" msg["From"] "\n\n",decoded_subject,"\n\n",msg['Message-ID'],"\n")
        return {"date":msg["Date"],"from":msg["From"],"subject":decoded_subject,"id":msg["Message-ID"],"text":extract_plain_text(msg)}
    
    
    def get_html(self,index):
        resp, lines, octets = self.server.retr(index)
        msg_content = b'\r\n'.join(lines)
        email_data = msg_content
        self.logger.debug("parser the email")
        msg = BytesParser(policy=policy.default).parsebytes(email_data)
        # 提取 HTML 部分
        subject = msg["Subject"]
        self.logger.debug("get the html content")
        html_content = None
        for part in msg.walk():
            print(part.get_content_charset(),part.get_content_type())
            if part.get_content_type() == 'text/html':
                charset = part.get_content_charset() or 'utf-8'
                html_content = part.get_payload(decode=True).decode(charset) #part.get_content()
            if part.get_content_type() == 'text/plain':
                charset = part.get_content_charset() or 'utf-8'
                text_content = part.get_payload(decode=True).decode(charset)
                html_template = email_template
                html_content = html_template.format(subject=subject, text_content=text_content.replace('\n', '<br>'))
                
        return html_content
    
    
    def save_dict_to_json(self,data_dict,user_id):
        """
        save dictionary into user file
        """
        file_path = f'{self.otherdb_path}/email_id.json'
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, ensure_ascii=False, indent=4)
        self.logger.info(f"数据已成功写入到 {file_path}")



    def load_dict_from_json(self,user_id):
        """
        load dictionary from user_file
        """
        file_path = f'{self.otherdb_path}/email_id.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        return data_dict
    
    def get_content_dict(self):
        if self.login_state:
            return self.content_dict
        else:
            self.logger.error("return conten_dict before connect to email client!")
            raise Exception("Haven't Connect to Email Client")
    

        
    

