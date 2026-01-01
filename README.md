# 🕵️‍♂️ Dark Pattern Detective

**A Machine Learning project that protects users from manipulative website designs.**

## 📖 What is this project?
Have you ever tried to book a hotel or buy a shirt, and saw messages like:
* *"Hurry! Only 1 room left!"*
* *"15 people are looking at this right now!"*
* *"Offer expires in 05:00 minutes!"*

These are called **Dark Patterns**—tricks used by websites to pressure you into spending money.

**Dark Pattern Detective** is an AI-powered tool that scans any product webpage, finds these hidden manipulative sentences, and warns you about them instantly.

---

## 🚀 How It Works
1.  **Input:** You paste a URL (link) of a product page.
2.  **Scraping:** The tool visits the website and reads all the text (like a human would).
3.  **AI Analysis:** It splits the text into sentences and feeds them into a **Random Forest** Machine Learning model.
4.  **Output:** It highlights exactly which sentences are "Dark Patterns" designed to trick you.

---

## 🛠️ Tech Stack
This project is built using Python.
* **Python:** The programming language.
* **Streamlit:** To create the web interface (Frontend).
* **Scikit-Learn:** For the Machine Learning model (Random Forest).
* **BeautifulSoup & LXML:** For scraping text from websites.
* **Pandas:** For handling data.

---

## 💻 Installation Guide (Step-by-Step)

Follow these steps to run the project on your own computer.

### Prerequisites
Make sure you have **Python** installed. You can check by typing `python --version` in your terminal.

### Step 1: Download the Project
Download the folder or clone the repository:

git clone [https://github.com/PrajwalGN1/dark-pattern-detective.git](https://github.com/PrajwalGN1/dark-pattern-detective.git)
cd dark-pattern-detective

### Step 2: Install Required Libraries
Open your terminal (Command Prompt) inside the project folder and run: [ pip install streamlit pandas scikit-learn beautifulsoup4 requests lxml]

### 🏃‍♂️ How to Run the App
You need to train the AI "Brain" first, and then start the website.

1. Train the Model
This creates the brain of the project (dark_pattern_model.pkl). Run this command:  [python train.py]
You should see a message: ✅ Model trained and saved!

2. Start the Website
Now, launch the Streamlit app:   [streamlit run app.py]

3. Use the App
A new tab will open in your browser (usually at http://localhost:8501).

Paste a product URL (e.g., from a booking or shopping site) into the box.

Click "Scan Now".

See the results!

### 📂 Project Structure
Here is what the files in the folder do:

 train.py:  The script that teaches the AI. It contains the list of "Dark Pattern" phrases and trains the Random Forest classifier.

 app.py:   The main website code. It handles the user interface and runs the scanning logic.

 dark_pattern_model.pkl:  The saved AI "Brain" (created after running train.py).

 vectorizer.pkl:   A helper file that translates English words into numbers the AI understands.
 

### 🔮 Future Improvements
If you want to contribute or improve this project, here are some ideas:

[ ] Add a larger dataset with thousands of dark pattern examples.

[ ] Build a Chrome Extension so it runs automatically while browsing.

[ ] Detect "Visual" dark patterns (like hidden 'X' buttons).

🤝 Author
Built by PRAJWAL G N 
[www.linkedin.com/in/prajwa3741a9332l-g-n-](https://www.linkedin.com/in/prajwa3741a9332l-g-n-/)

[(https://github.com/PrajwalGN1](https://github.com/PrajwalGN1)

