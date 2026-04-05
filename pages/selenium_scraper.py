import streamlit as st

st.subheader("🤖 Selenium Scraper (Local Only)")

st.warning(
    "⚠️ **Selenium cannot run inside Streamlit Cloud** due to browser security restrictions. "
    "Download the script below and run it locally on your own machine.",
    icon="🚫",
)

# ── Standalone script ──────────────────────────────────────────────────────────

SELENIUM_SCRIPT = '''import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ── Configuration ──────────────────────────────────────────────────────────────
SEARCH_QUERY = "watches for men"   # ← change this to whatever you like
OUTPUT_FILE  = "selenium_data.csv"
# ──────────────────────────────────────────────────────────────────────────────

search_url = f"https://www.ebay.com/sch/i.html?_nkw={SEARCH_QUERY.replace(' ', '+')}&_sop=12"

driver = webdriver.Chrome()
driver.get(search_url)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "s-item__wrapper"))
    )
    items = driver.find_elements(By.CLASS_NAME, "s-item__wrapper")

    s_data = []
    for item in items[2:]:
        try:
            title   = item.find_element(By.CLASS_NAME, "s-item__title").text
            price   = item.find_element(By.CLASS_NAME, "s-item__price").text
            reviews = "0 reviews"
            try:
                reviews = item.find_element(By.CLASS_NAME, "s-item__reviews-count").text
            except Exception:
                pass
            s_data.append({
                "title":    title,
                "price":    price,
                "reviews":  reviews,
                "category": SEARCH_QUERY.capitalize(),
            })
        except Exception as e:
            print(f"Skipping item: {e}")

finally:
    driver.quit()

df = pd.DataFrame(s_data)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} rows to {OUTPUT_FILE}")
print(df.head())
'''

st.download_button(
    label="⬇️ Download Selenium Script",
    data=SELENIUM_SCRIPT,
    file_name="selenium_scraper.py",
    mime="text/x-python",
    icon=":material/download:",
)

# ── Instructions ───────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("## 🛠️ How to Run the Script Locally")

st.markdown("""
**Step 1 — Install dependencies**
```bash
pip install selenium pandas
```

**Step 2 — Install ChromeDriver**

ChromeDriver must match your installed version of Google Chrome.

- **Automatic (recommended):** use `webdriver-manager`:
```bash
pip install webdriver-manager
```
Then replace the `webdriver.Chrome()` line in the script with:
```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

- **Manual:** download from https://chromedriver.chromium.org/downloads and place it on your PATH.

**Step 3 — Edit the script (optional)**

Open `selenium_scraper.py` and change `SEARCH_QUERY` to whatever you want to search for.

**Step 4 — Run**
```bash
python selenium_scraper.py
```
Results are saved to `selenium_data.csv` in the same folder.
""")

st.info("💡 A Chrome browser window will open automatically while the script runs — that's normal!")

st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")