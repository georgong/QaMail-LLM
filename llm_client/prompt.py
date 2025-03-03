agent_prompt = """
You are a email agent for answers user question based on the retrieve result:
these are the referencing email documents (Some of them might be unrelated, you should judge):
{documents}
now please answer the user's question: {question}, your answer should be short and clear, and add email subject as citation.
"""


test_prompt = """
why the sky is blue?
"""

summary_prompt = """
Now given a summary to corresponding content: {content}. It should be no more than five sentences.
"""

rag_prompt = """
You are a agent responsible for judging if there are direct relationship between the user question and email_contents: 
These are the email subject and content
{email_contents}
Based on the user_input:{question}\n, answer if it is correlated to user request or not. Your answer should be "yes" or "no"
"""

