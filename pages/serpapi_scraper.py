import streamlit as st
import pandas as pd
import requests
import ssl
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

st.subheader("🔑 API Scraping with SerpAPI")
st.markdown("Fetches structured eBay product data via the **SerpAPI** service — clean, fast, and reliable.")

search_q = st.text_input("Enter what to search:", placeholder="e.g. watches for men")

if search_q:
    params = {
        "api_key": st.secrets["SERPAPI_KEY"],
        "engine": "ebay",
        "_nkw": search_q,
        "output": "json",
    }

    with st.spinner("Fetching from SerpAPI…"):
        try:
            response = requests.get("https://serpapi.com/search", params=params, verify=False)
            results  = response.json()
            organic  = results.get("organic_results", [])

            api_data    = []
            api_3d_data = []
            api_prices  = []

            for item in organic:
                title    = item.get("title",   "No title")
                link     = item.get("link",    "No link")
                price    = item.get("price",   "No price")
                rating   = item.get("rating",  "No rating")
                reviews  = item.get("reviews", "No reviews")
                rating0  = item.get("rating",  0)
                reviews0 = item.get("reviews", 0)

                # Normalize price to float
                if isinstance(price, dict) and "extracted" in price:
                    price_value = price["extracted"]
                elif isinstance(price, str):
                    try:
                        price_value = float(price.replace("$", "").replace(",", ""))
                    except ValueError:
                        price_value = None
                else:
                    price_value = None

                api_prices.append(price_value)
                api_3d_data.append({"price": price_value, "rating": rating0, "reviews": reviews0})
                api_data.append({
                    "title":   title,
                    "price":   price_value,
                    "rating":  rating,
                    "reviews": reviews,
                    "link":    link,
                })

            if api_data:
                df = pd.DataFrame(api_data)
                st.success(f"Retrieved {len(df)} results for **{search_q}**")
                st.dataframe(df, use_container_width=True)

                api_csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download API CSV",
                    data=api_csv,
                    file_name="api_data.csv",
                    mime="text/csv",
                    icon=":material/download:",
                )

                st.session_state.api_prices  = api_prices
                st.session_state.api_data    = api_data
                st.session_state.api_3d_data = api_3d_data

                st.markdown("---")
                st.markdown("#### ✅ Done! Continue to the visualizations:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.page_link("pages/network_graph.py",  label="Network Graph",   icon="🌐")
                with col2:
                    st.page_link("pages/price_heatmap.py",  label="Price Heatmap",   icon="🔥")
                with col3:
                    st.page_link("pages/scatter_3d.py",     label="3D Scatter Plot", icon="🧊")

            else:
                st.warning("No results returned. Try a different search term.")

        except Exception as e:
            st.error(f"An error occurred while accessing SerpAPI: {e}")

st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")