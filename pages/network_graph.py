import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

st.subheader("🌐 Network Graph — Product Relationships")
st.markdown("Maps how products connect to shared price ranges and review counts.")

api_data = st.session_state.get("api_data")

if not api_data:
    st.info("Please fetch data from the SerpAPI Scraper first, then return here.")
    st.page_link("pages/serpapi_scraper.py", label="← Go to SerpAPI Scraper", icon="🔑")
    st.stop()

# ── Helpers ────────────────────────────────────────────────────────────────────

def categorize_price(price):
    try:
        price = float(price)
    except (TypeError, ValueError):
        return "Unknown Price"
    if price < 50:
        return "$0–50"
    elif price < 100:
        return "$50–100"
    elif price < 200:
        return "$100–200"
    elif price < 500:
        return "$200–500"
    return "$500+"

def categorize_reviews(reviews):
    try:
        if isinstance(reviews, str):
            reviews = int(reviews.replace(",", "").split()[0])
        reviews = int(reviews)
    except (TypeError, ValueError):
        return "Unknown Reviews"
    if reviews < 10:
        return "0–10 reviews"
    elif reviews < 50:
        return "10–50 reviews"
    elif reviews < 100:
        return "50–100 reviews"
    elif reviews < 500:
        return "100–500 reviews"
    return "500+ reviews"

def build_graph(data):
    G = nx.Graph()
    for product in data:
        name       = product["title"][:20]
        price_cat  = categorize_price(product["price"])
        review_cat = categorize_reviews(product["reviews"])
        G.add_node(name,       node_type="Product")
        G.add_node(price_cat,  node_type="Price")
        G.add_node(review_cat, node_type="Reviews")
        G.add_edge(name, price_cat)
        G.add_edge(name, review_cat)
    return G

def draw_graph(G):
    color_map = {"Product": "cyan", "Price": "royalblue", "Reviews": "limegreen"}
    colors    = [color_map.get(G.nodes[n].get("node_type", "Product"), "gray") for n in G.nodes]
    pos       = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(14, 9))
    nx.draw(G, pos, ax=ax, with_labels=True, node_color=colors,
            edge_color="gray", node_size=2000, font_size=7)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="cyan",       label="Product"),
        Patch(facecolor="royalblue",  label="Price Range"),
        Patch(facecolor="limegreen",  label="Review Count"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=9)
    st.pyplot(fig)
    plt.close(fig)

# ── Filter & draw ──────────────────────────────────────────────────────────────

filtered = [w for w in api_data if w.get("title") and w.get("price") and w.get("reviews")]

if not filtered:
    st.warning("No usable data found. Make sure data was fetched on the SerpAPI Scraper page.")
else:
    G = build_graph(filtered)
    draw_graph(G)

    st.markdown("---")
    st.subheader("📌 Network Insights")

    degree_dict = dict(G.degree())
    top_nodes   = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    st.write("🔝 Top 5 Most Connected Nodes:")
    for node, degree in top_nodes:
        st.markdown(f"- **{node}** — degree `{degree}`")

    communities = list(nx.connected_components(G))
    st.write(f"🌐 Detected **{len(communities)} communities** in the network.")

st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")