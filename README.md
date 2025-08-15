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
---

## 🛠 Tools & Libraries Used

| Tool/Library | Purpose |
|--------------|---------|
| **[Streamlit](https://streamlit.io/)** | Interactive web app interface |
| **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** | HTML parsing for Bing News scraping |
| **[Requests](https://docs.python-requests.org/)** | Fetching Bing News search results & article pages |
| **[HuggingFace Transformers](https://huggingface.co/docs/transformers)** | Loading and running the Qwen model |
| **[Qwen/Qwen3-8B-FP8](https://huggingface.co/Qwen/Qwen3-8B-FP8)** | Large language model for summarization & chatbot responses |
| **[urllib.parse.quote](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote)** | Encoding search queries for URLs |

---

## 🔍 How It Works

### 1. **Searching for News**
- User enters a company name (e.g., `"Tesla"`).
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
