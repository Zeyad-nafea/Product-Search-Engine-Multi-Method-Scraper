import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

st.subheader("🔥 Price Heatmap — BeautifulSoup vs SerpAPI")
st.markdown("Compares the price distribution of products collected via both scraping methods.")

api_prices = st.session_state.get("api_prices")
bu_prices  = st.session_state.get("bu_prices")

if not api_prices or not bu_prices:
    st.info("Please complete both Step 1 (BeautifulSoup) and Step 2 (SerpAPI) before viewing this page.")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/beautifulsoup_scraper.py", label="← BeautifulSoup Scraper", icon="🍵")
    with col2:
        st.page_link("pages/serpapi_scraper.py", label="← SerpAPI Scraper", icon="🔑")
    st.stop()

# ── Helpers ────────────────────────────────────────────────────────────────────

def kde_quartic(d, h):
    dn = d / h
    return (15 / 16) * (1 - dn ** 2) ** 2 if dn <= 1 else 0

def parse_price(p, cap=200):
    try:
        val = float(str(p).replace("$", "").replace(",", "")) if isinstance(p, str) else float(p)
        return val if val < cap else None
    except (TypeError, ValueError):
        return None

# ── Collect points ─────────────────────────────────────────────────────────────

points = []
for p in bu_prices:
    val = parse_price(p)
    if val is not None:
        points.append((val, 0))

for p in api_prices:
    val = parse_price(p)
    if val is not None:
        points.append((val, 1))

if not points:
    st.warning("Insufficient data to generate heatmaps. Try different search queries.")
    st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
    st.stop()

x = [pt[0] for pt in points]
y = [pt[1] for pt in points]

# ── KDE Heatmap ────────────────────────────────────────────────────────────────

grid_size = 1
h         = 2
x_min, x_max = min(x), max(x)
y_min, y_max = min(y), max(y)

x_grid = np.arange(x_min - h, x_max + h, grid_size / 2)
y_grid = np.arange(y_min - h, y_max + h, grid_size / 2)
x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
xc = x_mesh + grid_size / 4
yc = y_mesh + grid_size / 4

intensity = np.array([
    [sum(kde_quartic(math.sqrt((xc[r, c] - xi) ** 2 + (yc[r, c] - yi) ** 2), h)
         for xi, yi in zip(x, y))
     for c in range(xc.shape[1])]
    for r in range(xc.shape[0])
])

fig1, ax1 = plt.subplots(figsize=(10, 5))
hm = ax1.pcolormesh(x_mesh, y_mesh, intensity, shading="auto", cmap="plasma")
ax1.scatter(x, y, c="red", marker="o", edgecolor="k", s=50, label="Data Points")
fig1.colorbar(hm, ax=ax1, label="Intensity")
ax1.set_xlabel("Price ($)")
ax1.set_ylabel("Scraping Method")
ax1.set_yticks([0, 1])
ax1.set_yticklabels(["BeautifulSoup", "SerpAPI"])
ax1.set_title("KDE Heatmap: Price Distribution by Scraping Method")
ax1.legend(loc="upper right")
st.pyplot(fig1)
plt.close(fig1)

# ── Colored Block Heatmap ──────────────────────────────────────────────────────

clean_bu  = [parse_price(p) for p in bu_prices  if parse_price(p) is not None]
clean_api = [parse_price(p) for p in api_prices if parse_price(p) is not None]

df_heat = pd.DataFrame({
    "BeautifulSoup": pd.Series(clean_bu),
    "SerpAPI":       pd.Series(clean_api),
})
df_heat.fillna(df_heat.mean(), inplace=True)

fig2, ax2 = plt.subplots(figsize=(12, 2))
sns.heatmap(df_heat.T, cmap="coolwarm", annot=False, linewidths=1, cbar=True, ax=ax2)
ax2.set_title("Colored Block Heatmap: Price Comparison — BeautifulSoup vs SerpAPI")
st.pyplot(fig2)
plt.close(fig2)

st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")