# 🚀 QaMail-LLM
---
![Demo](assets/demo.gif)
QaMail-LLM is a local python program retrieves emails via POP3, understands their context with RAG techniques, and generates smart, accurate replies—making your email conversations faster and more efficient.
## 🌟 Features  

- **Multi-LLM Support**: Compatible with Ollama, OpenAI, and other OpenAI API-compatible LLMs.  
- **Advanced Email Processing**: Integrates time and keyword filtering, self-RAG, and hybrid search for accurate responses. 
- **Rich Email Display**: Parses and renders HTML email content for a seamless viewing experience.  

- **Bilingual Embedding Model**: Utilizes an embedding model that supports both Chinese and English for better multilingual processing.

---

## 📚 Table of Contents

- [🧰 Prerequisites](#-prerequisites)
- [🔧 Installation](#-installation)
- [⚡ Quick Start](#-quick-start)
- [🔮 Future Work](#-future-work)
- [📜 Declaration](#-declaration)

---

## 🧰 Prerequisites

Before you begin, ensure you have met the following requirements:

- **Software/Version**: python 3.8+ (we use python 3.9.21)

- **Dependencies**: pip, Anaconda

To run this project, you need to install the following dependencies. We recommend using either `pip` (Python's default package manager) or `Anaconda` (a popular Python distribution).

- **Hardware Requirements**:

if you use local LLM, usually at least **3GB of free VRAM** are necessary to generates a fluent and accurate response.
if you use external LLM, it doesn't matter.

- **Accounts**: ollama or other LLM with api_keys, your email_account with POP3 server support
   - [Downloading Ollama](https://ollama.com/download)
   - [Gmail POP3 instruction](https://support.google.com/mail/answer/7104828)
      - Common Question for Gmail POP3 Setting:https://support.google.com/accounts/thread/174976836/pop3-gmail-settings-not-working


---

## 🔧 Installation

To install and set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/georgong/QaMail-LLM.git
   ```

2. Install the required package:
   ```bash
   cd QaMail-LLM
   pip install -r requirements.txt
   ```

## ⚡ Quick Start

### 📥 Pull the Model from Ollama (Optional)
If you are using **Ollama** as your LLM provider, you need to pull the model before running it.

```sh
ollama pull qwen2.5:3b
```
- You can replace `qwen2.5:3b` with **any other model** of your choice.
- **Larger models** 🏋️‍♂️ perform better on complex tasks.
- **Smaller models** 🏃‍♂️ require less RAM and run more efficiently.


### 🛠️ Create `user.json` in the folder

Create a `user.json` file and fill in your email configuration:

> This is the default configuration used by the demo. Update the values as needed.

```json
{
  "email": "put your email here",
  "password": "put your password here",
  "server": "put your server here",
  "user_id": "create your user_id for login",
  "initial_load_num": 100,
  "llm_url": "http://localhost:11434",
  "llm_provider": "ollama",
  "model": "qwen2.5:3b",
  "enable_summary": false,
  "n_results": 10,
  "port": 5001,
  "api_key":"put your api key here"
}
```

### 🔹 Notes:
- Replace `"put your email"`, `"put your password"`, and `"put your server"` with actual values.
- `"enable_summary"` is not used yet, it will coming soon with hybrid search together. 
- Ensure `llm_url` points to your running LLM service.
---

### 🚀 Run the Server  

After setting up the configuration, start the server with:  

```bash
python server.py
```

The server should now be running and processing emails with the configured LLM. 🎯

> 🚨 **Note:** The first time you run the program, it may take a long time to initialize, as it needs to **parse and embed a large number of emails**.  
> ⏱ **The exact time depends on** `initial_load_num` — a larger value means longer processing time.  

- If you want **faster startup**, consider reducing `initial_load_num`.  
- Subsequent runs will be **faster**, as previously processed emails are already embedded.  


---

### 🌍 View Results  

Once the server is running, open your browser and visit:  

```plaintext
http://127.0.0.1:PORT
```

Replace `PORT` with the actual port number used by your server (e.g., `8000`, `5000`, etc.). You can also find the address in the output of console. 

🎯 **Now, your AI email assistant is ready to process emails and generate responses!** 🚀


## 🔮 Future Work  

- **Daily Email Summary**: Generate a concise summary of the day's emails for quick review.  
- **Scheduled Email Fetching**: Implement a scheduler to automatically retrieve and process emails at a specified time each day.  
- **Support for IMAP**: Extend email retrieval to IMAP for broader compatibility.  
- **Improved Summarization**: Enhance email summarization with more context-aware techniques.  
- **More LLM Integrations**: Add support for additional LLM providers and local models.  
- **User Interface Improvements**: Develop a web-based dashboard for easier email management and configuration. 

## 📜 Declaration  

- **Frontend Attribution**: The frontend part of this project is modified from [simple_chat](https://github.com/codingXiang/simple_chat).  
- **Network Usage & Security Notice**:  
  - This project operates **entirely offline**, except for **POP3 server communication** and **external LLM API calls**.  
  - Users should be aware that using external LLMs may result in **data exposure** due to API requests being sent over the network.  
  - To maximize security and privacy, it is **recommended** to use **local LLMs** via [Ollama](https://ollama.com) or trusted official providers such as OpenAI or Anthropic (Claude 3).  

---

🚀 **Stay secure and enjoy the AI-powered email assistant!**  