# Company News Chatbot (Live Search)

An interactive **Streamlit** app that can:  
- **Search for the latest company news** from Bing News in real time  
- **Summarize articles** in multiple styles (formal, casual, bullet points) using the **Qwen/Qwen3-8B-FP8** language model  
- **Chat interactively** with a built-in chatbot that can also fetch news if requested  

---

## Features

1. **Live Company News Search**  
   - Scrapes Bing News results for the latest headlines.  
   - Filters only articles relevant to the requested company.  
   - Summarizes each article in your preferred style.

2. **Multiple Summary Styles**  
   - **Formal business summary**  
   - **Casual conversation**  
   - **Quick bullet points**  

3. **Chatbot Mode**  
   - Have a natural conversation.
   - Maintains conversation history for context. 
---

## 🛠️ Tech Stack

### **Frontend / App Framework**
- **Streamlit**
  - Handles the entire UI, input forms, and live updating components.
  - `st.cache_resource` caches the model so it doesn't reload on every run.
  - `st.chat_input` and live `placeholder.markdown` enable streaming responses.

### **Web Scraping**
- **requests** for HTTP requests.
- **BeautifulSoup** for parsing HTML.
- We scrape **Bing News Search** results with a custom query (sorted by newest first).
- Headlines and links are extracted via multiple CSS selectors for robustness.
- Full articles are fetched and the text is extracted from `<p>` tags.

### **AI Model**
- **Qwen/Qwen3-14B-FP8** from Hugging Face.
  - Large-scale **language model** optimised for inference in FP8 format.
  - Runs with `torch.bfloat16` or `torch.float16` depending on GPU support.
  - Hugging Face **transformers** pipeline for quick text generation.
  - **TextIteratorStreamer** for token-by-token streaming.

**Why Qwen/Qwen3-14B-FP8?**
- High-quality, general-purpose language capabilities.
- FP8 weights make it more memory-efficient.
- Supports multi-turn conversations and summarization tasks.

---
## 🛠 Tools & Libraries Used

| Tool/Library | Purpose |
|--------------|---------|
| **Streamlit** | Interactive web app interface |
| **BeautifulSoup4** | HTML parsing for Bing News scraping |
| **Requests** | Fetching Bing News search results & article pages |
| **HuggingFace Transformers** | Loading and running the Qwen model |
| **Qwen/Qwen3-8B-FP8** | Large language model for summarization & chatbot responses |
| **urllib.parse.quote** | Encoding search queries for URLs |

---

## 🔍 How It Works

### 1. **Searching for News**
- User enters a company name (e.g., `"Zoho"`).
- The app sends a **Bing News search request** with the query formatted as:  
  ```
  https://www.bing.com/news/search?q={company}+latest+news&qft=sortbydate='1'
  ```
- The HTML page is fetched with a `User-Agent` header to avoid basic bot blocking.

### 2. **Scraping Results**
- The HTML is parsed using **BeautifulSoup**.
- The code checks multiple **headline selectors** (`div.news-card a`, `h2 a`, etc.) to extract links and titles.
- Only articles **containing the company name** are kept.
- The top **5 unique articles** are returned.

### 3. **Fetching Full Article Text**
- The article’s link is visited.
- All `<p>` tags are extracted and joined into a single string.
- Basic error handling ensures broken links don’t crash the app.

### 4. **Summarizing with Qwen**
- The **Qwen/Qwen3-8B-FP8** model is loaded via HuggingFace’s `transformers` library.
- The prompt includes:
  - The desired **summary style**  
  - The company name  
  - The full article text  
- The model generates a concise summary (formal, casual, or bullet points).

### 5. **Chatbot Mode**
- Stores conversation history in `st.session_state.messages`.
- Reconstructs the conversation into a single prompt for Qwen.
- If the user mentions "Company name" with "news" or "latest," it automatically:
  1. Extracts the company name using Qwen.
  2. Searches Bing News.
  3. Summarizes the top articles.

---

## Installation

```bash
git clone https://github.com/LSShrivathsan/RAP_CompanyNewsChatbot_LiveSearch.git
cd RAP_CompanyNewsChatbot_LiveSearch

pip install -r requirements.txt
```

`requirements.txt` contains:
```
streamlit
beautifulsoup4
requests
transformers
torch
sentencepiece
accelerate
safetensors
urllib3
```

---

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at:
```
http://localhost:8501
```

---

## License
MIT License. Free to use and modify.
