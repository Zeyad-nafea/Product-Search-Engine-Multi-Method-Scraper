# 🛒 eBay Scraper – Multi-Method Scraper

A Python-based product search engine that scrapes e-commerce data from eBay using multiple methods, cleans it, and visualizes insights. Perfect for exploring web scraping techniques, data integration, and interactive dashboards.

---

## 🔍 Features

### Multi-Method Data Collection
Scrape product titles, prices, and review counts via three distinct approaches:

- **Static HTML Parsing** — Requests + BeautifulSoup for fast, lightweight scraping
- **API Access** — SerpAPI for structured, reliable JSON results
- **Dynamic Rendering** — Selenium + ChromeDriver for JavaScript-heavy pages

### Data Cleaning & Integration
- Merge results from multiple sources
- Remove duplicates and normalize price formats
- Export combined results as CSV

### Interactive Visualizations
- **KDE Heatmaps** — Price distributions across scraping methods
- **Network Graphs** — Relationship mapping with NetworkX
- **3D Scatter Plots** — Multi-feature analysis (price × reviews × rating)

### Streamlit Dashboard
- Real-time search queries
- Dedicated page for each scraping method
- CSV export for each data source

---

## 💻 Live Demo

Check out the live Streamlit app here: **[eBay Scraper Dashboard](https://ebay-multi-method-scraper.streamlit.app)**
---

## 📂 Repository Structure

```
.
├── main.py                  # Streamlit dashboard entry point
├── requirements.txt         # Python dependencies
├── pages/
│   ├── bu.py                # BeautifulSoup scraper page
│   ├── api.py               # SerpAPI scraper page
│   ├── sel.py               # Selenium scraper page (local only)
│   ├── networkx.py          # Network graph visualization
│   ├── heatmap.py           # KDE & block heatmap visualization
│   ├── 3d.py                # 3D scatter plot visualization
│   └── the_end.py           # Project wrap-up page
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ebay-scraper.git
cd ebay-scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run main.py
```

---

## 🔧 Notes

### SerpAPI Key
The API page uses a SerpAPI key defined directly in `pages/api.py`. To use your own key, replace the value of `api_key` in the params dictionary with your key from [serpapi.com](https://serpapi.com).

### Selenium (Local Only)
Selenium cannot run inside Streamlit Cloud due to browser security restrictions. The Selenium page in the app provides a downloadable standalone script with full instructions for running it locally.

To run Selenium locally you will need:
- Google Chrome installed
- ChromeDriver (or use `webdriver-manager` to handle it automatically)

```bash
pip install webdriver-manager
```

---

## 📦 Requirements

See [`requirements.txt`](requirements.txt) for the full list of dependencies.

---

## 🏫 About

Developed as part of **DSAI 103 – Data Acquisition in Data Science**  
**Zewail City of Science and Technology** — CSAI Program  
Instructor: Dr. Mohamed Maher Ata

**Team Members:**
- [Zeyad Mohamed Fathy](https://www.linkedin.com/in/zeyad-nafea-314354357/)
- [Radwa Abd El Sadek Salah](https://www.linkedin.com/in/radwa-salah-84b752357)