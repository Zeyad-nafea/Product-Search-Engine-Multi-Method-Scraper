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

has_api = bool(api_prices)
has_bu  = bool(bu_prices)

# ── Guard: need at least one source ───────────────────────────────────────────
if not has_api and not has_bu:
    st.info("Please complete at least one scraping step before viewing this page.")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/beautifulsoup_scraper.py", label="← BeautifulSoup Scraper", icon="🍵")
    with col2:
        st.page_link("pages/serpapi_scraper.py", label="← SerpAPI Scraper", icon="🔑")
    st.stop()

# Soft warnings if only one source is available
if not has_bu:
    st.warning("⚠️ BeautifulSoup data not found — showing SerpAPI data only.")
if not has_api:
    st.warning("⚠️ SerpAPI data not found — showing BeautifulSoup data only.")

# ── Helpers ───────────────────────────────────────────────────────────────────
def kde_quartic(d, h):
    dn = d / h
    return (15 / 16) * (1 - dn ** 2) ** 2 if dn <= 1 else 0

def parse_price(p, cap=200):
    try:
        val = float(str(p).replace("$", "").replace(",", "")) if isinstance(p, str) else float(p)
        return val if val < cap else None
    except (TypeError, ValueError):
        return None

# ── Collect points ────────────────────────────────────────────────────────────
points = []

if has_bu:
    for p in bu_prices:
        val = parse_price(p)
        if val is not None:
            points.append((val, 0))

if has_api:
    for p in api_prices:
        val = parse_price(p)
        if val is not None:
            points.append((val, 1 if has_bu else 0))

if not points:
    st.warning("Insufficient numeric price data to generate heatmaps.")
    st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
    st.stop()

x = [pt[0] for pt in points]
y = [pt[1] for pt in points]

# ── Determine y-axis labels based on available data ───────────────────────────
if has_bu and has_api:
    ytick_positions = [0, 1]
    ytick_labels    = ["BeautifulSoup", "SerpAPI"]
elif has_api:
    ytick_positions = [0]
    ytick_labels    = ["SerpAPI"]
else:
    ytick_positions = [0]
    ytick_labels    = ["BeautifulSoup"]

# ── KDE Heatmap ───────────────────────────────────────────────────────────────
grid_size = 1
h         = 2
x_min, x_max = min(x), max(x)
y_min, y_max = min(y), max(y)

# Prevent zero-height grid when only one method is present
if y_min == y_max:
    y_min -= 0.5
    y_max += 0.5

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
ax1.set_yticks(ytick_positions)
ax1.set_yticklabels(ytick_labels)
ax1.set_title("KDE Heatmap: Price Distribution by Scraping Method")
ax1.legend(loc="upper right")
st.pyplot(fig1)
plt.close(fig1)

# ── Colored Block Heatmap ─────────────────────────────────────────────────────
heat_data = {}

if has_bu:
    clean_bu = [parse_price(p) for p in bu_prices if parse_price(p) is not None]
    if clean_bu:
        heat_data["BeautifulSoup"] = pd.Series(clean_bu)

if has_api:
    clean_api = [parse_price(p) for p in api_prices if parse_price(p) is not None]
    if clean_api:
        heat_data["SerpAPI"] = pd.Series(clean_api)

if heat_data:
    df_heat = pd.DataFrame(heat_data)
    df_heat.fillna(df_heat.mean(), inplace=True)

    fig2, ax2 = plt.subplots(figsize=(12, max(2, len(heat_data))))
    sns.heatmap(df_heat.T, cmap="coolwarm", annot=False, linewidths=1, cbar=True, ax=ax2)
    title = (
        "Colored Block Heatmap: Price Comparison — BeautifulSoup vs SerpAPI"
        if has_bu and has_api
        else f"Colored Block Heatmap: Price Distribution — {'SerpAPI' if has_api else 'BeautifulSoup'}"
    )
    ax2.set_title(title)
    st.pyplot(fig2)
    plt.close(fig2)

st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
