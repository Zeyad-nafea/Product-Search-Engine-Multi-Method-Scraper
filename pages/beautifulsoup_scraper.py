import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.subheader("🍵 Static Scraping with BeautifulSoup")
st.markdown("Scrapes live eBay search results by parsing raw HTML — no API key needed.")

search_q = st.text_input("Enter what to search on eBay:", placeholder="e.g. watches for men")

# ── Realistic browser headers ──────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
}

# ── Selector fallback map: try each until one yields results ───────────────────
ITEM_SELECTORS = [
    ("div",  {"class": "s-item__wrapper clearfix"}),
    ("li",   {"class": "s-item"}),
    ("div",  {"class": "s-item__pl-on-right"}),
]

TITLE_SELECTORS  = ["s-item__title"]
PRICE_SELECTORS  = ["s-item__price"]
REVIEW_SELECTORS = ["s-item__reviews-count", "s-item__reviews"]


def try_find_text(parent, tag, class_names):
    for cls in class_names:
        el = parent.find(tag, class_=cls)
        if el:
            return el.get_text(separator=" ", strip=True)
    return None


if search_q:
    url = (
        f"https://www.ebay.com/sch/i.html"
        f"?_nkw={search_q.replace(' ', '+')}&_sop=12"
    )

    with st.spinner("Scraping eBay…"):
        try:
            session = requests.Session()
            session.headers.update(HEADERS)

            r = session.get(url, verify=False, timeout=15)

            # ── Diagnostic expander (only visible during development) ──────────
            with st.expander("🔍 Debug info", expanded=False):
                st.write(f"**Status code:** {r.status_code}")
                st.write(f"**URL fetched:** {r.url}")
                if r.status_code != 200:
                    st.warning("eBay returned a non-200 status — may be blocking the request.")

            soup = BeautifulSoup(r.content, "html5lib")

            # ── Try each selector until we get results ─────────────────────────
            items = []
            matched_selector = None
            for tag, attrs in ITEM_SELECTORS:
                found = soup.find_all(tag, attrs)
                if found:
                    items = found
                    matched_selector = (tag, attrs)
                    break

            with st.expander("🔍 Debug info", expanded=False):
                st.write(f"**Selector used:** {matched_selector}")
                st.write(f"**Raw items found:** {len(items)}")

            scraped_data = []
            bu_prices    = []

            for item in items:
                # Skip eBay's ghost/filler elements
                title_text = try_find_text(item, "div", TITLE_SELECTORS) or \
                             try_find_text(item, "span", TITLE_SELECTORS)

                if not title_text or title_text.lower() in ("shop on ebay", ""):
                    continue

                price_text   = try_find_text(item, "span", PRICE_SELECTORS) or \
                               try_find_text(item, "div",  PRICE_SELECTORS)
                reviews_text = try_find_text(item, "span", REVIEW_SELECTORS) or \
                               try_find_text(item, "div",  REVIEW_SELECTORS) or "0"

                bu_prices.append(price_text)
                scraped_data.append({
                    "title":    title_text,
                    "price":    price_text,
                    "reviews":  reviews_text,
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
                # ── Helpful fallback message ───────────────────────────────────
                st.warning(
                    "No listings found. This usually means eBay served a CAPTCHA "
                    "or changed their HTML structure. Check the **Debug info** "
                    "expander above for clues."
                )
                with st.expander("📄 Raw HTML preview (first 3000 chars)"):
                    st.code(r.text[:3000], language="html")

        except Exception as e:
            st.error(f"An error occurred while scraping: {e}")

st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
