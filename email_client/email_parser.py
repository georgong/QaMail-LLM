import re
from bs4 import BeautifulSoup

def extract_plain_text(msg):
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                        except:
                            print(msg)
                            return "Error information"
                            continue;
                    if content_type == "text/html":
                        try:
                            return extract_text_from_html(part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8'))
                        except:
                            return "Error information"
            else:
                content_type = msg.get_content_type()
                if content_type == "text/plain":
                    try:
                        return msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')
                    except:
                        print(msg)
                        return "Error information"
                if content_type == "text/html":
                    try:
                        return extract_text_from_html(msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8'))
                    except:
                        print(msg)
                        return "Error information"
            return None


def extract_text_from_html(html_content):
    # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'lxml')
    # 提取纯文本内容
        text = soup.get_text()
        return re.sub(r'\s+', ' ', text).strip()