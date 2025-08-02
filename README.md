# 🎥 Advanced Movie Recommendation from Scratch  
Scraping, Data Cleaning, Zero-Shot Classification, and Vector Search

This project builds an end‑to‑end **movie recommendation system**:  
✅ Scraping movies from Goojara →  
✅ Data cleaning & genre extraction →  
✅ Zero‑shot classification with transformers →  
✅ Semantic vector search with FAISS →  
All ready to power an intelligent content‑based recommendation engine.


## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/sismolla/Advanced-movie-recommendation-from-scrath-using-vector-search-and_zero-shot-classification.git
cd Advanced-movie-recommendation-from-scrath-using-vector-search-and_zero-shot-classification
```

Create and activate a virtual environment (recommended):

```bash

python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux / macOS
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
If requirements.txt is missing, you can manually install core libraries:
```
```bash
If requirements.txt is missing, you can manually install core libraries:
```


```bash
🧹 Step 2 – Data Cleaning
The data_cleaning.py script:
```

Loads scraped data

Handles missing fields & normalizes text

Splits multi-label genres into lists

Maps / extracts main genres
```bash
python data_cleaning.ipynb
Output: clean_movies.json or .csv – clean dataset ready for NLP.
```
🧠 Step 3 – Vector Search & Enrichment
The vector_search.py script:

Uses facebook/bart-large-mnli with 🤗 transformers zero‑shot pipeline
→ categorizes each movie as Light & Entertaining or Dark / Serious / Realistic

Generates semantic embeddings with HuggingFaceEmbeddings (all-MiniLM-L6-v2)

Builds a FAISS index for fast vector search & recommendations

```bash
python vector_search.ipynb
```
✅ Result: a semantic index ready for recommendation APIs.

⚙️ Hardware & Tips
Zero‑shot classification uses a large transformer; recommended:

8GB+ RAM and CPU (GPU better)

💡 You can run vector_search.py and embeddings for free on Google Colab if local hardware is limited.

🧩 Project Pipeline Overview
1️⃣ Scrape data →
2️⃣ Clean & preprocess →
3️⃣ Zero‑shot classification & vector search →
4️⃣ Build recommendation API →
5️⃣ Deploy in Django web app

📦 Code Explanation – scrapy/goojara.py
```bash
import scrapy

class GoojaraSpider(scrapy.Spider):
    name = "goojara"
    allowed_domains = ["ww1.goojara.to"]
    start_urls = [f"https://ww1.goojara.to/watch-movies?p={i}" for i in range(1, 200)]

    def parse(self, response):
        for link in response.css('div.mxwd div.dflex a::attr(href)').getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parse_detail)

    def parse_detail(self, response):
        container = response.css('div.marl div.date::text').getall()
        description_container = response.css('div.marl div.fimm p::text').getall()
        yield {
            'film_link': response.url,
            'title': response.css('div.marl h1::text').get(),
            'thumbnail': response.css('div.imrl img::attr(src)').get(),
            'movie_generic': container[1] if len(container) > 1 else '',
            'release_date': container[2] if len(container) > 2 else '',
            'description': description_container[0] if len(description_container) > 0 else '',
            'directors': description_container[1] if len(description_container) > 1 else '',
            'cast': description_container[2] if len(description_container) > 2 else '',
        }
```
✅ Scrapes listing pages → follows links → extracts movie metadata.
✅ Protects against missing fields.

🤝 Contributing
Feel free to open issues or submit pull requests to improve the scraper, NLP pipeline, or deployment
