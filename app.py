import streamlit as st
import pickle
import requests
from bs4 import BeautifulSoup
import re
import time # Added to show how fast it runs

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Dark Pattern Detective", page_icon="⚡")

# --- 2. LOAD MODEL (Cached) ---
@st.cache_resource
def load_model():
    try:
        with open("dark_pattern_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        return None, None

model, vectorizer = load_model()

# --- 3. OPTIMIZED FUNCTIONS ---

def scrape_website(url):
    """Scrapes text using the fast 'lxml' parser."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        # Timeout set to 5 seconds so it doesn't hang on slow sites
        response = requests.get(url, headers=headers, timeout=5)
        
        # 'lxml' is much faster than 'html.parser'
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Only look at specific tags to save time
        tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'span', 'div', 'li', 'button'])
        
        return [t.get_text(strip=True) for t in tags]
    except Exception as e:
        return []

def analyze_text_batch(text_list):
    """
    Optimized: Predicts ALL sentences in one go (Batch Processing).
    """
    # 1. Pre-process: Split all text into sentences first
    all_sentences = []
    for block in text_list:
        # Fast split by common punctuation
        splits = re.split(r'[.!?]+', block)
        # Filter junk (length < 10) immediately
        all_sentences.extend([s.strip() for s in splits if len(s.strip()) > 10])

    # 2. Deduplicate (Don't check the same sentence twice)
    unique_sentences = list(set(all_sentences))
    
    if not unique_sentences:
        return []

    # 3. FAST PREDICTION (The Speed Boost)
    # Instead of a loop, we transform and predict EVERYTHING at once.
    vectors = vectorizer.transform(unique_sentences)
    predictions = model.predict(vectors)

    # 4. Filter results
    # Zip combines the sentence with its prediction result
    found_patterns = [sent for sent, pred in zip(unique_sentences, predictions) if pred == 1]
    
    return found_patterns

# --- 4. THE APP INTERFACE ---
st.title("⚡ Dark Pattern Detective")
st.write("Enter a product URL. The AI will scan it instantly.")

if model is None:
    st.error("❌ Error: Model files missing. Run 'train.py' first!")
else:
    url = st.text_input("Enter Website URL:", placeholder="https://example.com")
    
    if st.button("Scan Now"):
        if not url:
            st.warning("Please enter a URL.")
        else:
            if not url.startswith("http"):
                url = "https://" + url
            
            start_time = time.time()
            
            with st.spinner("🚀 Speed scanning..."):
                # Step 1: Get Data
                website_text = scrape_website(url)
                
                if not website_text:
                    st.error("Could not read website. It might be blocking bots.")
                else:
                    # Step 2: Analyze Data
                    dark_patterns = analyze_text_batch(website_text)
                    
                    # Calculate time taken
                    elapsed_time = time.time() - start_time
                    
                    st.divider()
                    st.caption(f"⏱️ Scan completed in {elapsed_time:.2f} seconds")

                    if dark_patterns:
                        st.error(f"⚠️ DANGER: Found {len(dark_patterns)} unique issues:")
                        for i, dp in enumerate(dark_patterns, 1):
                            st.write(f"**{i}.** \"{dp}\"")
                    else:
                        st.success("✅ This page looks safe!")
