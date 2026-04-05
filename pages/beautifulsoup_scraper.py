import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.subheader("🍵 Static Scraping with BeautifulSoup")
st.markdown("Scrapes live eBay search results by parsing raw HTML — no API key needed.")

search_q = st.text_input("Enter what to search on eBay:", placeholder="e.g. watches for men")

if search_q:
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_q.replace(' ', '+')}&_sop=12"

    with st.spinner("Scraping eBay…"):
        try:
            r = requests.get(url, verify=False)
            soup = BeautifulSoup(r.content, "html5lib")
            items = soup.find_all("div", class_="s-item__wrapper clearfix")

            scraped_data = []
            bu_prices = []

            for item in items:
                info = item.find("div", class_="s-item__info clearfix")
                if not info:
                    continue

                title_el   = info.find("div", class_="s-item__title")
                price_el   = info.find("div", class_="s-item__detail s-item__detail--primary")
                reviews_el = info.find("div", class_="s-item__reviews")

                title  = title_el.text.strip() if title_el else "No title"
                price  = price_el.text.strip() if price_el else None
                reviews = "0"
                if reviews_el:
                    reviews_span = reviews_el.find("span", class_="clipped")
                    if reviews_span:
                        reviews = reviews_span.text.strip()

                bu_prices.append(price)
                scraped_data.append({
                    "title":    title,
                    "price":    price,
                    "reviews":  reviews,
                    "category": search_q.strip(),
                })

            if scraped_data:
                df = pd.DataFrame(scraped_data)
                st.success(f"Found {len(df)} listings for **{search_q}**")
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="beautifulsoup_data.csv",
                    mime="text/csv",
                    icon=":material/download:",
                )

                st.session_state.bu_prices    = bu_prices
                st.session_state.scraped_data = scraped_data

                st.markdown("---")
                st.markdown("#### ✅ Done! Continue to Step 2:")
                st.page_link("pages/serpapi_scraper.py", label="Next → SerpAPI Scraper", icon="🔑")

            else:
                st.warning("No listings found. Try a different search term.")

        except Exception as e:
            st.error(f"An error occurred while scraping: {e}")

st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")