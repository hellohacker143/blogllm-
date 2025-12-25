import streamlit as st
import google.generativeai as genai

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="📝",
    layout="wide"
)

st.title("AI Blog Generator with Streamlit")
st.write("Type any topic (e.g., *how to host in Git and Streamlit*) and get a full SEO blog.")

# ---------- SIDEBAR: CONTROL ----------
st.sidebar.header("Settings")

api_key = st.sidebar.text_input("Gemini API Key", type="password")
model_name = st.sidebar.text_input("Model name", value="gemini-1.5-flash")

temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.7, 0.05)
max_tokens = st.sidebar.slider("Max output tokens", 256, 4096, 2048, 128)

# Default blog prompt template (you can edit this text)
default_prompt_template = """
Write high-quality, plagiarism-free, human-like content.

Use simple and clear language.
Follow on-page SEO best practices.
No emojis.
No extra explanation.

Main Keyword:
{keyword}

Topic:
{topic}

Instructions:
- Create a powerful SEO title with high CTR.
- Write a meta description (150–160 characters).
- Generate a short SEO-friendly URL slug.
- List focus keyword and LSI keywords.
- Use headings and CLEARLY label them exactly as:
  H1: Main Heading
  H2: Sub Heading
  H3: Sub-Sub Heading
- Do NOT use normal headings without H1, H2, H3 labels.
- Write minimum 1200 words.
- Optimize for Google Discover and social sharing.
"""

st.sidebar.subheader("Default Blog Prompt Template")
st.sidebar.caption("Use {keyword} and {topic} placeholders; app will fill them.")
user_template = st.sidebar.text_area(
    "Prompt template",
    value=default_prompt_template,
    height=260
)

# ---------- MAIN INPUT ----------
topic = st.text_input(
    "Enter your topic",
    value="structure of DBMS",
    help="Example: how to host in Git and Streamlit"
)
keyword = st.text_input(
    "Main keyword",
    value="structure of DBMS"
)

generate_btn = st.button("Generate Blog")

# ---------- VALIDATION ----------
if not api_key:
    st.info("Add your Gemini API key in the sidebar to start.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name)

# ---------- GENERATION LOGIC ----------
if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        final_prompt = user_template.format(keyword=keyword, topic=topic)

        with st.expander("Show final prompt sent to LLM"):
            st.code(final_prompt, language="markdown")

        with st.spinner("Generating blog article..."):
            try:
                response = model.generate_content(
                    final_prompt,
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": max_tokens,
                    },
                )
                blog_text = response.text

                st.subheader("Generated Blog Article")
                st.markdown(blog_text)

                # Download button
                st.download_button(
                    label="Download as .txt",
                    data=blog_text,
                    file_name=f"{topic.replace(' ', '-').lower()}-blog.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error while generating blog: {e}")
