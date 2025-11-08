

# 🧠 Intelligent FAQ Chatbot

An **AI-powered desktop chatbot** built with **Python** and **Tkinter** during my internship with CodeAlpha, designed to answer Frequently Asked Questions (FAQs) using **Natural Language Processing (NLP)**.
It provides an interactive and user-friendly interface for instant responses, feedback logging, and real-time typing simulation.

---

## 🚀 Features

* **Interactive GUI:** Clean, responsive Tkinter interface with chat bubbles and typing indicators.
* **AI-Powered Responses:** Uses **TF-IDF** and **Cosine Similarity** to find the best-matching answer.
* **Context Awareness:** Maintains recent conversation context for more accurate replies.
* **Feedback Logging:** Users can rate responses (👍 / 👎), and feedback is automatically saved in `feedback_log.json`.
* **Offline-Ready NLP:** Pretrained using NLTK datasets for tokenization, lemmatization, and stopword removal.
* **Error Handling:** Checks for missing NLTK data and provides easy setup instructions.
* **Customization:** Easily update or replace the FAQ dataset for any business or use case.

---

## 🧩 Project Structure

```
│
├── chatbot.py            # Main GUI application and NLP engine
├── download_data.py      # NLTK data downloader (run once before using)
├── create_icon.py        # Generates the chat send icon (send_icon.png)
├── feedback_log    # Stores user feedback (auto-generated)
├── FAQ/                  #  Folder for additional FAQ data
└── README.md             # Project documentation
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/faq-chatbot.git
cd faq-chatbot
```

### 2️⃣ Install Dependencies

```bash
pip install nltk scikit-learn pillow
```

### 3️⃣ Download Required NLTK Data

Run the helper script:

```bash
python download_data.py
```

This ensures that **punkt**, **stopwords**, and **wordnet** datasets are available.

### 4️⃣ Generate the Icon

```bash
python create_icon.py
```

### 5️⃣ Run the Chatbot

```bash
python chatbot.py
```

---

## 💬 How It Works

1. The chatbot preprocesses all FAQ questions (lemmatization + stopword removal).
2. Converts them into **TF-IDF vectors**.
3. When the user asks a question, the chatbot computes **cosine similarity** between the user’s input and all FAQ questions.
4. The most similar answer is returned.
5. If confidence is too low, the chatbot gives a polite fallback response.

---


## 🧠 Technologies Used

* **Python 3**
* **Tkinter** (GUI)
* **NLTK** (Natural Language Processing)
* **Scikit-learn** (TF-IDF Vectorization)
* **Pillow** (for UI icons and images)
* **JSON** (for feedback logging)

---

## 📘 Example Usage

1. Launch the chatbot.
2. Ask any FAQ-related question, e.g.
   *“How can I return my order?”*
3. The chatbot responds instantly based on similarity to preloaded questions.
4. Rate the response with 👍 or 👎 to help improve quality.


---

## 💡 Future Improvements

* Add **speech recognition** for voice-based interaction.
* Integrate **deep learning models (BERT)** for better semantic understanding.
* Include a **database or API** for dynamic FAQ updates.
* Add **dark mode** and advanced UI themes.

---

## 👨‍💻 Author

**Zainab**
📧 [[zainab.abbas.3495@gmail.com](mailto:zainab.abbas.3495@gmail.com)]
💼 [LinkedIn: https://www.linkedin.com/in/zainab2006]

---


