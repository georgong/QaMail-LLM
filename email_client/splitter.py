import re
def recursive_email_splitter(page_content,max_length=200, overlap=50):
    def replace_links_and_separators(text):
        # 定义一个正则表达式模式来匹配常见的URL
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        # 定义一个正则表达式模式来匹配由 "-" 组成的分隔线
        separator_pattern = re.compile(
            r'-+'
        )
        seperator_list = ['\r\n\r\n',"\r\n","\n\n","\n",".","。","，",","]
        # 使用正则表达式替换所有匹配的URL为 "--link--"
        replaced_text = url_pattern.sub('**link**', text)
        # 使用正则表达式替换所有匹配的分隔线为空字符串
        replaced_text = separator_pattern.sub('', replaced_text)
        replaced_text = re.sub('\s+', " ", replaced_text)
        return replaced_text
    text = replace_links_and_separators(page_content)
    if len(text) <= max_length:
        return [text]  # Base case: No need to split

    # Split text by sentences while preserving structure
    sentences = text.split(". ")  # Adjust for other delimiters if needed
    chunks, current_chunk = [], ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 2 <= max_length:  # +2 for ". "
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Handle overlaps
    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i > 0:
            overlap_text = chunks[i - 1][-overlap:]  # Take overlap from previous chunk
            chunk = overlap_text + " " + chunk
        final_chunks.append(chunk.strip())

    return final_chunks

if __name__ == "__main__":
    string = """
    Wikipedia is a free online encyclopedia that anyone can edit, and millions already have.

Wikipedia's purpose is to benefit readers by presenting information on all branches of knowledge. Hosted by the Wikimedia Foundation, Wikipedia consists of freely editable content, with articles that usually contain numerous links guiding readers to more information.

Written collaboratively by volunteers known as Wikipedians, Wikipedia articles can be edited by anyone with Internet access, except in limited cases in which editing is restricted to prevent disruption or vandalism. Since its creation on January 15, 2001, it has grown into the world's largest reference website, attracting over a billion visitors each month. Wikipedia currently has more than sixty-four million articles in more than 300 languages, including 6,951,668 articles in English, with 126,690 active contributors in the past month."
    """
    print(recursive_email_splitter(string))



