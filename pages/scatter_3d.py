import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

st.subheader("🧊 3D Scatter Plot — Price × Reviews × Rating")
st.markdown("Visualizes the relationship between product price, number of reviews, and rating.")

api_3d_data = st.session_state.get("api_3d_data")

if not api_3d_data:
    st.info("Please fetch data from the SerpAPI Scraper first, then return here.")
    st.page_link("pages/serpapi_scraper.py", label="← Go to SerpAPI Scraper", icon="🔑")
    st.stop()

# ── Clean data ─────────────────────────────────────────────────────────────────

df = pd.DataFrame(api_3d_data)
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["reviews"] = pd.to_numeric(
    df["reviews"].astype(str).str.replace(",", "").str.extract(r"(\d+)")[0],
    errors="coerce",
)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df = df.dropna(subset=["price", "reviews", "rating"])

# Remove top 5% price outliers so chart isn't squashed
if not df.empty:
    price_cap = df["price"].quantile(0.95)
    df = df[df["price"] <= price_cap]

if df.empty:
    st.warning("Not enough clean data to plot. Try a different search query.")
    st.stop()

st.markdown(
    f"**{len(df)} products** after cleaning · "
    f"price capped at 95th percentile (${df['price'].max():.0f})"
)

# ── Layout: 3D plot + 2 supporting 2D charts ──────────────────────────────────

fig = plt.figure(figsize=(16, 6), facecolor="#0e1117")
fig.patch.set_facecolor("#0e1117")
gs  = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)

text_kw   = {"color": "white"}
spine_col = "#444444"

# — 3D scatter ——————————————————————————————————————————————————————————————————
ax3d = fig.add_subplot(gs[0], projection="3d")
ax3d.set_facecolor("#0e1117")
sc = ax3d.scatter(
    df["price"], df["reviews"], df["rating"],
    c=df["price"], cmap="plasma", s=60, alpha=0.85, edgecolors="none",
)
ax3d.set_xlabel("Price ($)",  **text_kw, labelpad=8)
ax3d.set_ylabel("Reviews",    **text_kw, labelpad=8)
ax3d.set_zlabel("Rating",     **text_kw, labelpad=8)
ax3d.set_title("3D Overview", **text_kw, pad=12)
ax3d.tick_params(colors="white")
ax3d.xaxis.pane.fill = ax3d.yaxis.pane.fill = ax3d.zaxis.pane.fill = False
ax3d.xaxis.pane.set_edgecolor(spine_col)
ax3d.yaxis.pane.set_edgecolor(spine_col)
ax3d.zaxis.pane.set_edgecolor(spine_col)
fig.colorbar(sc, ax=ax3d, pad=0.12, label="Price ($)", shrink=0.6)

# — Price vs Rating ————————————————————————————————————————————————————————————
ax1 = fig.add_subplot(gs[1])
ax1.set_facecolor("#0e1117")
ax1.scatter(df["price"], df["rating"], c=df["price"], cmap="plasma",
            alpha=0.8, s=50, edgecolors="none")
xs = np.linspace(df["price"].min(), df["price"].max(), 100)
if len(df) > 2:
    z = np.polyfit(df["price"], df["rating"], 1)
    ax1.plot(xs, np.poly1d(z)(xs), color="#ff6b6b", linewidth=1.5,
             linestyle="--", label="Trend")
    ax1.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=8)
ax1.set_xlabel("Price ($)", **text_kw)
ax1.set_ylabel("Rating",    **text_kw)
ax1.set_title("Price vs Rating", **text_kw)
ax1.tick_params(colors="white")
for sp in ax1.spines.values():
    sp.set_edgecolor(spine_col)

# — Price vs Reviews ————————————————————————————————————————————————————————————
ax2 = fig.add_subplot(gs[2])
ax2.set_facecolor("#0e1117")
ax2.scatter(df["price"], df["reviews"], c=df["reviews"], cmap="cool",
            alpha=0.8, s=50, edgecolors="none")
if len(df) > 2:
    z2 = np.polyfit(df["price"], df["reviews"], 1)
    ax2.plot(xs, np.poly1d(z2)(xs), color="#ffd93d", linewidth=1.5,
             linestyle="--", label="Trend")
    ax2.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=8)
ax2.set_xlabel("Price ($)",       **text_kw)
ax2.set_ylabel("Reviews",         **text_kw)
ax2.set_title("Price vs Reviews", **text_kw)
ax2.tick_params(colors="white")
for sp in ax2.spines.values():
    sp.set_edgecolor(spine_col)

st.pyplot(fig)
plt.close(fig)

# ── Quick stats ────────────────────────────────────────────────────────────────

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Avg Price",   f"${df['price'].mean():.2f}")
c2.metric("Avg Rating",  f"{df['rating'].mean():.2f} ⭐")
c3.metric("Avg Reviews", f"{df['reviews'].mean():.0f}")

st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")