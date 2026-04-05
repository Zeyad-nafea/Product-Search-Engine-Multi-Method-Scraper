import streamlit as st

st.balloons()
st.title("🎉 Project Wrap-Up")

st.markdown("""
### 🏫 Zewail City of Science and Technology
**University of Science and Technology**  
**Computational Sciences and Artificial Intelligence (CSAI) Program**  
**Course:** DSAI 103 – *Data Acquisition in Data Science*  
**Instructor:** Dr. Mohamed Maher Ata  
**Teaching Assistants:** Rasha Mostafa · Bassem Adel Naguib
""")

st.markdown("""
## 🙏 Special Thanks
A heartfelt thank you to our doctor and TAs for teaching this course and guiding us through the project.  
We truly learned a lot and had fun doing it! 😊
""")

st.markdown("## 👥 Team Members")

team = {
    "Zeyad Mohamed Fathy":     "https://www.linkedin.com/in/zeyad-nafea-314354357/",
    "Radwa Abd El Sadek Salah": "https://www.linkedin.com/in/radwa-salah-84b752357",
}

for name, link in team.items():
    st.markdown(f"- [{name}]({link})")

st.markdown("""
## 💬 Reflections
- Loved working as a team 🤝  
- Learned a lot about web scraping, data visualization, and Streamlit 📊  
- Excited to keep building! 🚀
""")

sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("faces")
if selected is not None:
    st.markdown(f"You selected **{sentiment_mapping[selected]} star(s)**. Thank you! ⭐")

st.success("Thanks for exploring our project — hope you liked it! 😄")
st.markdown("---")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")