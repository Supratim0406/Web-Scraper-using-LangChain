import streamlit as st
from langchain_community.document_loaders import WebBaseLoader, SeleniumURLLoader, UnstructuredURLLoader


#----------------------- USER AGENTS LIST ----------------------------------------------

USER_AGENTS = [

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",

]

# ------------------------- STREAMLIT UI----------------------------------------------------------

## Sidebar
st.sidebar.title("⚙️ Scraper Options")
scraper_choice = st.sidebar.selectbox("Choose Scraper", ("Unstructured Loader", "Selenium Loader", "WebBase Loader"))
user_agent = st.sidebar.selectbox("Choose User Agent", USER_AGENTS)


# -----------------------------MAIN AREA ----------------------------------------------------------

st.set_page_config(page_title='Web Scraper', layout='wide')
st.title("🌐 LangChain Web Scraper")
url = st.text_input("Enter a Website URL:")

if st.button("Scrape Now"):
    with st.spinner("Scrapping content... Wait for few mins"):
        if not url:
            st.error("Please enter a valid URL")
        else:
            try:
                docs=[]
            
                if scraper_choice == "Unstructured Loader":
                    loader = UnstructuredURLLoader(urls=[url], headers = {"User-Agent": user_agent})
                    docs = loader.load()

                elif scraper_choice == "Selenium Loader":
                    loader = SeleniumURLLoader(urls=[url], headless=False, browser="chrome")
                    docs = loader.load()

                elif scraper_choice == "WebBase Loader":
                    loader = WebBaseLoader(url, header_template={"User-Agent": user_agent})
                    docs = loader.load()

                # Display output
                if docs:
                    full_text = "\n\n".join([doc.page_content for doc in docs])

                    # Snippet Preview
                    st.subheader("📌 Snippet Preview:")
                    st.write(full_text[:1000] + ("..." if len(full_text) > 1000 else ""))

                    # View All + Copy
                    st.subheader("📖 Full Content:")
                    with st.expander("Click to View Full Text"):
                        st.text_area("Scraped Text", full_text, height=400)
                        st.download_button("📋 Copy/Download Text", full_text, file_name="scraped_content.txt")

                else:
                    st.warning("⚠️ No content extracted. Try another scraper or user-agent.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")