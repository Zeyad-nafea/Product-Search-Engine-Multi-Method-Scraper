import streamlit as st

st.title("🗂️ DSAI 103 – eBay Product Scraper")
st.markdown("A multi-method data collection and visualization project built with Python & Streamlit.")

st.markdown("---")

st.markdown("## 🔢 Recommended Flow")
st.markdown("Follow the steps below in order — each step feeds data into the next.")

st.markdown("---")

st.markdown("### Step 1 · 🍵 Static Scraping with BeautifulSoup")
st.markdown(
    "Scrape eBay listings directly from HTML using the **BeautifulSoup** and **Requests** libraries. "
    "Enter a search query and extract product titles, prices, and review counts from the raw page source."
)
st.page_link("pages/beautifulsoup_scraper.py", label="Open BeautifulSoup Scraper", icon="🍵")

st.markdown("---")

st.markdown("### Step 2 · 🔑 API Scraping with SerpAPI")
st.markdown(
    "Fetch structured eBay product data through the **SerpAPI** service, which returns clean JSON results. "
    "Faster and more reliable than HTML parsing. "
    "Data collected here powers all three visualizations in Step 3."
)
st.page_link("pages/serpapi_scraper.py", label="Open SerpAPI Scraper", icon="🔑")

st.markdown("---")

st.markdown("### Step 3 · 📊 Data Visualizations")
st.markdown(
    "Explore the collected data through three interactive visualizations. "
    "Complete Steps 1 and 2 before visiting these pages."
)
st.page_link("pages/network_graph.py", label="Network Graph — Product Relationships", icon="🌐")
st.page_link("pages/price_heatmap.py", label="Price Heatmap — BeautifulSoup vs SerpAPI", icon="🔥")
st.page_link("pages/scatter_3d.py", label="3D Scatter Plot — Price × Reviews × Rating", icon="🧊")

st.markdown("---")

st.markdown("### 🤖 Selenium Scraper (Local Only)")
st.markdown(
    "**Selenium** automates a real Chrome browser to scrape JavaScript-rendered pages. "
    "This cannot run on Streamlit Cloud due to browser security restrictions — "
    "download the standalone script and run it on your own machine."
)
st.page_link("pages/selenium_scraper.py", label="Selenium Scraper — Download & Instructions", icon="🤖")

st.markdown("---")

st.markdown("### 🎬 Project Wrap-Up")
st.markdown("Final acknowledgments, team members, and project reflections.")
st.page_link("pages/project_wrap_up.py", label="The End", icon="🎬")