import requests
from bs4 import BeautifulSoup
import pickle
import re # Added regex to help split sentences better

# --- LOAD THE BRAIN ---
try:
    with open("dark_pattern_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
except FileNotFoundError:
    print("❌ Error: You must run 'train.py' first!")
    exit()

def analyze_text(text_list):
    """
    Checks a list of text for dark patterns.
    Splits long text into individual sentences to pinpoint the exact bad phrase.
    """
    found_patterns = set() # Use a set to automatically remove duplicates
    
    for block in text_list:
        # 1. Split the block of text into individual sentences
        # We split by periods (.), exclamation marks (!), or question marks (?)
        sentences = re.split(r'[."!?]+', block)
        
        for sentence in sentences:
            sentence = sentence.strip() # Remove extra spaces
            
            # 2. Filter out short/junk text
            if len(sentence) < 10: continue 
            
            # 3. Predict using the AI model
            vec = vectorizer.transform([sentence])
            prediction = model.predict(vec)
            
            # 4. If it is a Dark Pattern, add ONLY this sentence
            if prediction[0] == 1:
                found_patterns.add(sentence)
            
    return list(found_patterns)

def scan_url():
    """Scrapes a real website."""
    url = input("\n🌐 Enter URL to scan: ")
    if not url.startswith("http"):
        url = "https://" + url
        
    print(f"   Fetching {url}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # We look for text in headers, paragraphs, and spans
        tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'span', 'div', 'li'])
        return [t.get_text(strip=True) for t in tags]
    except Exception as e:
        print(f"❌ Could not scrape website: {e}")
        return []

# --- MAIN MENU ---
print("\n🕵️  DARK PATTERN DETECTIVE 🕵️")
print("1. Scan a Live Website")
print("2. Test a Manual Sentence")
choice = input("Choose an option (1 or 2): ")

text_to_analyze = []

if choice == '1':
    text_to_analyze = scan_url()
elif choice == '2':
    user_text = input("\n✍️  Type a sentence to test: ")
    text_to_analyze = [user_text]

# --- RUN ANALYSIS ---
print("\n🔍 Analyzing...")
dark_patterns = analyze_text(text_to_analyze)

# --- REPORTING (This is the part you asked to change) ---
print(f"\n--- DARK PATTERNS FOUND ---")

if dark_patterns:
    print(f"⚠️  Found {len(dark_patterns)} unique issues:\n")
    # This loop prints them number-wise
    for i, dp in enumerate(dark_patterns, 1):
        print(f"{i}. \"{dp}\"")
else:
    print("✅ No dark patterns detected.")
